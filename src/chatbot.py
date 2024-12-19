from helper import StreamlitMessage as UIMessage, STREAMLIT_ROLE as ROLE
from typing import Callable
import streamlit as ui
from collections.abc import Mapping
from collections import deque
import json

# define function to display messages of variable types
def display_single(message, role:ROLE="user", run_in_terminal=False, append_to_session=True):
    if run_in_terminal:
        print(f"{role}: \n{message}")
        return
    if isinstance(message, Mapping):
        if type(message) == dict:
            message_str = json.dumps(message, indent=4)
        else:
            message_str = str(message)
        display_message = lambda: ui.json(message_str)
    else:
        display_message = lambda: ui.markdown(message)
    with ui.chat_message(role):
        display_message()
    if append_to_session:
        # Add message to chat array
        ui.session_state["messages"].append({"role": role, "content": message})
        
def display(message, role:ROLE="user", run_in_terminal=False, append_to_session=True):
    if isinstance(message, tuple) or isinstance(message, list):
        for m in message:
            if isinstance(m, UIMessage):
                m, role = m.content, m.role
            display_single(m, role, run_in_terminal, append_to_session)
    else:
        display_single(message, role, run_in_terminal, append_to_session)

def chatbot(
    generate_response:Callable[[str], tuple[UIMessage | Mapping | str] | UIMessage | Mapping | str], 
    intro:str="I am a chatbot",
    input_hint:str="Enter your message here",
    run_in_terminal=False,
    display_user_input=True,
    history_length=2
):
    if run_in_terminal:
        print(intro)
        while(True):
            prompt = input(input_hint + ": ")
            response = generate_response(prompt)
            display(response, "assistant", run_in_terminal)
    

    #define the assistants opening message
    Opening_message = ui.chat_message("assistant")
    Opening_message.write(intro)

    # Initialize empty chat array
    if "messages" not in ui.session_state:
        ui.session_state["messages"] = deque(maxlen=history_length)

    # Display previously sent chat messages
    for message in ui.session_state["messages"]:
        display(message["content"], message["role"], append_to_session=False)

    if prompt := ui.chat_input(input_hint):
        if display_user_input:
            display(prompt, "user")
        display(generate_response(prompt), "assistant")