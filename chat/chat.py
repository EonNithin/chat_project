'''
#pip -q install langchain huggingface_hub transformers sentence_transformers accelerate bitsandbytes
#pip install transformers accelerate torch langchain bitsandbytes
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from langchain import PromptTemplate  
from langchain import HuggingFacePipeline
from langchain import LLMChain

'''
import os
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
'''

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

model_id = 'google/flan-t5-small'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id, load_in_4bit=True, device_map='auto')

pipeline = pipeline(
    "text2text-generation",
    model=model, 
    tokenizer=tokenizer, 
    max_length=128
)

local_llm = HuggingFacePipeline(pipeline=pipeline)

llm_chain = LLMChain(prompt=prompt, llm=local_llm)

question = input("Enter your question: ")
print(llm_chain.run(question))

'''
import subprocess
from langchain_community.llms import Ollama

ollama = Ollama(
    base_url='http://localhost:11434',
    model="mistral"
)

# Example command: List directory contents
command = ["obs","ollama run mistral"]  # Replace with your desired command and arguments
print("Command:\n",command)
# Execute the command and capture the output (optional)
process = subprocess.run(command, capture_output=True, text=True)  # Set text=True for string output
print("Process:\n",process)
output = process.stdout
print("Output is:\n",output)
# Print the output (optional)
if output:
    print(output)


print("ollama instance initialized:",ollama)

prompt = input("enter your question: ")
response = ollama.invoke(prompt)
print(response)
