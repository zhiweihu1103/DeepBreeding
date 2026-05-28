# Security Policy

## Supported Scope

This repository primarily contains data-processing scripts, configuration, documentation, and small structural examples. Security concerns are most likely to involve:

- Accidental credential or proxy configuration exposure
- Unsafe local path handling
- Accidental publication of private datasets, dumps, or large generated outputs
- Third-party source access behavior

## Reporting a Vulnerability

If you find a security issue, avoid posting sensitive details in a public issue. Contact the repository maintainers privately and include:

- Affected file or script
- Trigger conditions
- Potential impact
- Reproduction steps or suggested fix

## Operational Notes

- Do not commit `.env` files, access tokens, proxy credentials, private data, or full dumps.
- Before publishing a release, manually review `data/`, `downloads/`, `server_dumps/`, and the repository root for files that should not be under version control.
