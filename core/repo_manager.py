import os
import shutil
import subprocess

def clone_repo(repo_url, local_dir):
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)
    subprocess.check_call(['git', 'clone', repo_url, local_dir])

def create_branch(local_dir, branch_name):
    subprocess.check_call(['git', 'checkout', '-b', branch_name], cwd=local_dir)

def commit_and_push(local_dir, branch, msg):
    subprocess.check_call(['git', 'add', '.'], cwd=local_dir)
    subprocess.check_call(['git', 'commit', '-m', msg], cwd=local_dir)
    subprocess.check_call(['git', 'push', 'origin', branch], cwd=local_dir)

def create_pr(local_dir, title, body, reviewers):
    subprocess.check_call([
        'gh', 'pr', 'create',
        '--title', title,
        '--body', body,
        '--reviewer', reviewers
    ], cwd=local_dir)