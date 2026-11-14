import json
from http import HTTPMethod

from workers import Request, Response, WorkerEntrypoint, fetch


class Default(WorkerEntrypoint):
    async def fetch(self, request: Request):
        if request.method != "POST":
            return Response("Method not allowed", status=405)

        received_auth = request.headers.get("Authorization")
        expected_auth = f"Bearer {self.env.FORGEJO_WEBHOOK_AUTH_HEADER}"
        if received_auth != expected_auth:
            return Response("Unauthorized", status=401)

        if request.headers.get("X-Forgejo-Event-Type") != "workflow_job_waiting":
            return Response("Ignored (not workflow_job_waiting)", status=200)

        body = await request.json()

        repo_map = json.loads(self.env.FORGEJO_GITHUB_REPO_MAP)
        repo_name = body.get("repository").get("full_name")
        target_repo = repo_map.get(repo_name)
        if not target_repo:
            return Response(f"Ignored (unmapped repo: {repo_name})", status=200)

        gh_repo = target_repo.get("repo")
        gh_pat = target_repo.get("pat")

        for runner in body.get("job").get("runs_on"):
            if not runner.startswith("gh-"):
                continue

            workflow_file = f"{runner}.yml"
            gh_response = await fetch(
                f"https://api.github.com/repos/{gh_repo}/actions/workflows/{workflow_file}/dispatches",
                method=HTTPMethod.POST,
                headers={
                    "Authorization": f"Bearer {gh_pat}",
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "dispatcher-server",
                    "Content-Type": "application/json",
                },
                body=json.dumps({"ref": body.get("repository").get("default_branch")}),
            )

            if not gh_response.ok:
                return Response(f"GitHub dispatch failed: {await gh_response.text()}", status=502)

            return Response(f"Dispatched {workflow_file} on {gh_repo} successfully", status=200)

        return Response("Ignored (not a 'gh-*' runner)", status=200)
