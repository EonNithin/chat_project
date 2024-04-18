import whisper
from langchain_community.llms import Ollama

# Initialize Ollama outside the view
llm = Ollama(model="mistral")
conversation_history = []

model = whisper.load_model("base")
result = model.transcribe("./chat/static/mp3s/blood.mp3")
print("="*50, "\nText Response from Whisper :\n", "="*50, "\n", result["text"])
result_text = result["text"]
response_text = llm.invoke(result_text)
print("="*50, "\nResponse from Mistral :\n", "="*50, "\n", response_text, "\n")

