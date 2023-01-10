import streamlit as st

st.title("Here is how stats are created:")
st.write("To come up with the amount of new and deleted vacancies program compares all historical data day by day, "
         "obtaining info about changes in vacations.")
st.write("To calculate the average opening time of the new vacancy, the program divides the number of total days that "
         "data was analyzed by the total amount of added vacancies during this period.")
st.write("To get the most popular words in the titles, the program counts every one of them, sorts them, and comes up "
         "with the result.")
st.write("To calculate the predicted amount of positions per year, "
         "the program divides 365(total amount of days per year) by amount of analyzed days, "
         "and multiplies it by all times amount of new positions ")
st.write("To come up with the list of the names of added and deleted vacancies, the program compares day-by-day "
         "changes and shows positions that were appended or deleted in every historical day. ")

# Blank space to debug page in vertical mode on mobile
st.title(" ")
