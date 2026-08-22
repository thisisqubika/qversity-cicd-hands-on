# Qversity CI/CD Hands-On Workshop

A minimal, fully working Flask API with a real GitHub Actions + Render
pipeline, built to teach CI/CD concepts to new hires:

- Automated testing on every push/PR
- Build & deploy automation
- Staging vs. production environments
- Secrets & environment variables
- Manual approval gates before production deploys

## Quick start (local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
flask --app app.main run
```

Visit `http://127.0.0.1:5000/health` and `http://127.0.0.1:5000/items`.

## Project layout

```
app/            Flask API (/health, /items)
tests/          pytest unit tests
render.yaml     Render service definitions (staging + prod)
.github/workflows/
  ci.yml               lint + test, every push/PR
  deploy-staging.yml   test -> deploy to staging, on push to develop
  deploy-prod.yml      test -> approval gate -> deploy to prod, on push to main
```

## Doing the workshop

Start with [`WALKTHROUGH.md`](./WALKTHROUGH.md). It covers Render setup,
secrets, branch protection, and running the pipeline end to end.
