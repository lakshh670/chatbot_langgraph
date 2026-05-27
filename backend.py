from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
load_dotenv()

llm=HuggingFaceEndpoint(repo_id='openai/gpt-oss-20b',task='text-generation')
model=ChatHuggingFace(llm=llm)

from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
def chat_node(state: ChatState):
    response=model.invoke(state['messages'])
    return {'messages':[response]}

from langgraph.graph import START,StateGraph,END
checkpointer=MemorySaver()
graph=StateGraph(ChatState)
graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)
chatbot=graph.compile(checkpointer=checkpointer)