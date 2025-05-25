# llm/llm_service.py

import subprocess
import json

class LLMServiceBase:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Must implement generate method")

class OllamaLLMService(LLMServiceBase):
    def __init__(self, model_name="llama2"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        # Call Ollama CLI with prompt and return response
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, "--prompt", prompt],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error calling Ollama: {e}")
            return ""

# Placeholder for GPT-4o or other LLMs
class GPT4oLLMService(LLMServiceBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        # Implement API call to GPT-4o here
        pass