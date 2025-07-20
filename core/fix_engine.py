# Main orchestrator for applying fixes 
from .fixers.semgrep_fixer import semgrep_autofix
from .fixers.javaparser_fixer import javaparser_fix
from .fixers.openai_fixer import openai_fix
from .fixers.snyk_fixer import snyk_fix

def run_fixes(java_path, line, snippet, fix_strategy, repo_path, desc):
    if fix_strategy == "SEMIGREP_SQLI":
        semgrep_autofix(java_path, repo_path)
    elif fix_strategy == "SEMIGREP_LOG_INJECTION":
        semgrep_autofix(java_path, repo_path)
    elif fix_strategy == "JAVAPARSER_REFACTOR":
        javaparser_fix(java_path, repo_path)
  #  elif fix_strategy == "OPENAI":
   #     openai_fix(java_path, line, snippet, repo_path, desc)
    # Always run Snyk for dependencies
    snyk_fix(repo_path)