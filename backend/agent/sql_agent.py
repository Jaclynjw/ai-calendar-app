#refer to https://github.com/HamzaG737/rappel-conso-chat-app/blob/main/sql_agent/agent.py

from langchain.agents.agent_toolkits import SQLDatabaseToolkit

from langchain.agents.agent_types import AgentType
from langchain.agents import create_sql_agent
from langchain.memory import ConversationBufferMemory
from agent.utils import get_chat_openai, get_db
from agent.few_shot_prompt import get_full_prompt

from langchain.tools import Tool
from datetime import datetime


db = get_db()
llm = get_chat_openai("gpt-3.5-turbo")

def get_sql_toolkit(tool_llm_name: str):
    """
    Get the SQL toolkit for a given tool LLM name.

    Parameters:
        tool_llm_name (str): The name of the tool LLM.

    Returns:
        SQLDatabaseToolkit: The SQL toolkit object.
    """
    llm_tool = get_chat_openai(model_name=tool_llm_name)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm_tool)
    return toolkit


def get_agent_llm(agent_llm_name: str):
    """
    Retrieves the LLM agent with the specified name.

    Parameters:
        agent_llm_name (str): The name of the LLM agent.

    Returns:
        llm_agent: The LLM agent object.
    """
    llm_agent = get_chat_openai(model_name=agent_llm_name)
    return llm_agent

datetime_tool = Tool(
    name="CURRENT_DATE",
    func=lambda x: datetime.now().isoformat(),
    description="Returns the current date",
)


def create_agent(
    # tool_llm_name: str = "gpt-4-1106-preview",
    agent_llm_name: str = "gpt-4-1106-preview",
    #tool_llm_name: str = "gpt-4-1106-preview",
    #agent_llm_name: str = "gpt-3.5-turbo",
):
    """
    Creates a SQL agent using the specified tool and agent LLM names.

    Args:
        tool_llm_name (str, optional): The name of the SQL toolkit LLM. Defaults to "gpt-4-1106-preview".
        agent_llm_name (str, optional): The name of the agent LLM. Defaults to "gpt-4-1106-preview".

    Returns:
        agent: The created SQL agent.
    """

    llm_agent = get_agent_llm(agent_llm_name)
    memory = ConversationBufferMemory(memory_key="history", input_key="input")

    agent = create_sql_agent(
        llm=llm_agent,
        db=db,
        agent_type='openai-tools',
        input_variables=["input", "agent_scratchpad", "history"],
        prompt=get_full_prompt(),
        agent_executor_kwargs={"memory": memory},
        extra_tools=[datetime_tool],
        verbose=True,
    )
    return agent

# agent = create_agent()
# # res = agent.invoke({"input": "Add a new event titled 'CEO's Birthday Party' on 2024-05-07."})
# res = agent.invoke({"input": "Do I have any events today?"})
# print(res)