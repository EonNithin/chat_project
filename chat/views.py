from django.shortcuts import render
from django.http import JsonResponse
from langchain_community.llms import Ollama

# Initialize Ollama outside the view
llm = Ollama(model="Eon_Assistant")
conversation_history = []

def ollama_generate_response(question):
    global conversation_history
    conversation_history.append(question)
    full_prompt = "\n".join(conversation_history)
    response_text = llm.invoke(full_prompt)
    conversation_history.append(response_text)
    print("Response:\n", response_text, "\n")
    return response_text

def generate_response(request):
    if request.method == 'POST':
        question = request.POST.get('question', '')
        print("Question is : \n", question)
        response = ollama_generate_response(question)
        print("Response is : \n", response)
        return JsonResponse({'question': question, 'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def chat_page(request):
    return render(request, 'chat_page.html')
