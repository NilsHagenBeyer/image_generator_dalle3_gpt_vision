from openai import OpenAI 
import os
import base64
from PIL import Image
from io import BytesIO
import time
import image_replication
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class ImageReplicator:
    def __init__(self, api_key, name=None, function="loop", max_tokens=300):
        self.client = OpenAI (api_key=api_key)
        self.image_counter= 0
        if name is None:
            self.name = input("Enter a name for the image series: ")
        else:
            self.name = name
        self.function = function
        self.max_tokens = max_tokens

    def get_description (self, base64_image, instruction):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            stream=True,
            messages=[
                {
                    "role": "user",
                    "content":[
                        {"type":"text", "text": f"""Your task is two parts: one to describe this
                        image in detail but also to modify the description to match and reflect
                        and emphasize the requests, inputs made by the user. User is not describing
                        the image to you but wishes you to alter the detailed description to reflect
                        the user provided inputs. User is requesting these changes to the overall
                        description of the image. Be truthful to the original image with new instructions
                        in mind. don't mention anythig about user instructions not matching the image,
                        simply describe the image with the new user additions in
                        mind\n\nuser instructions/input:\n\n {instruction}"""},
                        
                        {"type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64, {base64_image}"}
                        },
                    ]
                }
            ],
            max_tokens=self.max_tokens,
        )
        responses=  ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                responses += str(chunk.choices[0].delta.content)
        
        return responses
    
    # a function which opens a tkinter window and asks the user to select an image
    def get_image_path(self):
        self.root = Tk()
        self.root.withdraw()
        image_path = askopenfilename()
        self.root.destroy()
        return image_path

    def generate_image (self, promt):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=promt,
            size="1024x1024",
            quality="standard",
            response_format="b64_json",
            n=1,
        )
        return response.data[0].b64_json

    def save_image(self, b64_data):
        img_data = base64.b64decode(b64_data)
        # create the folder if it doesn't exist
        image_path = f'images/{self.name}/'
        if not os.path.exists(image_path):
            os.makedirs(f'images/{self.name}')
        image_filepath = image_path + self.genereate_image_name()
        with open(image_filepath, 'wb') as f:
            #show the image from the path
            img =Image.open(BytesIO(img_data))
            img.show()
            f.write(img_data)        
        self.image_counter += 1

    # a function to generate a name for the image based on the unix timestamp
    def genereate_image_name(self,):
        return f"{self.name}_{int(time.time())}.png"
    
    # checks instructions for special commands
    def decode_instructions(self, instruction):
        if instruction.lower().startswith('$'):            
            if instruction.lower().endswith('loop'):
                self.function = "loop"
                print("Function set to loop")
            elif instruction.lower().endswith('gen'):
                self.function = 'gen'
                print("Function set to generate")
            elif instruction.lower().endswith('replicate'):
                self.function = 'replicate'
                print("Function set to replicate")
                return instruction
            elif instruction.lower()[1:].startswith('tokens'):
                try:
                    self.max_tokens = int(instruction.split()[1])
                    print(f"Max tokens set to {self.max_tokens}")
                except:
                    print("Invalid number of tokens!")
            elif instruction.lower().endswith('help'):
                print("$loop - sets the function to loop")
                print("$gen - sets the function to generate")
                print("$replicate - sets the function to replicate")
                print("$tokens <number> - sets the max tokens to <number>")
                print("$help - shows this help message")
            else:
                print("Invalid function name!")
            # ask for a new instruction
            instruction = self.read_input()
            instruction = self.decode_instructions(instruction)

        return instruction
    
    def read_input(self):
        instruction = input(f"Enter an instruction ({self.function}) (token={self.max_tokens}) (or 'quit' to exit): ")
        return instruction


    def run(self):
        quit_flag = False
        while True and not quit_flag:
            instruction = self.read_input()
            if instruction.lower() == 'quit':
                break            
            instruction = self.decode_instructions(instruction)
            
            
            if self.function == "gen":
                b64_data = self.generate_image(instruction)
                self.save_image(b64_data)           
                print("Image generated successfully!")
            
            while True and self.function == "loop":
                instruction = self.read_input()
                instruction = self.decode_instructions(instruction)
                if self.function == "loop":
                    if instruction.lower() == 'quit':
                        quit_flag = True
                        break
                    elif instruction:
                        description = self.get_description(b64_data, instruction)
                        b64_data = self.generate_image(description) 
                        self.save_image(b64_data)

                        print("Image generated successfully!")
            
            if self.function == "replicate":
                image_path = self.get_image_path()
                b64_data = image_replication.replicate(self.client, image_path)
                self.save_image(b64_data)
                print("Image generated successfully!")

def get_api_key():
    with open("api_key.txt", "r") as file:
        api_key = file.readline().strip()  # remove newline if present
    return api_key

if __name__ ==  "__main__":
    api_key = get_api_key(  )
    replicator = ImageReplicator(api_key, function="replicate")
    replicator.run()