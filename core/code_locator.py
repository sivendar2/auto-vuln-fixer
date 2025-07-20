import os

def locate_vuln_file(issue):
    """
    Maps SonarQube or Fortify file/component identifiers to actual source paths.
    Supports:
      - SonarQube commercial: "component": "com.ameya.service.EmployeeInfoBusinessService"
      - Fortify or others: "file": "src/main/java/com/ameya/service/EmployeeInfoBusinessService.java"
    """
    component = issue.get("component") or issue.get("file")
    
    if component.endswith(".java"):
        # Already a file path (possibly with colons)
        path = component.replace(":", "/")
    else:
        # Java-style package (dot notation) -> file path
        path = os.path.join("src", "main", "java", *component.split(".")) + ".java"
    
    line = int(issue.get("line", 1))
    return path, line


def extract_code_snippet(java_path, line, repo_path, context=3):
    """
    Extracts code lines around the specified line from the resolved file path.
    """
    abs_path = os.path.join(repo_path, java_path)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"[ERROR] File not found: {abs_path}")
    
    print(f"[*] Reading from: {abs_path}")
    
    with open(abs_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    start = max(0, line - context - 1)
    end = min(len(lines), line + context)
    return "".join(lines[start:end])
