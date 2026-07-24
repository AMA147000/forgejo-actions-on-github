# Forgejo Actions on GitHub
A sort of starting template for me, and a tutorial for anyone seeing this on how to run Forgejo actions on GitHub runners since GH provides unlimited minutes for open source projects and Codeberg, understandably so, cannot keep with what Microsoft can offer.

Of course this method is not perfect as if for example the Forgejo action was called on a PR or dispatched manually, the GH runner will require manual dispatching or waiting for the cron schedule, but it is better than nothing.

# Different OSs
currently this repo supports:
- `ubuntu-latest`: through the official [forgejo/runner](https://code.forgejo.org/forgejo/runner) repo
- `windows-latest`: through the amazing [Crown0815/Forgejo-runner-windows-builder](https://github.com/Crown0815/Forgejo-runner-windows-builder) repo
- `macos-latest`: through my [AMA147000/forgejo-runner-macos-builder](https://github.com/AMA147000/forgejo-runner-macos-builder) repo ;)

*If you want to disable one of the OSs, simply remove its workflow and config from the `.github` folder.*

# Steps
1. Add the GH repo as a push mirror for the Codeberg one
2. Create a new runner in Codeberg
3. Copy the the new runner's UUID and token and put them in GH action secrets called `UBUNTU_LATEST_RUNNER_UUID` and `UBUNTU_LATEST_RUNNER_TOKEN` respectively
- repeat steps `2` and `3` for `WINDOWS_LATEST_RUNNER_UUID` and `WINDOWS_LATEST_RUNNER_TOKEN` / `MACOS_LATEST_RUNNER_UUID` and `MACOS_LATEST_RUNNER_TOKEN` (with a different runner for each OS)
4. Copy the whole `.github` folder from this repo to yours
5. In your Forgejo workflows specify that they run on `gh-ubuntu-latest`/`gh-windows-latest`/`gh-macos-latest`
