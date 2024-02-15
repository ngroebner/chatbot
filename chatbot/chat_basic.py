# Very basic chatbot with llms

# can make this selectablke with command line argument
model_path = '/Users/nate/.cache/huggingface/hub/models--TheBloke--Mixtral-8x7B-Instruct-v0.1-GGUF/snapshots/fa1d3835c5d45a3a74c0b68805fcdc133dba2b6a/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf'

import sys
from typing import List
from llama_cpp import Llama

from bot import Message, SYS_PROMPT_NATEBOT

from model_config import model_kwargs, generation_kwargs

SYS_PROMPT = SYS_PROMPT_NATEBOT

def exit(messages: List[Message]):
    response = input("Thanks for the chat! press Y if you want to see all of the messages, any other key to exit: ")
    if response.lower() == "y":
        print(messages)
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

def make_prompt(user_input: str, messages: List[Message]) -> str:
    # add system prompt and last 2 exchanges to prompt

    if len(messages) > 0:
        nmsgs = 4 if len(messages) >= 4 else 2
        last_messages = " ".join([format_message(msg) for msg in messages[-nmsgs:]])
    else:
        last_messages = ""
    prompt = "<s.\n" + SYS_PROMPT + last_messages
    prompt += f"[INST]user {user_input}[/INST]" + "</s>"
    # print(prompt)
    return prompt

if __name__ == "__main__":

    messages = []
    ## Instantiate model from downloaded file
    llm = Llama(model_path=model_path, **model_kwargs)

    print("Welcome to NateChat v0.0.0alpha")
    print("Type something at the prompt")
    print("You can input multiline prompts. A blank line ends your prompt")

    while True:
        print(">>>", end="")
        user_input = get_input()
        if user_input == "exit": exit(messages)

        prompt = make_prompt(user_input, messages)
        messages.append(Message(role="user", content=user_input))

        res = llm.create_completion(prompt, stream=True, **generation_kwargs)
        ai_output = []
        for token in res:
            for letter in token["choices"][0]["text"]:
                ai_output.append(letter)
                print(letter, end="")
        messages.append(Message(role="assistant", content="".join(ai_output)))
        print("\n")
