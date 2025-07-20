from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_REPO_URL = os.getenv('GITHUB_REPO_URL', 'https://github.com/sivendar2/employee-department-1.git')
SONARQUBE_URL = os.getenv("SONARQUBE_URL")
SONARQUBE_TOKEN = os.getenv("SONARQUBE_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_API_KEY")

SONARQUBE_PROJECT_KEY = os.getenv("SONARQUBE_PROJECT_KEY", "dummy-key")
LOCAL_PATH = os.getenv("LOCAL_PATH", "./repo")