# Build and host the documentation

The documentation is a static site generated from Markdown with MkDocs Material. You can preview it locally or publish it with the included GitHub Pages workflow.

## Preview locally

From the repository root, install the documentation requirements and start the live preview:

```bash
python -m venv .venv-docs
source .venv-docs/bin/activate
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

Open the local URL printed by MkDocs (normally `http://127.0.0.1:8000/`). The preview rebuilds as Markdown or `mkdocs.yml` changes.

To produce the static site files:

```bash
python -m mkdocs build --strict
```

MkDocs writes the generated site to `site/`. This directory is build output; edit the Markdown in `docs/` instead.

## Publish with GitHub Pages

The workflow in `.github/workflows/docs.yml` checks pull requests by building the site. On pushes to `master`, it builds and deploys the site artifact to GitHub Pages.

After the workflow is merged, configure the repository once:

1. Open the repository's **Settings → Pages**.
2. Under **Build and deployment**, select **GitHub Actions** as the source.
3. Merge or push a commit to `master` and check the **Actions** tab for the deployment result.

The workflow's GitHub Pages environment reports the published URL after the first successful deployment. A custom domain can be configured separately in repository Pages settings.

Documentation changes should be made in Markdown under `docs/`, linked in `mkdocs.yml`, and previewed with `mkdocs serve` or validated with `mkdocs build --strict`.
