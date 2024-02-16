## Imports
from huggingface_hub import hf_hub_download

## Define model name and file name
model_name = "TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF"
model_file = "mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf"

## Use the following model_name and model_file if you have 8gb ram or less
# model_name = "TheBloke/Mistral-7B-OpenOrca-GGUF"
# model_file = "mistral-7b-openorca.Q4_K_M.gguf"

## Use the following model_name and model_file if you have 16gb ram or less
# model_name = "TTheBloke/vicuna-13B-v1.5-16K-GGUF"
# model_file = "vicuna-13b-v1.5-16k.Q4_K_M.gguf"

## Download the model
print("Downloading model. This could take a while.")
model_path = hf_hub_download(model_name, filename=model_file)

with open("model_path.txt", "w") as f:
    f.write(model_path)

print(f"Downloaded and save model at {model_path}")