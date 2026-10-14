# QuackLoan - IS212 Week 9 lab

This repository continues the Week 6 DuckFine starter with the web app and gated release pipeline from the Week 9 lab.

## Run locally

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest -v
flask --app app run --port 5001
```

Visit http://localhost:5001/ for the fine checker, `/health` for the health response, or `/fine?days=5&deluxe=1` for a JSON quote. Five days late means three chargeable days: $1.50 for a standard duck or $3.00 for Deluxe. Non-numeric and negative API inputs return HTTP 400.

For the browser journey, leave the server running and use another terminal:

```bash
source .venv/bin/activate
python -m pip install playwright
python -m playwright install chromium
BASE_URL=http://localhost:5001/ python -m unittest discover -s e2e -v
bash smoke.sh http://localhost:5001
```

The E2E folder deliberately has no `__init__.py`; ordinary unittest discovery runs the seven fee-rule tests and four Flask integration tests without needing a browser or live server.

## What the pipeline proves

| Job | Evidence |
| --- | --- |
| lint | Ruff checks the source. |
| test | Unit and Flask integration tests check the source. |
| audit | pip-audit checks the deployment dependencies for known vulnerabilities. |
| package | Installs dependencies into build, includes all three app files, builds one ZIP and uploads an SPDX SBOM. |
| smoke | Extracts the ZIP, runs it and probes health and fee calculations over HTTP. |
| e2e | Extracts the same ZIP and checks the Deluxe fine through Chromium. |
| staging | On main, receives the package after both smoke and e2e pass. |
| production | Receives the same package after staging passes and the required reviewer approves. |

Main requires pull requests and passing test, lint, audit, smoke and e2e checks. The production environment requires the repository owner as reviewer; administrator bypass is disabled and self-review is allowed for this individual lab.

The package job is the only place that builds the deployable ZIP. Downstream jobs download that artifact; they do not rebuild it from source. The SBOM explains the direct and transitive dependencies inside the package. AWS `CodeSha256` values let the reviewer verify that staging and production received identical bytes.

## AWS configuration

Use the AWS Academy Learner Lab in `us-east-1`, its existing `LabRole`, Python 3.13 and x86_64. The lab names are `quackloan-staging` and `quackloan-prod` with function URLs using auth type NONE. Set `FUNCTION_NAME` and `FUNCTION_URL` separately in the staging and production GitHub environments. Store the three temporary AWS credentials as environment secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN`. Refresh them when a new Learner Lab session starts.

The initial staging and production jobs are placeholders until Part 4 replaces them with the AWS deployment jobs. The execution record identifies which stages have actually run.

## Release-gate experiments

- Removing the API ValueError handler gives HTTP 500 for negative days. The Flask integration test catches it; the fee-rule unit tests still pass.
- Removing the Deluxe checkbox value sends `deluxe=on` and quotes $1.50. The browser test expects $3.00 and blocks the merge, even though source and API smoke checks pass.
- Omitting `duckfine.py` from the ZIP leaves source checks green but makes the extracted app fail to start. Both package checks block the merge. Restore the copy line before integrating.

Production approval records a person's decision after reviewing green checks, the staging smoke result, and the running staging app. End the Learner Lab after release verification to save credits.
