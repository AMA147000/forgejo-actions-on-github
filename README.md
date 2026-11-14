# Forgejo Actions on GitHub
A sort of starting template for me, and a tutorial for anyone seeing this on how to run Forgejo actions on GitHub runners since GitHub provides unlimited minutes for open source projects and Codeberg, understandably so, cannot keep up with what Microsoft can offer.

*Note that this requires a free Cloudflare worker (and thus an account) to act as a middleman dispatcher between Forgejo and GitHub*

# Different OSs
currently this repo supports:
- `ubuntu-latest`: through the official [forgejo/runner](https://code.forgejo.org/forgejo/runner) repo
- `windows-latest`: through the amazing [Crown0815/Forgejo-runner-windows-builder](https://github.com/Crown0815/Forgejo-runner-windows-builder) repo
- `macos-latest`: through my [AMA147000/forgejo-runner-macos-builder](https://github.com/AMA147000/forgejo-runner-macos-builder) repo ;)

# Steps
1. Add the Github repo as a push mirror for the Codeberg one
2. Create a new runner in Codeberg `gh-ubuntu-latest`
3. Copy the new runner's UUID and token and put them in GitHub action secrets called `UBUNTU_LATEST_RUNNER_UUID` and `UBUNTU_LATEST_RUNNER_TOKEN` respectively
- repeat steps `2` and `3` for `gh-windows-latest`, `WINDOWS_LATEST_RUNNER_UUID` and `WINDOWS_LATEST_RUNNER_TOKEN` / `gh-macos-latest`, `MACOS_LATEST_RUNNER_UUID` and `MACOS_LATEST_RUNNER_TOKEN` (with a different runner for each OS)
4. Copy the whole `.github` folder from this repo to yours
5. Follow [these steps](#wrangler) to deploy the Wrangler server
6. Create a Forgejo webhook (in the Forgejo repo) with:
- Target URL: the url Wrangler gave you (or your subdomain, if you manually changed it to that)
- Trigger on: custom event -> Workflow job events -> Waiting (only check that one)
- Authorization header: "Bearer FORGEJO_WEBHOOK_AUTH_HEADER" (of course replace FORGEJO_WEBHOOK_AUTH_HEADER with the actual secret)

*Leave anything not stated as default*

Now, in Forgejo you can run your workflows on `gh-ubuntu-latest`/`gh-windows-latest`/`gh-macos-latest`. :D

# Notes
- If you want to have this on an instance that is not codeberg, just change the "url: https://codeberg.org/" line in each `.github/gh-*-config.yml`
- Without a `.forgejo/workflows` folder Forgejo will look into the `.github/workflows` folder (which is kinda problematic (._.;) )
- To update secrets, run:
```
uv run pywrangler secret bulk .env
```

# Wrangler
1. Clone repo and create a `.env` file
```
git clone https://codeberg.org/AMA147000/forgejo-actions-on-github.git
cd forgejo-actions-on-github/dispatch-server
cp .env.example .env
```
2. Create a secure password and populate `FORGEJO_WEBHOOK_AUTH_HEADER` in `.env` with it
3. Populate the `FORGEJO_GITHUB_REPO_MAP` map in `.env` as shown in the placeholder example (create a fine grained GitHub PAT [here](https://github.com/settings/personal-access-tokens), make sure it has write access for 'Actions')
4. Deploy using Wrangler (and take a note of the url it gives you, or don't if you will manually go and change it to a subdomain you own)
```
uv run pywrangler deploy --secrets-file .env
```
