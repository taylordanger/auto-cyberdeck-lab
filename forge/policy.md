# Policy

## Rules
1. Do exactly one small useful task per run.
2. Prefer docs, tests, tiny scripts, or small refactors.
3. Do not remove large amounts of code.
4. Do not touch secrets, credentials, SSH keys, `.env` files, or system files.
5. Do not edit files outside this repository.
6. Do not add network calls except to the local Ollama server.
7. Maximum 5 files changed per run.
8. Maximum 300 new/changed lines per run.
9. Update `DECISIONS.md`.
10. Update `CHANGELOG.md` when a meaningful change is made.
11. If tests fail, either fix the issue or commit nothing.
12. When uncertain, improve documentation instead of changing code.