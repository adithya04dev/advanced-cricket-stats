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

credentials_b64 = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
credentials_bytes = base64.b64decode(credentials_b64)
credentials_dict = json.loads(credentials_bytes)
credentials = service_account.Credentials.from_service_account_info(credentials_dict)

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# llm=ChatTogether(model="meta-llama/Llama-3-70b-chat-hf")
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



vector_store_files=''
for filename in os.listdir('./vector_store_files'):
    with open(os.path.join('./vector_store_files', filename), 'r') as file:
        filename=filename.replace('.txt','')
        vector_store_files+=(filename+": column")
        vector_store_files+='\n'
        vector_store_files+=file.read()
        vector_store_files+='\n'
with open("./schema.txt", "r") as file:
    schema=file.read()
prompt1="""

Columns and its values in database: {vector_store_files}.
Just try to store it as your context, i will be giving u some task based on this.

"""
query="""

You are an intelligent agent designed to assist in generating SQL queries based on user inputs. 
Users may provide   references to entity  names, such as player names, venues, or series names and some other columns in a cricket database.
You need to identify those  references and replace those names to their exact names in the database in processed query.

USE database TO accomplish the task.

Here are the steps you should follow:
1. Identify potential vague references in the user query that may correspond to any of the specified columns.
2.Search from the below names that are in database.
3.and return a json/dict with correct references in the database and also mention the column in which u found that refernce.
json format:
"references": [
"original": ,
"corrected": ,
"column":]



user query: {user_query}
Dont return SQL query return json with correct references.


"""
prompt2="""  
Imagine yourself as a sql assitant who writes sql code for calculating stats based on user query in a cricket database.
I have a ball by ball bigquery database named bbbdata.ballsnew_2406 of cricket matches..
Schema of Database: {schema}
User Query :  {user_query}
More info about correct refernces from userquery present in Database for where clause in sql: {res_gem}

THINK step by step..
use COMMON TABLE EXPRESSIONS IF NEEDED.
""" 
f_prompt1=prompt1.format(vector_store_files=vector_store_files,schema=schema)

history =None

chat =None 
# cache = caching.CachedContent.create(model="models/gemini-1.5-flash-001",display_name="database", system_instruction="You are a helpful assistant.",contents=[f_prompt1],ttl=timedelta(minutes=10),)
# model = genai.GenerativeModel.from_cached_content(cached_content=cache) 
n=0
model = genai.GenerativeModel('gemini-1.5-flash') 
chat_gemini = model.start_chat(history=[])

response = chat_gemini.send_message(f_prompt1)
def find_references(user_query):
    global history,chat
    global n,chat_gemini,model
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
    f_user_query=query.format(user_query=user_query)
    try:
        response = chat_gemini.send_message(f_user_query)
        
        print(f"Total Tokens = {model.count_tokens(chat_gemini.history)}")

    except Exception as e:
        # cache = caching.CachedContent.create(model="models/gemini-1.5-pro-001",display_name="database", system_instruction="You are a helpful assistant.",contents=[f_prompt1],ttl=timedelta(minutes=10),)
        # model = genai.GenerativeModel.from_cached_content(cached_content=cache) 
        pass

    res_gem+=response.text
    print(res_gem)
    res_gem+='\n\n'
    return {'response':res_gem,'query':user_query,'f':None}
with open("sample_codes.txt","r") as f:
  sample_codes=f.read()

task=""" Imagine yourself as sql assitant who writes sql code for calculating stats based on user query in a cricket database.
I have a ball by ball bigquery database named bbbdata.ballsnew_2406 of cricket matches..
Schema of Database:
{schema}
Some of sample queries using this database are :{sample_codes}
Write SQL QUERY for :
User Query :  {user_query}
More info about correct refernces from userquery present in Datbase: {res_gem}. use only this to filter dataset i.e in where of sql..

Suggestions:
1.Use \ as delimeter before ' is present in sql query.

Think step by step and return sql query that can be executed.
 """


llm2 = ChatOpenAI(model='gpt-4o-mini')
critique = """
User Query: {user_query}

Generated SQL Query: {sql_query}

Database Schema: {schema}

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
    n+=1
    if n>4:
        remarks="Cannot be processed further. Simplify the Quey and try again."
    if type(f)==pandas.core.frame.DataFrame:
       return [remarks,f]
    if f==None:
      f_user_query=task.format(user_query=user_query,res_gem=res_gem,schema=schema,sample_codes=sample_codes)
      res=chat.invoke({"input": f_user_query},{"configurable": {"session_id": "unused"}},)
      
      
    else:
       if type(f)!=pandas.core.frame.DataFrame:
          res=chat.invoke({"input": f"this error occurred{f}. Please try again and only provide rectified sql query"},{"configurable": {"session_id": "unused"}},)
    critique=critique.format(user_query=user_query,sql_query=res.content,schema=schema)
    res=llm2.invoke(critique)
    result=res.content  
    sql_query = result.split('```')[-2].strip()
    sql_query=sql_query.replace('sql',' ')
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
