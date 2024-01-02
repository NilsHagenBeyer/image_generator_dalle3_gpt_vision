# Genereate Images in the loop with dalle-3 and GPT-vision

ImageReplicator is a Python tool for replicating or generating images based on textual descriptions, with the power of OpenAI's GPT-4 and DALL-E 3 models. It allows users to describe an image, modify the description to match user inputs, and then generate an image that aligns with the modified description.

## Installation
Ensure the required libraries are installed by using pip:

```shell
pip install openai Pillow
```
You also need to get your own API key from OpenAI and place it in a file called api_key.txt

## Usage

Once you instantiate the ImageReplicator class, you can enter in a prompt or instruction to guide image generation/replication in the command line terminal window. Any instruction specified should be relevant to the image generation context.

However, the ImageReplicator tool also includes a special "$" flag which can be used for special command introduction before the instruction/prompt. It has different modes of operation, which affects how the program runs. These modes can be changed during runtime by using this "$" flag.

The configurations are as follows:

- `$gen`: This command sets the tool to generate a new image based on a textual prompt that you give. 

- `$loop`: This command sets the tool to continually generate new images based on updated prompts. It will keep asking you for new prompts and generate new images until you decide to stop.

- `$replicate`: This command sets the tool to replicate an existing image. You will be guided to select an image whose description will be generated and used to create a new image.

- `$tokens <number>`: This command allows you to set a maximum token limit for the model ensuring control over usage. `<number>` needs to be replaced with the desired maximum token count.

- `$help`: This command displays a help message showing the list and explanations of all "$" commands.

To stop the program, you can simply type 'quit'.

## Example Run

Here is how you can run the ImageReplicator:

```python
api_key = get_api_key()
replicator = ImageReplicator(api_key, function="replicate")
replicator.run()
```

Or simply:

```
$python dalle3_gpt_vision_tools.py
```


## Final Notes

Please note that the quality of the generated images and descriptions rely heavily on the prompts provided by the user and the capability of OpenAI's models. As such, the more detailed and precise the instructions, the more accurate the generated image will be.
