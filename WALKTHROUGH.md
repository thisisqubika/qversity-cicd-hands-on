# Workshop walkthrough

Work through these steps in order.

## 1. Run it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
flask --app app.main run
```

Visit `/health`. You should see `{"environment": "unknown", "status": "ok"}`
(Flask 3 sorts JSON keys alphabetically by default), since no `APP_ENV` is
set locally.

## 2. Read `ci.yml`

Open `.github/workflows/ci.yml`. It runs on every push and every PR to any
branch: install dependencies, run `flake8`, run `pytest`. That is the gate
that keeps broken code from merging without anyone having to remember to
run checks by hand. If you push to a branch that already has an open PR, CI
runs twice (once for the push, once for the PR). You will see two green
checks instead of one. That is normal.

## 3. Fork and set up your `develop` branch

Fork this repo to your own GitHub account. Keep the fork public. Branch
protection rules and Environment required reviewers (steps 5 and 6) are not
available on private repos on GitHub's free plan.

If your fork does not already have a `develop` branch, create and push one
now. The staging Render service (next step) tracks it:

```bash
git checkout -b develop
git push -u origin develop
```

## 4. Create your Render services

1. Sign up at Render (free) and connect your GitHub account.
2. Push your fork to Render as a Blueprint (New -> Blueprint -> pick
   your fork). Render reads `render.yaml` and creates two web services:
   `qversity-cicd-staging` (tracking `develop`) and `qversity-cicd-prod`
   (tracking `main`). Both have `autoDeploy: false`. Render builds them
   once but does not redeploy automatically on future pushes.
3. For each service, open Settings -> Deploy Hook and copy the URL.

## 5. Wire up secrets

In your GitHub repo: Settings -> Secrets and variables -> Actions, add:

- `STAGING_DEPLOY_HOOK` = the staging service's deploy hook URL
- `PROD_DEPLOY_HOOK` = the production service's deploy hook URL

After tests pass, `deploy-staging.yml` and `deploy-prod.yml` curl these
URLs. The app never sees these secrets; only the workflow does.

## 6. Require CI to pass before merging

Settings -> Branches -> Add branch protection rule for both `develop`
and `main`: require the `lint-and-test` status check (from `ci.yml`) to
pass before merging.

## 7. Add the production approval gate

Settings -> Environments -> New environment, name it `production`.
Add yourself (or a teammate) as a required reviewer. That matches the
`environment: production` line in `deploy-prod.yml`. GitHub pauses the
deploy job until someone approves it.

## 8. Exercise: ship a change to staging

1. Create a branch off `develop`, change the `name` of one item in
   `app/main.py`'s `/items` list (e.g. `"widget"` -> `"sprocket"`).
2. Open a PR into `develop`. Watch the `CI` check run. It should go red,
   because `tests/test_main.py` still asserts the old literal `"widget"`.
   That is intentional. CI is flagging a code change that needs a matching
   test update.
3. Update the assertion in `tests/test_main.py` to expect `"sprocket"`
   instead of `"widget"`, and push again. Watch `CI` go green.
4. Merge it. Watch `deploy-staging.yml` run in the Actions tab: test job,
   then deploy job. A green workflow only means Render accepted the deploy
   request. Open the Render dashboard to confirm the build completed
   successfully.
5. Visit your staging service's `/items` URL and confirm the change is
   live, and `/health` reports `"environment": "staging"`. If the service
   had gone idle, the first request after a fresh deploy on the free tier
   can take up to a minute to respond (cold start). That is normal on the
   free tier, not a broken deploy.

## 9. Exercise: promote to production

1. Open a PR from `develop` into `main`. Watch `CI` run again.
2. Merge it. Watch `deploy-prod.yml` start. It runs tests first, then the
   `deploy` job shows Waiting for review.
3. Approve the deployment in the Actions tab. The deploy hook is called
   with `&ref=${{ github.sha }}`, so the commit you approve is the exact
   commit that ships, even if a later merge lands while you were deciding.
4. Visit your production service's `/items` and `/health` URLs and confirm
   the change is live under `"environment": "production"`. As in step 8,
   a green workflow only means Render accepted the request. Check the
   Render dashboard to confirm the build succeeded.

## 10. Recap

You just exercised all five concepts this workshop covers:

- Automated testing on PRs via the `CI` check.
- Build and deploy automation through `deploy-staging.yml` and
  `deploy-prod.yml` calling Render deploy hooks.
- Separate environments: `develop`/staging and `main`/production, each
  with its own `APP_ENV`.
- Secrets and environment variables: `STAGING_DEPLOY_HOOK`,
  `PROD_DEPLOY_HOOK`, and `APP_ENV`.
- Manual approval gates: the `production` GitHub Environment pauses
  `deploy-prod.yml` until a reviewer approves. The deploy hook uses
  `ref=${{ github.sha }}`, so the approved commit is the one that ships.
