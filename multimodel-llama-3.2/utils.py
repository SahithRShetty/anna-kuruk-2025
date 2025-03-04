# The code below should be added to a util.py file

import requests
import json

from dotenv import load_dotenv, find_dotenv
import os

def load_env():
    _ = load_dotenv(find_dotenv())

  # The right API to pass in a prompt (of type string) is the completions API https://docs.together.ai/reference/completions-1
  # The right API to pass in a messages (of type of list of message) is The chat completions API https://docs.together.ai/reference/chat-completions-1

def llama32(messages, model_size=11):
  model = f"meta-llama/Llama-3.2-{model_size}B-Vision-Instruct-Turbo"
  url = f"{os.getenv('DLAI_TOGETHER_API_BASE', 'https://api.together.xyz')}/v1/chat/completions"
  payload = {
    "model": model,
    "max_tokens": 4096,
    "temperature": 0.0,
    "stop": ["<|eot_id|>","<|eom_id|>"],
    "messages": messages
  }

  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer <bearer-token>"
  }
  res = json.loads(requests.request("POST", url, headers=headers, data=json.dumps(payload)).content)

  if 'error' in res:
    raise Exception(res['error'])

  return res['choices'][0]['message']['content']

import os
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def disp_image(address):
    if address.startswith("http://") or address.startswith("https://"):
        response = requests.get(address)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(address)
    
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def resize_image(img, max_dimension = 1120):
  original_width, original_height = img.size

  if original_width > original_height:
      scaling_factor = max_dimension / original_width
  else:
      scaling_factor = max_dimension / original_height

  new_width = int(original_width * scaling_factor)
  new_height = int(original_height * scaling_factor)

  # Resize the image while maintaining aspect ratio
  resized_img = img.resize((new_width, new_height))

  resized_img.save("images/resized_image.jpg")

  print("Original size:", original_width, "x", original_height)
  print("New size:", new_width, "x", new_height)

  return resized_img


from PIL import Image

def merge_images(image_1, image_2, image_3):
    img1 = Image.open(image_1)
    img2 = Image.open(image_2)
    img3 = Image.open(image_3)
    
    width1, height1 = img1.size
    width2, height2 = img2.size
    width3, height3 = img3.size
    
    print("Image 1 dimensions:", width1, height1)
    print("Image 2 dimensions:", width2, height2)
    print("Image 3 dimensions:", width3, height3)
    
    total_width = width1 + width2 + width3
    max_height = max(height1, height2, height3)
    
    merged_image = Image.new("RGB", (total_width, max_height))
    
    merged_image.paste(img1, (0, 0))
    merged_image.paste(img2, (width1, 0))
    merged_image.paste(img3, (width1 + width2, 0))
    
    merged_image.save("images/merged_image_horizontal.jpg")
    
    print("Merged image dimensions:", merged_image.size)
    return merged_image



# pretty print JSON with syntax highlighting
from pygments import highlight, lexers, formatters
def cprint(response):
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json,
                              lexers.JsonLexer(),
                              formatters.TerminalFormatter())
    print(colorful_json)

import nest_asyncio
nest_asyncio.apply()


