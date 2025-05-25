import subprocess
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class LLMServiceBase:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Must implement generate method")

class OllamaLLMService(LLMServiceBase):
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "deepseek-r1:1.5b")
        print(f"Using Ollama model: {self.model_name}")

    def generate(self, prompt: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error calling Ollama: {e}")
            return ""