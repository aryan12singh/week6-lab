# QuackLoan – IS212 Week 6 lab (completed starting point)

This is the end state of the Week 6 lab: `DuckFine`, a test suite that catches all five
seeded faults, and a CI workflow whose job is named `test`. Use it if you missed Week 6
and want to go straight to the Week 9 lab.

## Getting set up

1. Click **Use this template → Create a new repository**. Name it `week6-lab` and make it
   **public** (required for the protection rules and the production reviewer in Week 9).
2. Open the **Actions** tab and check the `tests` workflow has run once and is green.
   If it has not run, push any small commit to `main` (e.g. edit this README).
3. Protect `main`: **Settings → Branches → Add classic branch protection** (or
   **Settings → Rulesets → New branch ruleset**), targeting `main`, and turn on
   - **Require a pull request before merging** (leave *Require approvals* off), and
   - **Require status checks to pass**, then search for and select `test`.
4. Clone your repository and continue with Week 9, Part 1.

Locally: `python -m unittest -v`
