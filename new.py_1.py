#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
from tempfile import NamedTemporaryFile
from flask import Flask, request, render_template
#from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from langchain.llms import OpenAI
from langchain.agents import create_csv_agent
#from dotenv import load_dotenv
from werkzeug.utils import secure_filename
#from utils import json_csv
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
import pyodbc
import pandas as pd


# In[10]:


import urllib


# In[18]:


def create():        #function to create sql agent, create_sql_agent  
  server = 'uid.database.windows.net' #tcp:peearz.database.windows.net,1433
  database = 'FuelData'
  username = 'password@host.database.windows.net' 
  password = 'Password'

  #Create the connection string
  conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
  )
  #conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

  conn=pyodbc.connect(conn_str)#specify odbc driver17
  
  #db = SQLDatabase(connection_string=conn_str)
  db = SQLDatabase.from_uri(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")
  llm = OpenAI(openai_api_key="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",temperature=0)  #main component
  toolkit = SQLDatabaseToolkit(db=db, llm=llm)


  agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #top_k=10000
  )

  return agent
agent=create()


# In[24]:





#query="What is the total fuel quantity on 23-Jul-2022 between 09:30 P.M. and 10:03 P.M.?" #wrong mathematical calculation 1216.01
query="How many records in the table?"
#query="What is the total fuel cost for 22-Jul-2022?" #zero because checking for fuel date==, not 'like'

#query="How many records on 22-Jul-2022, ignoring time?" #incorrect

#query="What is the total fuel quantity on 22-Jul-2022?" #0, not able to give answer since there is no time concatenation

#query="What is the total fuel quantity on 22-Jul-2022 between 9:49 P.M. and 10:03 P.M.?" #Correct

#query="Which receiver_name took maximum fuel during the first 10 days of July 2022 ignoring time?" #wrong

#query="Which receiver_name took maximum fuel during the first 12 days of July 2022?" #Alok?

#query="Ignoring time, what is the total fuel quantity for the month of July?"

#query="What is the total fuel_qnty on vehicle_name Tipper - BOX in the month of July 2022 ignoring time and answer rounded by last two digits?" #106409.90

response=agent.run(query)

#agent.toolkit.database_connection.close()

print(response)


# In[ ]:




