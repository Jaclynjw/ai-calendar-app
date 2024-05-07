from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)




def get_full_prompt():
    examples = [
        {"input": "List all upcoming events.", "query": "SELECT * FROM events WHERE start_time > CURRENT_TIMESTAMP;"},
        {
            "input": "Find all events scheduled at 'Conference Room A'.",
            "query": "SELECT * FROM events WHERE location = 'Conference Room A';",
        },
        {
            "input": "Show events happening today.",
            "query": "SELECT * FROM events WHERE DATE(start_time) = CURRENT_DATE;",
        },
        {
            "input": "List all events in the 'Workshop' category.",
            "query": "SELECT * FROM events WHERE category = 'Workshop';",
        },
        {
            "input": "What is the duration of the event titled 'Annual Review'?",
            "query": "SELECT end_time - start_time FROM events WHERE title = 'Annual Review';",
        },
        {
            "input": "How many events are there this month?",
            "query": "SELECT COUNT(*) FROM events WHERE EXTRACT(MONTH FROM start_time) = EXTRACT(MONTH FROM CURRENT_DATE);",
        },
        {
            "input": "Find all events with 'Training' in their description.",
            "query": "SELECT * FROM events WHERE description LIKE '%Training%';",
        },
        {
            "input": "List events that start after 5 PM today.",
            "query": "SELECT * FROM events WHERE DATE(start_time) = CURRENT_DATE AND EXTRACT(HOUR FROM start_time) >= 17;",
        },
        {
            "input": "Which events last longer than 2 hours?",
            "query": "SELECT * FROM events WHERE end_time - start_time > INTERVAL '2 hours';",
        },
        {
            "input": "Add a new event called 'Team Meeting' on April 10th from 10 AM to 11 AM at 'Board Room' with the description 'Quarterly Planning'.",
            "query": "INSERT INTO events (title, start_time, end_time, location, description) VALUES ('Team Meeting', '2024-04-10 10:00:00', '2024-04-10 11:00:00', 'Board Room', 'Quarterly Planning');",
        },
        {
            "input": "Delete the event titled 'Project X Presentation'.",
            "query": "DELETE FROM events WHERE title = 'Project X Presentation';",
        },
        {
            "input": "Change the location of the 'Annual General Meeting' to 'Conference Room B'.",
            "query": "UPDATE events SET location = 'Conference Room B' WHERE title = 'Annual General Meeting';",
        },
        {
            "input": "Extend the end time of the 'Tech Workshop' on June 5th by two hours.",
            "query": "UPDATE events SET end_time = end_time + INTERVAL '2 hours' WHERE title = 'Tech Workshop' AND DATE(start_time) = '2024-06-05';",
        },
        {
            "input": "Cancel all events scheduled for May 1st.",
            "query": "DELETE FROM events WHERE DATE(start_time) = '2024-05-01';",
        },
        {
            "input": "Add a new category 'Private' to the event titled 'CEO's Birthday Party'.",
            "query": "UPDATE events SET category = 'Private' WHERE title = 'CEO''s Birthday Party';",
        },
        {
            "input": "Schedule a meeting with Sam tomorrow from 6 to 9 PM.",
            "query": "INSERT INTO events (title, start_time, end_time, description) VALUES ('Meeting with Sam', DATE 'tomorrow' + TIME '18:00:00', DATE 'tomorrow' + TIME '21:00:00', 'Discuss project updates.');"
        },
        {
        "input": "I want to pass the exam before 2024-06-07, break down the study plan for me.",
        "query": [
            "INSERT INTO events (title, start_time, end_time, description) VALUES ('Study Chapter 1', '2024-05-10 09:00:00', '2024-05-10 11:00:00', 'Study Chapter 1 of the textbook.');",
            "INSERT INTO events (title, start_time, end_time, description) VALUES ('Review Past Papers', '2024-05-15 09:00:00', '2024-05-15 11:00:00', 'Review past exam papers.');",
            "INSERT INTO events (title, start_time, end_time, description) VALUES ('Study Chapter 2', '2024-05-20 09:00:00', '2024-05-20 11:00:00', 'Study Chapter 2 of the textbook.');",
            "INSERT INTO events (title, start_time, end_time, description) VALUES ('Mock Exam', '2024-06-01 09:00:00', '2024-06-01 12:00:00', 'Take a mock exam to assess readiness.');"
        ]
    },
    {
        "input": "I want to lose weight for 10 kg in a month, make a workout plan for me.",
        "query": [
            "INSERT INTO events (title, start_time, end_time, description) VALUES ('Morning Cardio', '2024-05-01 07:00:00', '2024-05-01 08:00:00', '30 minutes of running.');",
            "INSERT INTO events (title, start_time, end_time, description) VALUES ('Gym Session', '2024-05-02 18:00:00', '2024-05-02 19:30:00', 'Strength training at the gym.');",
            "INSERT INTO events (title, start_time, end_time, description) VALUES ('Yoga Class', '2024-05-04 08:00:00', '2024-05-04 09:00:00', 'Attend a yoga class for flexibility.');",
            "INSERT INTO events (title, start_time, end_time, description) VALUES ('Cycling', '2024-05-06 07:00:00', '2024-05-06 08:00:00', 'One hour of cycling for cardio.');"
        ]
    },
    ]


    system_prefix = """You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    You can make DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database if the user asks for it, but be careful and double check the query before executing it.
    When inserting data, make sure the title, start_time, and end_time columns are not empty.

    When the user mentions "schedule a meeting", "add an event", "make an appointment", "book a meeting", "create an event", "schedule a meeting with", "add a meeting", "make an appointment with", "book a meeting with", "create an event with", "schedule a ", "add a ", "make an ", "book a ", or similar phrases, you should insert a new event into the 'events' table.
    
    Here are some examples of user inputs and their corresponding SQL queries:"""

    CUSTOM_SUFFIX = """Begin!

    Relevant pieces of previous conversation:
    {history}
    (Note: Only reference this information if it is relevant to the current query.)

    Question: {input}
    Thought Process: My primary task is to ensure accuracy and safety in executing SQL queries based on the user's natural language instructions.
    I will double-check each SQL query against the schema of the 'events' table. 

    I must not fabricate information and should double check each query against the database schema. 
    If the user's request does not match any records in the 'events' table, I will respond with "No records found."
    If the question is unrelated to the database, I will respond with common sense and knowledge, the response should start with "This question is not related to the database, but based on common knowledge, ...". 
    For correct understanding and response, I will rely on detailed knowledge of the table's structure and the purpose of each column. 
    I will confirm the columns involved in the query and avoid executing commands on non-existent columns. 

    SQL Query: Construct the appropriate SQL query here.
    SQL Execution Check: Double-check the correctness and security of the SQL before execution.
    SQL Result: Result of the SQLQuery
    Answer: If the query is related to the database, provide the data. If not, answer using general knowledge as specified.

    {agent_scratchpad}
    """

    example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
    )

    few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k"],
    prefix=system_prefix,
    suffix=CUSTOM_SUFFIX,
    )

    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    return full_prompt