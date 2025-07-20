import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.repo_manager import clone_repo, create_branch, commit_and_push, create_pr
from core.sonarq_fetcher import fetch_sonar_report
from core.cwe_mapper import load_cwe_map, map_sonar_to_cwe
from core.code_locator import locate_vuln_file, extract_code_snippet
from core.fix_engine import run_fixes
from core.notifier import notify_reviewers
from config.settings import GITHUB_REPO_URL, SONARQUBE_PROJECT_KEY, LOCAL_PATH

def main():
    # 1. Clone repository
    print('[*] Cloning repository...')
    clone_repo(GITHUB_REPO_URL, LOCAL_PATH)
    
    # 2. Fetch SonarQube report
    print('[*] Fetching SonarQube vulnerabilities...')
    #sonar_report = fetch_sonar_report(SONARQUBE_PROJECT_KEY)
    sonar_report = fetch_sonar_report(r"D:\VATest\auto-vuln-fixer\config\sonar_commerial.json")
    path = r"D:\VATest\auto-vuln-fixer\config\sonar_commerial.json"
    with open(path, "r", encoding="utf-8") as f:
     sonar_report = json.load(f)
    issues = sonar_report.get("issues", [])


    issues = sonar_report.get("issues", [])
    print(f'[*] {len(issues)} issues fetched.')
    
    # 3. Load CWE mapping strategies
    cwe_map = load_cwe_map(os.path.join('config', 'cwe_map.json'))

    fix_branch = "ai-vuln-autofix"
    branch_created = False
    changes_detected = False

    # 4. Process each issue
    for issue in issues:
        rule = issue.get("rule")
        cwe_strategy = map_sonar_to_cwe(rule, cwe_map)

        file_path, line = locate_vuln_file(issue)
        vuln_desc = issue.get("message", "")
        code_snippet = extract_code_snippet(file_path, int(line), LOCAL_PATH)

        if not cwe_strategy:
            print(f"[*] Unmapped issue: {rule}. Using OpenAI LLM.")
            run_fixes(file_path, int(line), code_snippet, "OPENAI", LOCAL_PATH, vuln_desc)
        else:
            print(f"[*] Mapped issue: {rule}. Strategy: {cwe_strategy['fix_strategy']}")
            run_fixes(file_path, int(line), code_snippet, cwe_strategy['fix_strategy'], LOCAL_PATH, vuln_desc)

        # Check for new changes after each fix
        git_status = os.popen(f"cd {LOCAL_PATH} && git status --porcelain").read()
        if git_status.strip():
            changes_detected = True
            if not branch_created:
                create_branch(LOCAL_PATH, fix_branch)
                branch_created = True

    # 5. If there are changes, commit and push, then open PR
    if changes_detected:
        print("[*] Committing and creating PR...")
        commit_and_push(LOCAL_PATH, fix_branch, "Automated fix for vulnerabilities detected by SonarQube")
        create_pr(LOCAL_PATH, "AI Vulnerability Autofix", "This PR fixes vulnerabilities detected via automation.", "reviewer1,reviewer2")
        notify_reviewers()
    else:
        print("[*] No changes detected, nothing to commit.")

if __name__ == "__main__":
    main()