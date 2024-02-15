import logging
import numpy as np
from typing import List, Literal, TypedDict

from llama_cpp import Llama
import streamlit as st

from model_config import model_path, model_kwargs, generation_kwargs

from types import Role, Message

@st.cache_resource
def load_model():
    return Llama(model_path=model_path, **model_kwargs)

LOG_LEVEL = logging.INFO

SYS_PROMPT = """You are a mostly good natured assistant. You answer all
    questions asked by the user."""
app_logger = logging.getLogger()
app_logger.addHandler(logging.StreamHandler())
app_logger.setLevel(LOG_LEVEL)

moods = [
    "Happy",
    "Shy",
    "Angry",
    "Pirate-y"
]

def agree_response():
    resps = [
        "Gotta agree to the terms, slick",
        "Nope. See Agreement above.",
        "Agree to our terms, jack knuckle.",
        "Our lawyers make you click on the button up there first",
        "Just click the button dammit!"
    ]

    idx = np.random.randint(0, len(resps))
    return resps[idx]

def getmood() -> str:
    idx = np.random.randint(0, len(moods)-1)
    return moods[idx]

def generate_prompt_from_template(input):
    chat_prompt_template = f"""{input}"""
    return chat_prompt_template

def get_response(prompt):
    if len(st.session_state["messages"]) == 0:
        messages=[{"role":"user", "content":prompt}]
    else:
        messages = st.session_state["messages"] + [{"role":"user", "content":prompt}]
    res = st.session_state["llm"].create_completion(prompt, stream=True, **generation_kwargs)
    # res = st.session_state["llm"].create_chat_completion(
    #    messages=messages, stream=True, **generation_kwargs)
    return stream_result(res)

def stream_result(res):
    for token in res:
        app_logger.debug(token)
        yield token["choices"][0]["text"]

def main():
    if len(st.session_state) == 0:
        st.session_state["llm"] = load_model()
        st.session_state["messages"] = []
        st.session_state["messages"].append(Message(role="system", content=SYS_PROMPT))

    st.title("Welcome to NateChat!")
    st.caption("v0.0.0alpha")
    st.write("Terms of service: Use at your own risk. The developers of NateChat are not responsible for anything.")
    service_agree = st.radio(
        "Please agree to our terms of service before using.",
        ["Nope", "I agree"]
    )
    st.divider()
    st.sidebar.write("Controls to go here")

    c = st.container(height=450)


    for msg in st.session_state["messages"]:
        if msg["role"] != "system":
            c.chat_message(msg["role"]).write(msg["content"])

    if user_input := st.chat_input("Say something"):
        if user_input == "Happy birthday!":
            st.balloons()
        c.chat_message("user").write(user_input)
        prompt = generate_prompt_from_template(user_input)
        if service_agree == "I agree":
            with st.spinner("Thinking..."):
                res_stream = get_response(prompt)
            st.session_state["messages"].append(Message(role="user", content=user_input))
            msg = c.chat_message("assistant").write_stream(res_stream)
            st.session_state["messages"].append(Message(role="assistant", content=msg))
        else:
            msg = agree_response()
            c.chat_message("assistant").write(msg)
            st.session_state["messages"].append(Message(role="user", content=user_input))
            st.session_state["messages"].append(Message(role="assistant", content=msg))


if __name__ == "__main__":
    main()
