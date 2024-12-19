# ChainOfThought
chatbot for demonstrating the capabilities of Chain of Thought, enabling a selection of prompts containing different approaches and different tasks.

## Setup
create a virtual environment and install all dependencies:
```bash
python3 setup.py
```
activate the virtual environment:
```bash
source venv/bin/activate
```
get **API Key** to enable Usage of server based LLMs from **GroqCloud**
1. [sign up](https://console.groq.com/login)
2. [generate Key](https://console.groq.com/keys)
3. insert Key [here](https://github.com/BeneHTWG/ChainOfThoughtPublic/blob/main/src/main.py#L47)

## Running the Chatbot
in the Terminal:
```bash
python3 src/main.py
```
with Streamlit:
```bash
streamlit run src/main.py
```
### VS Code Addition
when using VS Code, streamlit can be run in Debugmode.
Therefore, add this configuration to `launch.json`:
```json
{
    "name": "Python:Streamlit",
    "type": "debugpy",
    "request": "launch",
    "module": "streamlit",
    "args": [
        "run",
        "src/main.py"
    ]
}
```

