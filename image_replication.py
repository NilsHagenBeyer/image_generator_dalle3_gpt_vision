from openai import OpenAI
import os
import base64
#import requests
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def get_image_path():
        root = Tk()
        root.withdraw() # we don't want a full GUI, so keep the root window from appearing
        image_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        root.destroy() # destroy the root window after getting the file path
        return image_path

def get_api_key():
    with open("api_key.txt", "r") as file:
        api_key = file.readline().strip()  # remove newline if present
    return api_key

def encode_image (image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def replicate(client, image_path):
    print("Replicating image...")

    # Getting the base64 string
    base64_image = encode_image(image_path)


    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
    stream=True,
    messages=[
                {
                    "role": "user",
                    "content":[
                        {"type":"text", "text": "describe this image as a prompt for a text to image model"},
                        
                        {"type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64, {base64_image}"}
                        },
                                ],
                }
            ],
    max_tokens=300,
    )

    responses = ""

    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            responses += str(chunk.choices[0].delta.content)


    response = client.images.generate(
        model="dall-e-3",
        prompt=responses,
        size="1792x1024",
        quality="standard",
        response_format="b64_json",
        n=1,
    )


    #To see the keys that are returned in the response 
    print(response.data[0].dict().keys()) 
    b64_data = response.data[0].b64_json
    
    revised_prompt = response.data[0].revised_prompt
    print (revised_prompt)

    # convert the base64 string to an image 
    #img_data = base64.b64decode(b64_data)

    return b64_data
'''    with open('generated_image.png', 'wb') as f:
        f.write(img_data)
'''
if __name__ == "__main__":
    image_path = get_image_path()
    api_key = get_api_key()
    client = OpenAI(api_key)
    replicate(client, image_path)