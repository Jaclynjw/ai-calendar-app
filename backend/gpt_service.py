import db.database as mydb


from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 

from langchain.llms.openai import OpenAI 
from langchain.agents import AgentExecutor 
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool, BaseSQLDatabaseTool, InfoSQLDatabaseTool, ListSQLDatabaseTool, QuerySQLCheckerTool
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.agent_toolkits import create_sql_agent
from datetime import datetime
from langchain.tools import Tool
from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import create_openai_tools_agent
from langchain.agents.agent import AgentExecutor
from langchain_community.agent_toolkits import JsonToolkit
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage


# Define a new tool that returns the current datetime
datetime_tool = Tool(
    name="CURRENT_DATE",
    func=lambda x: datetime.now().isoformat(),
    description="Returns the current date",
)

# set up LLM
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(api_key = api_key, model = "gpt-3.5-turbo", temperature = 0)

# set up the agent
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True, extra_tools=[datetime_tool])
result = agent_executor.invoke(
    {
        "input": "What is LangSmith?"
    }
)
print(result)