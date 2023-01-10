import streamlit as st
import plotly_express as px
import sqlite3
import pandas as pd
import datetime
from collections import Counter
from .. import static


conn = sqlite3.connect("db.db")
c = conn.cursor()


st.title("Distribution of the most common words in vacancy titles")
df3 = pd.read_sql_query("SELECT "+static.date+" FROM CTW", conn)
select_date_type = st.selectbox("Select type of the statistics range", options=["All Time",
                                                                                "Selected Date",
                                                                                "Date Range"])


def blank_space():
    st.title(" ")
    st.title(" ")
    st.title(" ")
    st.title(" ")


# Creating and showing data for analysing titles of vacancies for 1 day
def one_day(counter):
    c.execute("SELECT MIN("+static.date+") FROM CTW")
    min_date = c.fetchone()
    c.execute("SELECT MAX("+static.date+") FROM CTW")
    max_date = c.fetchone()
    min_date = datetime.date(int(min_date[0][:4:]), int(min_date[0][5:7:]), int(min_date[0][8:10:]))
    max_date = datetime.date(int(max_date[0][:4:]), int(max_date[0][5:7:]), int(max_date[0][8:10:]))
    select_date = st.date_input("Select a date", min_value=min_date, max_value=max_date)

    numbers = []
    for i in range(10, 51):
        numbers.append(str(i))
    select_amount_of_pie_groups = st.selectbox("Select amount of words in the chart", options=numbers)

    c.execute("SELECT "+static.vacancies+" FROM CTW WHERE "+static.date+"='"+str(select_date)+"'")
    data_set = c.fetchall()[0][0]

    split_it = data_set.split()
    coun = counter(split_it)
    most_occur = coun.most_common(int(select_amount_of_pie_groups))

    df2 = pd.DataFrame(most_occur, columns=["Word", "Reps"])

    fig2 = px.pie(df2, values='Reps', names='Word')
    st.write(fig2)


# Creating and showing data for analysing titles of vacancies of all time
def all_range():

    numbers = []
    for i in range(10, 51):
        numbers.append(str(i))
    select_amount_of_pie_groups = st.selectbox("Select amount of words in the chart", options=numbers)
    c.execute("SELECT "+static.vacancies+" FROM CTW")
    data_set = c.fetchall()
    q = []
    for i in range(0, len(data_set)):
        q.append(data_set[i][0])

    data_set = " ".join(q)
    split_it = data_set.split()
    coun = Counter(split_it)
    most_occur = coun.most_common(int(select_amount_of_pie_groups))

    df2 = pd.DataFrame(most_occur, columns=["Word", "Reps"])
    fig2 = px.pie(df2, values='Reps', names='Word')
    st.write(fig2)


# Creating data and visualization for daya in selected range
def dates_range(Counter):
    c.execute("SELECT MIN("+static.date+") FROM CTW")
    min_date = c.fetchone()
    c.execute("SELECT MAX("+static.date+") FROM CTW")
    max_date = c.fetchone()
    min_date = datetime.date(int(min_date[0][:4:]), int(min_date[0][5:7:]), int(min_date[0][8:10:]))
    max_date = datetime.date(int(max_date[0][:4:]), int(max_date[0][5:7:]), int(max_date[0][8:10:]))
    select_date = st.date_input("Select a start date", min_value=min_date, max_value=max_date)

    if select_date != max_date:
        select_date2 = st.date_input("Select a finish date", min_value=select_date, max_value=max_date)

        numbers = []
        for i in range(10, 51):
            numbers.append(str(i))
        select_amount_of_pie_groups = st.selectbox("Select amount of words in the chart", options=numbers)

        final_data = []
        searching_date = select_date
        while True:
            c.execute("SELECT "+static.vacancies+" FROM CTW WHERE "+static.date+"='"+str(searching_date)+"'")
            final_data.append(c.fetchall()[0][0])
            c.execute("SELECT "+static.date+" FROM CTW WHERE "+static.date+"='" + str(searching_date) + "'")
            if str(c.fetchall()[0][0]) == str(select_date2):
                break
            searching_date = str(searching_date)
            searching_date = datetime.date(
                int(searching_date[:4:]),
                int(searching_date[5:7:]),
                int(searching_date[8:10:])) + datetime.timedelta(days=1)

        data_set = "".join(final_data)
        split_it = data_set.split()
        coun = Counter(split_it)
        most_occur = coun.most_common(int(select_amount_of_pie_groups))

        df2 = pd.DataFrame(most_occur, columns=["Word", "Reps"])
        fig2 = px.pie(df2, values='Reps', names='Word')
        st.write(fig2)
        final_data.clear()
    else:
        blank_space()
        blank_space()
        blank_space()


# Some logic for frontend
if select_date_type == "Selected Date":
    one_day(Counter)
elif select_date_type == "All Time":
    all_range()
elif select_date_type == "Date Range":
    dates_range(Counter)


# Creating df for vacancy count change histogram
df_count_list = []
df_5_list = []
added = []
deleted_list = []
df_6_list = []
c.execute("SELECT "+static.date+" FROM CTW")
first_date = c.fetchall()
date = first_date[1][0]
total_new = 0
total_deleted = 0
amount_of_rows = first_date
date = datetime.date(int(date[:4:]), int(date[5:7:]), int(date[8:10:]))
c.execute("SELECT "+static.vacancies+" FROM CTW WHERE "+static.date+" = '"+str(date)+"'")

for i in range(0, len(amount_of_rows)):
    try:
        yesterday = date - datetime.timedelta(days=1)
        new = 0
        deleted = 0
        c.execute("SELECT "+static.vacancies+" FROM CTW WHERE "+static.date+" = '"+str(date)+"'")
        vacs = c.fetchall()[0][0]
        c.execute("SELECT "+static.vacancies+" FROM CTW WHERE "+static.date+" = '"+str(yesterday)+"'")
        vacs_yesterday = c.fetchall()[0][0]

        f1 = vacs.split("\n")
        f2 = vacs_yesterday.split("\n")

        if len(f1) > len(f2):
            forl = len(f1)
        else:
            forl = len(f2)

        if f1 == f2:
            pass

        else:
            for j in range(0, forl):
                try:
                    if f1[j] in f2:
                        pass
                    else:
                        added.append(f1[j])
                        new += 1
                        total_new += 1
                except IndexError:
                    pass

                try:
                    if f2[j] in f1:
                        pass
                    else:
                        deleted_list.append(f2[j])
                        deleted += 1
                        total_deleted += 1
                except IndexError:
                    pass

        df_count_list.append([str(date), new, deleted])
        if added:
            df_5_list.append([str(date), "  |  \n".join(added)])
        if deleted_list:
            df_6_list.append([str(date), "  |  \n".join(deleted_list)])
        date = date + datetime.timedelta(days=1)
        added.clear()
        deleted_list.clear()

    except IndexError:
        pass


df1 = pd.DataFrame(df_count_list, columns=["Date", "Amount of new", "Amount of deleted"])
st.title("Day by day vacancies change")
# Showing Amount of New histogram
fig = px.bar(df1,
             x="Date",
             y="Amount of new",
             color="Amount of new").update_xaxes(categoryorder='total descending')
st.write(fig)
# Showing Amount of Deleted histogram
fig1 = px.bar(df1,
              x="Date",
              y="Amount of deleted",
              color="Amount of deleted").update_xaxes(categoryorder='total descending')
st.write(fig1)


# Creating and showing other data
st.title("Other data:")
vac_every = len(amount_of_rows) / total_new
st.write("Average time of waiting for a new vacancy: "+str(round(vac_every, 1))+" days")
st.write("The predicted amount of new positions per year: "+str(round((365 / len(amount_of_rows) * total_new), 1)))


df5 = pd.DataFrame(df_5_list, columns=["Date", "New"])
st.write("Opened positions by dates:")
st.write(df5)
df6 = pd.DataFrame(df_6_list, columns=["Date", "Deleted"])
st.write("Closed Positions by days:")
st.write(df6)
