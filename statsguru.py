import os
import pandas
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_together import ChatTogether
import pandas as pd
from google.cloud import bigquery
from google.generativeai import caching
import google.generativeai as genai
from  datetime import timedelta
import time 
import os
import time
import shutil
from pathlib import Path
from datetime import datetime
import langgraph
from langgraph.graph import Graph
from langgraph.graph import END
import streamlit as st 
from google.cloud import bigquery
import base64
import json
import google.auth
from google.oauth2 import service_account
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.tools import tool
#import propmt template,agent executor,react agent
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent

from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
import requests 
import re
import ast




credentials_b64 = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
credentials_bytes = base64.b64decode(credentials_b64)
credentials_dict = json.loads(credentials_bytes)
credentials = service_account.Credentials.from_service_account_info(credentials_dict)

API_KEY = os.environ['edge_api_key']
URL = "https://api.bing.microsoft.com/v7.0/search"
HEADERS = {"Ocp-Apim-Subscription-Key": API_KEY}

llm=ChatOpenAI(model='gpt-4o-mini')
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt | llm
with open("./schema.txt", "r") as file:
    schema=file.read()

prompt2="""  
Imagine yourself as a sql assitant who writes sql code for calculating stats based on user query in a cricket database.
I have a ball by ball bigquery database named bbbdata.ballsnew_2406 of cricket matches..
Schema of Database: {schema}
User Query :  {user_query}
More info about correct refernces from userquery present in Database for where clause in sql: {res_gem}

THINK step by step..
use COMMON TABLE EXPRESSIONS IF NEEDED.
""" 

history =None

chat =None 
n=0


def find_references(user_query,model='gpt-4o-mini',stream=True):
    global history,chat
    global n
    n=0
    history=ChatMessageHistory()
    chat = RunnableWithMessageHistory(
        chain,
        lambda session_id: history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    


    res_gem=user_query
    res_gem+='\n'
    ti=time.time()
    if model=='sonnet':
        llm = ChatAnthropic(temperature=0, model_name="claude-3-sonnet-20240229")
    elif model =='gpt-4o-mini':
        llm = ChatOpenAI(model="gpt-4o-mini")
    # elif model=='gemini':
    #     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    else:
        llm = ChatGroq(model='llama-3.1-70b-versatile')  
  
    @tool
    def get_value_from_column(list1:str) -> str:
        """
        This function retrieves the specific value present in database column_name that is most similar to the search_value.
        input: 2D list of lists  with the format shown below.
        ([[column_name1,search_value1], [column_name2,search_value2], [column_name3,search_value3]]

        """
        def get_value_from_column1(list1:list) -> str:



            column_name=list1[0]
            search_value=list1[1]
            if column_name not in ['venue', 'series_name',  'tournament_name',   'match_type',  'team_bat',  'team_bowl',  
            'bowler_type', 'batter','bowler', 'bowler_kind','batter_hand']:
                return """Can only  search for this columns ['venue', 'series_name',  'tournament_name',   'match_type',  'team_bat',  'team_bowl',  
            'bowler_type', 'batter','bowler', 'bowler_kind','batter_hand']  in database"""
            if column_name=='batter' or column_name=='bowler':
                API_KEY = "3d1d6539895b4ec18c0adc1633fce5f3"
                URL = "https://api.bing.microsoft.com/v7.0/search"

                HEADERS = {"Ocp-Apim-Subscription-Key": API_KEY}
                PARAMS = {
                    "q": search_value + ' cricinfo ',
                    "count": 10,
                    "offset": 0,
                    "mkt": "en-US",
                    "safeSearch": "Moderate"
                }

                response = requests.get(URL, headers=HEADERS, params=PARAMS)
                results = response.json()
                flag = False

                for result in results["webPages"]["value"]:
                    url = result["url"]
                    if 'https://www.espncricinfo.com/cricketers/' in url:
                        flag = True
                        break

                if flag is False:
                    return "Player not found Leave this column's value  empty."

                parts = url.split("-")
                id = parts[-1]
                res = requests.get('http://core.espnuk.org/v2/sports/cricket/athletes/' + str(id))
                name = res.json()['displayName']
                return str(name)
            else:

            # Load FAISS index for specified column
                embeddings = OpenAIEmbeddings(
                    model='text-embedding-ada-002'
                )
                db = FAISS.load_local(fr"C:\Users\adith\Documents\Projects\python-projects\cric_metric_clone\vector_databases\{column_name}", embeddings, allow_dangerous_deserialization=True)

                # Create document retriever and find most relevant document to player name
                retriever = db.as_retriever(search_type='mmr', search_kwargs={'k': 5, 'lambda_mult': 1})
                matched_value = retriever.get_relevant_documents(search_value)
                res=[]
                for i in matched_value:
                    res.append(i.page_content)
                return str(res)

        # print(type(list1))
        # print(list1)


        list_str = re.search(r'\[.*\]', list1)
        if list_str:
            list_str = list_str.group()
        else:
            return "Invalid input format: No list found"
        list1 = ast.literal_eval(list_str)
        # list1 = eval(list_str)
        # list1=eval(list1)

        # print(type(list1))
        # print(list1)
        l=[]
        for list2 in list1:
            if len(list2)!=2:
                print("list2",list2)
                return "Inputs are not in correct format."
                
            res=get_value_from_column1(list2)
            l.append(list2+[res])
        print(l)
        return l 
        
    @tool
    def add_2_numbers(a,b) :
        """ 
        This function adds 2 numbers.
      """
        return a+b
        

    tools = [get_value_from_column,add_2_numbers]
    system_prompt=""" 
   You are an helpful assistant.

    """
    user_prompt=f"""   
    User Query: "{user_query}"
    -
    Finally you need to return the final answer with correct column names and values that are present in the database.
    Thats why,you need  to preprocess these user queries by seraching in the database using the tool get_value_from_column
    and then return the final answer.

    


    Some of the important columns,and its values in the database are:
    - venue : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - series_name : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - tournament_name : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - team_bat : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - team_bowl : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - batter : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - bowler : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - bowler_kind: ['pace bowler','spin bowler'] (you may need not search in database for this columns,values as they are only few)
    - batter_hand :['Right Hand Batter','Left Hand Batter'] (you may need not search in database for this columns,values as they are only few)
    - match_type : ['ODI','MDM','Test','IT20','T20','ODM'] (you may need not search in database for this columns,values as they are only few)

    - bowler_type : ['RAP'(abbreviated for right arm pace),'OB'(abbreviated for off break),'LWS'(abbreviated for left wrist spin),
    'LAP'(abbreviated for left arm pace),'LB'(abbreviated for left arm break),'SLA'(abbreviated for slow left arm)
    ] (you may need not search in database for this columns,values as they are only few)

    -another point is that tournament_name consists of  name of series,event..
    but the seriesname consists of tournamanet_name+Season  of the series/event..
      for example:tournament_namecan be :IPL ,series_name:IPL 2024 season: 2024
    thus for query involving just the name of event you can use directly the tournament_name,if specifically
    mentioned the event/tournament with a season/year you can use series_name.







    """
    MEMORY_KEY = "chat_history"
    # prompt for tool calling agent
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", "you're a helpful assistant"), 
    #     ("human", "{input}"), 
    #     ("placeholder", "{agent_scratchpad}"),
    # ])  
    prompt= PromptTemplate.from_template(
"""

You are an intelligent agent designed to assist in generating SQL queries by processing  based on user query.


You will be given a user query,in which users may provide vague references to entity names, such as batter,bowler,bowler_type,
batter_hand,bowler_kind,match_type,team_bat,team_bowl,tournament_name,series_name,venue in a cricket database,
but directly using those names/values of that column in SQL query may not work always,so you need to search for the exact name 
of the  in the database using the tool get_value_from_column ( except for bowler_kind,batter_hand,match_type which have only f
ew values and i have provided below  you with the list of those values).



Thus you need  to preprocess these user queries by searching in the database using the tool get_value_from_column and 
then return the final answer.


Remember:
-Even if in the query users mentioned other columns other than the ones mentioned above,you need to ignore them.    



Important  info about databse
    Some of the important columns,and its values in the database are:
    - venue : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - series_name : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - tournament_name : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - team_bat : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - team_bowl : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - batter : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - bowler : many values are present in this column, so you may need to search in database using a function that is mentioned below.
    - bowler_kind: ['pace bowler','spin bowler'] (you may need not search in database for this columns,values as they are only few)
    - batter_hand :['Right Hand Batter','Left Hand Batter'] (you may need not search in database for this columns,values as they are only few)
    - match_type : ['ODI','MDM','Test','IT20','T20','ODM'] (you may need not search in database for this columns,values as they are only few)

    - bowler_type : ['RAP'(abbreviated for right arm pace),'OB'(abbreviated for off break),'LWS'(abbreviated for left wrist spin),
    'LAP'(abbreviated for left arm pace),'LB'(abbreviated for left arm break),'SLA'(abbreviated for slow left arm)
    ] (you may need not search in database for this columns,values as they are only few)

    -another point is that tournament_name consists of  name of series,event..
    but the seriesname consists of tournamanet_name+Season  of the series/event..
      for example:tournament_namecan be :IPL ,series_name:IPL 2024 season: 2024
    thus for query involving just the name of event you can use directly the tournament_name,if specifically
    mentioned the event/tournament with a season/year you can use series_name.


---------------------
You have access to the following tools:

{tools}
---
Tool names:
{tool_names}
---------------------------------------------------------------------------------------------------

Use the following format:

User Query: {input}

Thought: Analyze the user query and determine what information needs to be retrieved from the database. 
Consider which columns are relevant and what search terms to use.

Action: get_value_from_column

Action Input: [['column_name1', 'search_value1'],['column_name2', 'search_value2'], ...].

Observation: Review the results returned by the action. 
These are the most similar values found in the database for the given search terms.

(Repeat the Thought/Action/Action Input/Observation steps N times, but dont repeat the same action again and again)

Thought: Analyze the observations from all actions. 
Determine which results are most relevant and accurate for answering the user query. 
Consider any discrepancies or ambiguities in the data.

Final Answer: Provide a concise response to the user query, including:
-The relevant column names,appropriate values based on results of actions found for each column. from the database.
But Dont include  sql query.
Begin!

User Query: {input}
Thought: {agent_scratchpad}


"""
    )


    chat_history = []
    # prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)    
    # agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    try:
        # result=agent_executor.invoke({"input": user_prompt})

        result=agent_executor.invoke({"input": user_query})
    except Exception as e:
        # print(e)
        n=404
        return {"response":str(e),"query":user_query,"f":None}
    res_gem+=result['output']
    # print("Response: ",res_gem)
    print("Time Taken for gpt-4o-mini = ",time.time()-ti)
    
    res_gem+='\n\n'
    return {'response':res_gem,'query':user_query,'f':None}

with open("sample_codes.txt","r") as f:
  sample_codes=f.read()

task=""" Imagine yourself as sql assitant who writes sql code for calculating stats based on user query in a cricket database.
I have a ball by ball bigquery database named bbbdata.ballsnew_2406 of cricket matches..
Schema and info about columns of  Database:
{schema}
Some of sample queries using this database are :{sample_codes}
Write SQL QUERY for :
User Query :  {user_query}
More info about correct refernces from userquery present in Datbase: {res_gem}. 
Use only this to filter dataset i.e in where of sql..

Suggestions:
1.Use backslash as delimeter before ' is present in sql query.

Think step by step and return sql query that can be executed.
 """


critique = """
User Query: {user_query}

Generated SQL Query: {sql_query}

Schema and info about columns of  Database:

Please critique the generated SQL query for any errors or inefficiencies. 

Think Step by Step.
Finally Provide a corrected and Modified  SQL query:.
"""
def coding(json_data):
    res_gem=json_data['response']
    user_query=json_data['query']
    f=json_data['f']
    remarks=user_query
    global n,critique
    llm2 = ChatOpenAI(model='gpt-4o-mini')
    ti=time.time()
    n+=1
    if n>4:
        remarks="Cannot be processed further. Simplify the Quey and try again."
    if n==404:
        remarks=res_gem
    if type(f)==pandas.core.frame.DataFrame:
       return [remarks,f]
    if f==None:
      f_user_query=task.format(user_query=user_query,res_gem=res_gem,schema=schema,sample_codes=sample_codes)
      res=chat.invoke({"input": f_user_query},{"configurable": {"session_id": "unused"}},)
      
      
    else:
       if type(f)!=pandas.core.frame.DataFrame:
          res=chat.invoke({"input": f"this error occurred{f}. Please try again and only provide rectified sql query"},{"configurable": {"session_id": "unused"}},)
    # critique=critique.format(user_query=user_query,sql_query=res.content,schema=schema)
    # res=llm2.invoke(critique)
    print(f"time taken for sql query generation {time.time()-ti}") 
    result=res.content  
    sql_query = result.split('```')[-2].strip()
    sql_query=sql_query.replace('sql',' ')

    print(f"sql query generated for {n}th iteration :",sql_query)



    return [sql_query,f]
def router(inp):
    global n
    if type(inp[1])==pandas.core.frame.DataFrame or n>4:
        return "exit"
    else:
        return "run"
def query_to_dataframe(queryl):
    project_id = 'adept-cosine-420005'
    query=queryl[0]
    client = bigquery.Client(project=project_id,credentials=credentials)
    try:
        query_job = client.query(query)
        query_job.result()
        df = query_job.to_dataframe()
    except Exception as e:
        return { "response": "error","query":"adi", "f": str(e) }
        # return "a","a",e
    return { "response": "success","query":query, "f": df }


#graph building


workflow = Graph()

workflow.add_node("find_references", find_references)
workflow.add_node("coding", coding)
workflow.add_node("query_to_dataframe", query_to_dataframe)

workflow.add_conditional_edges(
    "coding",
    router,
    {
        "exit": END,
        "run": "query_to_dataframe",
    },
)

workflow.add_edge('find_references', 'coding')

workflow.add_edge('query_to_dataframe', 'coding')

workflow.set_entry_point("find_references")



def ask(question):
    app = workflow.compile()
    response=app.invoke(question)
    remarks=response[0]
    df=response[1]
    if remarks=="Cannot be processed further. Simplify the Quey and try again.":
        st.write(remarks)
    else:
        #show the dataframe
        st.write(df)
