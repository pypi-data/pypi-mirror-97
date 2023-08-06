import subprocess
from pathlib import Path

projects = Path.home().glob("**/.dev")
projects = [project.parent for project in projects if "cookiecutter-pypackage" not in str(project)]
for project in projects:
    print(f"==== {project}")
    result = subprocess.run(
        "cookiecutter_project_upgrader -p true -m true".split(),
        cwd=str(project),
        encoding="utf-8",
    )
    print("\n\n")
    result.check_returncode()
    result = subprocess.run(
        "git push".split(),
        cwd=str(project),
        encoding="utf-8",
    )
    result.check_returncode()

print()
print("=================")
print("Successful")
