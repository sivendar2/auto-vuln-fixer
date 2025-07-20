import subprocess
import os

def semgrep_autofix(java_path, repo_path):
    abs_path = os.path.join(repo_path, java_path)
    # You can tweak the command/config as needed
    try:
        subprocess.run(['semgrep', '--config', 'auto', '--autofix', abs_path], check=True)
    except Exception as e:
        print(f"Semgrep autofix failed for {abs_path}: {e}")