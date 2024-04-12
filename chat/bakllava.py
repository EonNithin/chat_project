import base64
from io import BytesIO
from IPython.display import HTML, display
from PIL import Image
from langchain_community.llms import Ollama

# Function to convert PIL images to Base64 encoded strings
def convert_to_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Function to display Base64 encoded images
def display_base64_image(img_base64):
    image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />'
    display(HTML(image_html))

# Initialize the Ollama model
ollama_model = Ollama(model="bakllava")  # Replace "your_model_name" with the appropriate model name

# Function to generate an image for a text prompt using the Ollama model
def generate_image_for_prompt(prompt):
    response = ollama_model.invoke(prompt)
    print("Response is:\n",response)
    image_b64 = convert_to_base64(response)
    display_base64_image(image_b64)

# Example usage:
prompt = "Generate an image related to jasmine flower"
generate_image_for_prompt(prompt)
