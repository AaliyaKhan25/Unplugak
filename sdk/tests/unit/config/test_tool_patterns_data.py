"""Tests for packaged tool/agent TOML maps."""

from __future__ import annotations

import re

from unplug.config.tools import (
    DEFAULT_SIDE_EFFECT_PATTERNS,
    DEFAULT_TAINT_SOURCE_PATTERNS,
    PROFILE_ALLOWED_PATTERNS,
    PROFILE_BLOCKED_PATTERNS,
    ToolPolicyConfig,
    ToolProfile,
)
from unplug.core.agent.intent import _BENIGN_INTENT, _DESTRUCTIVE_INTENT
from unplug.core.agent.toolchain import (
    _EXEC_TOOLS,
    _NETWORK_TOOLS,
    _READ_TOOLS,
    _SUSPICIOUS_CHAINS,
    _WRITE_TOOLS,
)
from unplug.data.maps_loader import load_agent_tools_map, load_tool_patterns_map


def test_tool_patterns_toml_loads() -> None:
    data = load_tool_patterns_map()
    assert len(data.side_effect) >= 20
    assert len(data.taint_source) >= 8
    assert set(data.profiles) >= {"readonly", "messaging", "full"}


def test_agent_tools_toml_loads() -> None:
    data = load_agent_tools_map()
    assert len(data.high_risk_patterns) >= 10
    assert data.toolchain.read_tools
    assert len(data.toolchain.suspicious_chains) >= 8
    re.compile(data.intent_benign_regex)
    re.compile(data.intent_destructive_regex)
    re.compile(data.toolchain.sensitive_path_regex)


def test_module_defaults_match_bundled_maps() -> None:
    tool_maps = load_tool_patterns_map()
    agent_maps = load_agent_tools_map()

    assert tool_maps.side_effect == DEFAULT_SIDE_EFFECT_PATTERNS
    assert tool_maps.taint_source == DEFAULT_TAINT_SOURCE_PATTERNS
    readonly = tool_maps.profiles["readonly"].blocked_patterns
    assert PROFILE_BLOCKED_PATTERNS[ToolProfile.READONLY] == readonly
    assert PROFILE_ALLOWED_PATTERNS[ToolProfile.MESSAGING] is None
    assert agent_maps.high_risk_patterns[0].startswith("^")

    assert agent_maps.toolchain.read_tools == _READ_TOOLS
    assert agent_maps.toolchain.write_tools == _WRITE_TOOLS
    assert agent_maps.toolchain.network_tools == _NETWORK_TOOLS
    assert agent_maps.toolchain.exec_tools == _EXEC_TOOLS
    assert len(_SUSPICIOUS_CHAINS) == len(agent_maps.toolchain.suspicious_chains)


def test_intent_regexes_detect_expected_phrases() -> None:
    assert _BENIGN_INTENT.search("please summarize this document")
    assert _DESTRUCTIVE_INTENT.search("delete all files")
    assert not _BENIGN_INTENT.search("delete all files")


def test_tool_policy_uses_bundled_side_effect_patterns() -> None:
    policy = ToolPolicyConfig()
    assert policy.is_side_effect("shell")
    assert policy.is_taint_source("web_fetch")
    assert policy.is_read_only("search")
