import streamlit as st
import sqlite3
import pandas as pd
import static


# Connecting to the database
conn = sqlite3.connect("db.db")
c = conn.cursor()


# Creating a Pandas Dataset from sql table
df = pd.read_sql_query("SELECT "+static.date+", "+static.vacancies+"FROM CTW", conn)


# Making dataset accessible from other pages
st.session_state["df"] = df


# Content of the home page
st.title("Critical TechWorks Porto vacancies analysis")
st.write("Hi! At the end of October 2022, I decided to make my life easier by automating the "
         "process of checking for new Critical Tech Works vacancies in the Porto region.")
st.write("So the next day, I wrote a simple program, that checked the CTW site every day, "
         "notifying me if the changes were done, and storing the results.")
st.write("As some time passed, I was invited to be a candidate for CTW Data Science academy, I decided to create my "
         "first project using iconic to myself data. In a very short time, the project grew to today's size.")
st.write("Hope you will have a nice time exploring it")
st.write("P.S. all the code is available on GitHub")
st.write("P.S.S. Streamlit (framework used for visualization) bugs a lot on mobile devices in vertical mode, "
         "I strongly recommend you flip the phone to the horizontal mode, or change to the PC")


st.title("Used tools:")
st.write("Pandas, Streamlit, Plotly, Requests, BeautifulSoup, Sqlite3, Host services, and more.")
st.write("The total amount of lines to make this work: 530")


# Adding links to the text
st.title("Links:")
st.markdown("[Telegram Chanel with notifications](%s)" % static.telegram)
st.markdown("[LinkedIn](%s)" % static.linked)
st.markdown("[GitHub](%s)" % static.git)


st.title("Disclaimer")
st.write("The project was created only for educational purposes, the author didn't mean to harm anybody in any mean. "
         "Requests to the site were limited to 1 per 24 hours to prevent the high load of CTW servers. ")
st.write("Due to these limitations, the stats might not show changes in the vacancy list that was true "
         "for less than 24 hours")
st.write("If actions of this program harm you, make you uncomfortable, or issue your performance -- contact me please "
         "using any available link from above, and I will fix the problem")
st.write("Thank you for your time, you can start discovering the project by selecting the "
         "next page in the menu on the left.")
