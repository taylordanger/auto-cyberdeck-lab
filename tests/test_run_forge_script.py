import os
import shutil
import subprocess
from pathlib import Path


def test_run_forge_recovers_from_merge_state(tmp_path):
    repo = tmp_path / "repo"
    (repo / "forge").mkdir(parents=True)

    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)

    (repo / "forge" / "agent.py").write_text("print('ok')\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, check=True, capture_output=True, text=True)
    initial_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()

    subprocess.run(["git", "checkout", "-b", "ai/m3-worker"], cwd=repo, check=True)
    (repo / "README.md").write_text("branch\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "branch change"], cwd=repo, check=True, capture_output=True, text=True)

    subprocess.run(["git", "checkout", "-B", "main", initial_commit], cwd=repo, check=True)
    (repo / "README.md").write_text("main\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "main change"], cwd=repo, check=True, capture_output=True, text=True)

    subprocess.run(["git", "checkout", "ai/m3-worker"], cwd=repo, check=True)
    result = subprocess.run(["git", "merge", "main"], cwd=repo, capture_output=True, text=True)
    assert result.returncode != 0

    script_path = Path(__file__).resolve().parents[1] / "run_forge.sh"
    shutil.copy2(script_path, repo / "run_forge.sh")
    subprocess.run(["chmod", "+x", str(repo / "run_forge.sh")], check=True)

    env = os.environ.copy()
    env["FORGE_SKIP_RUN"] = "1"
    result = subprocess.run([str(repo / "run_forge.sh")], cwd=repo, env=env, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    assert "Resolving unfinished merge state" in result.stdout
