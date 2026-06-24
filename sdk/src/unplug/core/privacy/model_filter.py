"""Production privacy filter backed by a token-classification checkpoint."""

from __future__ import annotations

import logging
from pathlib import Path
from threading import Lock
from typing import TYPE_CHECKING

from unplug.api.types import Finding
from unplug.core.pattern_loader import load_privacy_entity_label_map, load_privacy_label_map
from unplug.core.privacy.ner_decode import decode_ner_spans, normalize_ner_label

if TYPE_CHECKING:
    from transformers import PreTrainedModel, PreTrainedTokenizerBase

_logger = logging.getLogger("unplug.privacy.model")


class TokenPrivacyFilter:
    """NER/token-classification checkpoint for PII and secret span detection."""

    def __init__(
        self,
        model_source: str | Path,
        *,
        threshold: float = 0.5,
        max_length: int = 512,
        device: str | None = None,
        local_files_only: bool = False,
        eager_load: bool = True,
    ) -> None:
        self._model_source = str(model_source)
        self._threshold = threshold
        self._max_length = max_length
        self._local_files_only = local_files_only
        self._entity_map = load_privacy_entity_label_map()
        self._pf_label_map = load_privacy_label_map()
        self._tokenizer: PreTrainedTokenizerBase | None = None
        self._model: PreTrainedModel | None = None
        self._device: str | None = device
        self._load_lock = Lock()
        if eager_load:
            self.load()

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    @property
    def model_source(self) -> str:
        return self._model_source

    def load(self) -> None:
        if self._model is not None:
            return
        with self._load_lock:
            if self._model is not None:
                return
            try:
                import torch
                from transformers import AutoModelForTokenClassification, AutoTokenizer
            except ImportError as exc:
                msg = (
                    "TokenPrivacyFilter requires transformers and torch; "
                    "install unplug-ai[ml] or server [ml] extra"
                )
                raise RuntimeError(msg) from exc

            from unplug.ml.device import resolve_torch_device

            source = self._model_source
            path = Path(source)
            load_kwargs = {"local_files_only": self._local_files_only}
            if path.is_dir():
                source = str(path)

            self._tokenizer = AutoTokenizer.from_pretrained(source, **load_kwargs)
            self._model = AutoModelForTokenClassification.from_pretrained(
                source,
                **load_kwargs,
                use_safetensors=True,
                torch_dtype=torch.float32,
            )
            device = resolve_torch_device(self._device)
            model_loaded = self._model
            if model_loaded is None:
                msg = "Privacy filter failed to load model"
                raise RuntimeError(msg)
            model_loaded.to(device)
            model_loaded.eval()
            self._device = device
            _logger.info("Loaded token privacy filter from %s on %s", self._model_source, device)

    def unload(self) -> None:
        self._model = None
        self._tokenizer = None

    def _entity_to_subcategory(self, entity: str) -> str:
        key = entity.strip().upper()
        return self._entity_map.get(key, self._entity_map.get("DEFAULT", "private_other"))

    def scan(self, text: str, *, baseline: list[Finding]) -> list[Finding]:
        if not text:
            return baseline
        self.load()
        tokenizer = self._tokenizer
        model = self._model
        if tokenizer is None or model is None:
            msg = "Privacy filter failed to load tokenizer/model"
            raise RuntimeError(msg)

        import torch

        covered = {(f.span_start, f.span_end) for f in baseline}
        extra: list[Finding] = []

        encoding = tokenizer(
            text,
            return_offsets_mapping=True,
            truncation=True,
            max_length=self._max_length,
            return_tensors="pt",
        )
        offsets = encoding.pop("offset_mapping")[0].tolist()
        model_inputs = {k: v.to(self._device) for k, v in encoding.items()}

        with torch.no_grad():
            logits = model(**model_inputs).logits[0]

        probs = torch.softmax(logits, dim=-1)
        id2label_raw = model.config.id2label
        if id2label_raw is None:
            msg = "Privacy model missing id2label mapping"
            raise RuntimeError(msg)
        id2label = {int(k): str(v) for k, v in id2label_raw.items()}
        labels: list[str] = []
        scores: list[float] = []
        for idx in range(len(offsets)):
            pred_id = int(probs[idx].argmax().item())
            labels.append(id2label.get(pred_id, "O"))
            scores.append(float(probs[idx][pred_id].item()))

        for span in decode_ner_spans(
            offsets,
            labels=labels,
            scores=scores,
            threshold=self._threshold,
        ):
            key = (span.start, span.end)
            if key in covered:
                continue
            subcategory = self._entity_to_subcategory(span.entity)
            pf_label = self._pf_label_map.get(subcategory, "private_other")
            extra.append(
                Finding(
                    category="leakage",
                    subcategory=pf_label,
                    stage="privacy_filter",
                    span_start=span.start,
                    span_end=span.end,
                    score=span.score,
                    evidence=f"Privacy model detected {normalize_ner_label(span.entity)}",
                    replacement=None,
                )
            )
            covered.add(key)

        return [*baseline, *extra]
