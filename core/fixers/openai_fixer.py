# Generate fix using OpenAI API 
import openai
from config.settings import OPENAI_TOKEN

def openai_fix(java_path, line, code, repo_path, desc):
    openai.api_key = OPENAI_TOKEN
    prompt = f"Fix this security issue:\n{desc}\n\nCode:\n{code}\nRespond ONLY with fixed code."
    result = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=500
    )
    # Write back changes
    fixed = result["choices"][0]["text"]
    abs_path = f"{repo_path}/{java_path}"
    lines = open(abs_path).readlines()
    lines[line-1] = fixed + '\n'
    open(abs_path, "w").writelines(lines)