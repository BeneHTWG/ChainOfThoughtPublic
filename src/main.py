from chatbot import chatbot
from LLMs import init_llm, MODEL
from helper import StreamlitMessage as UIMessage
from pathlib import Path
from streamlit.runtime.scriptrunner import get_script_run_ctx
    
PROMPTS = [
    "math_few_shot_DA",
    "math_few_shot_CoT",
    "math_zero_shot_implicit_CoT",
    "logic_zero_shot_DA",
    "logic_zero_shot_CoT",
    "logic_zero_shot_instructive_CoT"
]

def get_prompt_by_input(input:str):
    try:
        prompt_name = PROMPTS[int(input) - 1]
    except (ValueError, IndexError):
        raise ValueError("Invalid input")
    with open(Path("prompts") / f"{prompt_name}.txt") as f:
        return f.read()

def init_response_generator(model:MODEL, groq_api_key:str=None, memory_size:int=0, structured_output:bool=False):
    llm = init_llm(
        model, 
        groq_api_key=groq_api_key, 
        structured_output=structured_output,
        memory_size=memory_size,
        temperature=0.0
    )
    def generate_response(input:str):
        try:
            prompt = get_prompt_by_input(input)
        except ValueError:
            prompt = input
        return (
            UIMessage(prompt, "user"),
            UIMessage(llm.invoke(prompt).content, "assistant")
        )
    return generate_response
        

def main():
    generate_response = init_response_generator(
        model="llama3-8b-8192",
        groq_api_key=None,
        structured_output=False,
        memory_size=0
    )
    intro = "\n\n".join([
        "Enter an own prompt or choose a prompt from the following list in the form \"1\" / \"2\" etc.:",
        *[f"{i+1}. {prompt}" for i, prompt in enumerate(PROMPTS)]
    ])
    input_hint = "User Input"
    chatbot(
        generate_response,
        intro,
        input_hint,
        run_in_terminal=get_script_run_ctx() is None,
        display_user_input=False,
        history_length=2
    )

if __name__ == "__main__":
    main()