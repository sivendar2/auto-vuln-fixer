# Parse SonarQube JSON reports 
import json
import requests
from config.settings import SONARQUBE_TOKEN, SONARQUBE_URL

def fetch_sonar_report(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
    headers = {"Authorization": f"Bearer {SONARQUBE_TOKEN}"}
    url = f"{SONARQUBE_URL}/api/issues/search?projectKeys={project_key}&types=VULNERABILITY"
    return requests.get(url, headers=headers).json()