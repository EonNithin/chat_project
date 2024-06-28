
from transformers import pipeline, set_seed

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# google/flan-t5-base
# facebook/blenderbot-400M-distill
text2text_generator = pipeline("text2text-generation", model="google/flan-t5-base")

transcribed_text = """ 
Listen the minute.com. Eggs. Eggs are great. Where would we be without them? They are so useful. I can't imagine life, or cooking, without them. There are many ways of cooking eggs for breakfast, fried eggs, scrambled eggs, boiled eggs, etc. There are even many ways of cooking these. You can have a runny or hard fried egg, or even have it sunny side up. You can have soft or hard boiled eggs, and fluffy scrambled eggs. There are also many things to put on top of eggs. Mayonnaise, ketchup, salt, soy sauce. Each country has something different. I like cooking with eggs. I particularly like breaking them. I can now do it with one hand without breaking the yolk. Sometimes it gets messy and the egg white starts dripping down your arm.
"""
question = f"Explain about: {transcribed_text}"

print("Summarization Response is:\n",summarizer(question, do_sample=False),"\n")

print("Text 2 Text Generation Response is:\n",text2text_generator(question),"\n")


'''

from transformers import pipeline, Conversation

# Load the chatbot pipeline with the desired model
chatbot = pipeline(model="facebook/blenderbot-400M-distill")

def run_chatbot():
  # Start the conversation with the user's opening message
  conversation = Conversation("Hello, how can I help you?")

  while True:
    # Get the user's latest message
    user_message = input("You: ")

    # Update conversation (optional for context)
    conversation.add_message({"role": "user", "content": user_message})

    # Get the chatbot's response using the latest message
    response = chatbot(user_message)

    # Print the chatbot's response
    print(f"Chatbot: {response[0]['generated_text']}")

    # Check for exit condition (optional)
    if user_message.lower() == "quit":
      break

if __name__ == "__main__":
  run_chatbot()

'''