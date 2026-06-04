import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"


def ask_ollama(prompt: str):
    """
    Send prompt to Ollama and return response.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "")

    except requests.exceptions.ConnectionError:
        return (
            "Ollama server is not running. "
            "Please start Ollama using: ollama serve"
        )

    except Exception as e:
        return f"Error while calling Ollama: {str(e)}"