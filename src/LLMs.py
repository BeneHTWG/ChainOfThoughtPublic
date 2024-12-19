from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.conversation.base import ConversationChain
from langchain_core.output_parsers import BaseLLMOutputParser
from langchain_core.runnables.base import Runnable
from typing import Literal
import json

MODEL = Literal[
    "llama3-8b-8192",
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile"
]

class ConversationOutputPasser(BaseLLMOutputParser):
    def parse_result(self, result, *, partial = False):
        if type(output:=result[-1]) == ChatGeneration:
            return repr(output.message)
        else:
            return output.text

class LLMwithJsonStrOutput(Runnable):
    def __init__(self, llm:BaseChatModel):
        self.llm = llm
    
    def invoke(self, input:str, config=None, **kwargs):
        return json.dumps(self.llm.invoke(input, config, **kwargs), indent=4)
    
class LLMwithMemory(Runnable):
    def __init__(self, llm:BaseChatModel, memory_size:int=0, structured_output:bool=False):
        self.structured_output = structured_output
        self.conversation = ConversationChain(
            llm=LLMwithJsonStrOutput(llm) if structured_output else llm,
            memory=ConversationBufferWindowMemory(k=memory_size),
            output_parser=ConversationOutputPasser()
        )
    
    def invoke(self, input:str, config=None, **kwargs) -> AIMessage | dict:
        parse_output = json.loads if self.structured_output else eval
        return parse_output(self.conversation.predict(input=input))
    
    def reset_memory(self):
        self.conversation.memory.clear()

LLM_TYPE = Runnable[str, dict | BaseMessage] | LLMwithMemory

def init_llm(
    model:MODEL, 
    temperature:float=0.7,
    groq_api_key:str=None,
    structured_output=True, 
    memory_size:int=0
):
    assert groq_api_key is not None, "Groq API key must be provided,\nplease sign up at https://console.groq.com/login\n and generate a key at https://console.groq.com/keys"
    llm = ChatGroq(
        model=model,
        temperature=temperature,
        api_key=groq_api_key
    )
    if structured_output:
        llm = llm.with_structured_output(None, method="json_mode")
    if memory_size > 0:
        llm = LLMwithMemory(llm, memory_size, structured_output)
    return llm

