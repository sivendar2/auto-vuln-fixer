import subprocess
import os

def snyk_fix(repo_path):
    abs_path = os.path.join(repo_path, 'pom.xml')
    try:
        subprocess.run(['snyk', 'fix', '--all-projects', '--file', abs_path], check=False)
    except Exception as e:
        print(f"Snyk fix failed in {repo_path}: {e}")