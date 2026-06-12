# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Unplug, please report it responsibly.

**Preferred:** [GitHub Security Advisories](https://github.com/UnplugAI/Unplug/security/advisories/new) (private disclosure).

**Email:** [security@unplug-ai.org](mailto:security@unplug-ai.org)

Please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce or a proof of concept
- Affected versions (e.g. `unplug-ai==0.3.0`)

Do **not** open a public GitHub issue for security vulnerabilities.

## Response Timeline

- **Acknowledgment** within 3 business days
- **Initial assessment** within 7 business days
- **Fix or mitigation plan** communicated as soon as a path is identified

We will coordinate disclosure timing with you and credit reporters who wish to be named.

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest on PyPI | Yes |
| Older releases | Best effort |

## Scope

In scope:

- The `unplug-ai` Python SDK (`sdk/`)
- Official CI workflows and release artifacts

Out of scope:

- Third-party integrations (Firecrawl, Hugging Face Hub, etc.) unless the SDK introduces the vulnerability
- Hosted services (report to the respective operator)
