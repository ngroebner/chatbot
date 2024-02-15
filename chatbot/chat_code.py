# Code generation bot

# can make this selectablke with command line argument
model_path = '/Users/nate/.cache/huggingface/hub/models--TheBloke--Mixtral-8x7B-Instruct-v0.1-GGUF/snapshots/fa1d3835c5d45a3a74c0b68805fcdc133dba2b6a/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf'

import logging
import json
import sys
from typing import List
from llama_cpp import Llama

from bot import Message, CodeResponse, SYS_PROMPT_CODE, parse_json

from model_config import model_kwargs, generation_kwargs

LOG_LEVEL = logging.INFO
logger = logging.Logger(__name__, level=LOG_LEVEL)

def exit():
    print("Thanks for using NateCode.")
    sys.exit()

def get_input() -> str:
    # Gets multiline input and returns it
    text =[]
    while True:
        prompt = input()
        if prompt == "": break
        elif prompt == "exit": return "exit"
        else: text.append(prompt)
    return "\n".join(text)

def format_message(msg: Message) -> str:
    return f"[INST] {msg['role']} {msg['content']} [/INST]"

def make_prompt(user_input: str) -> str:
    # add system prompt and user input
    prompt = "<>\n" + SYS_PROMPT_CODE
    prompt += f"User: {user_input}\n" + "Assistant: "
    # print(prompt)
    return prompt

def get_response(prompt: str, print_response=False) -> Message:
    res = llm.create_completion(prompt, stream=True, **generation_kwargs)
    ai_output = []
    for token in res:
        for letter in token["choices"][0]["text"]:
            ai_output.append(letter)
            if print_response: print(letter, end="")
    print("\n\n")
    return Message(role="assistant", content="".join(ai_output))

def execute(code):
    import tempfile
    import subprocess

    with open("code.py", "w") as f:
        f.write(code)

    retval = subprocess.run(
        ["python", "code.py"],
        capture_output=True, text=True
    )

    return retval

if __name__ == "__main__":

    ## Instantiate model from downloaded file
    llm = Llama(model_path=model_path, **model_kwargs)

    print("\nWelcome to NateCode v0.0.1alpha\n")
    print("Generates python code and runs it\n")
    print("You can input multiline prompts. A blank line ends your prompt\n\n")

    while True:
        print(">>>", end="")
        user_input = get_input()
        if user_input == "exit": exit()

        prompt = make_prompt(user_input)
        ai_output = get_response(prompt, print_response=False)
        try:
            output: CodeResponse = parse_json(ai_output)
            #try:
            code = output["code"]["main_code"]
            logger.info("type:", type(code))
            logger.debug(code)
            print("Code:\n")
            print(code, "\n")
            if output["language"].lower() == "python":
                print("Running generated code...\n")
                ret = execute(code)
                if ret.stderr != '':
                    print("Error in execution:")
                    print(ret.stderr)

                print("Result from program: \n")
                print(ret.stdout)
                print("\n")
            else:
                print(f"Code was generated in {output['language']}")
                print("Code not run, but saved to `code.py`")
        except json.decoder.JSONDecodeError as e:
            print("unable to parse answer, try again")

