import streamlit as st
import sqlite3
import pandas as pd
from .. import static


# Connecting to the database
conn = sqlite3.connect("db.db")
c = conn.cursor()


# Creating a Pandas Dataset from sql table
df = pd.read_sql_query("SELECT "+static.date+", "+static.vacancies+"FROM CTW", conn)


c.execute("SELECT Date FROM CTW")
dates = c.fetchall()
st.title("Amount of days researched: " + str(len(dates)))


st.title("Here is how I collect the data:")
st.markdown("""
Every day an automated program sends a GET request to the https://join.criticaltechworks.com/jobs?location=Porto&query=
, and receives raw HTML of the site. 

Program checks if the answer from the site was correct, and processes HTML by searching for 
all elements of a certain class. 

On exit from this process, we receive a list of all vacancies. 
The program splits them, sorts them, and adds them to the SQL table.

Then the data processes into something bigger, that's described in detail""" " [here](%s)" % "/Stats_Creation")


st.title("Here is the exit data from this part of the program:")

st.write(df)
