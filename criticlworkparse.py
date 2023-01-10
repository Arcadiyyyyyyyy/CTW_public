from bs4 import BeautifulSoup
import timedelta
import datetime
import requests
import sqlite3
import telebot
import static
import time
import os


def app(owner, bot, path=""):
    try:
        # Initializing database
        conn = sqlite3.connect(path+'db.db')
        c = conn.cursor()
        c.execute('''
                  CREATE TABLE IF NOT EXISTS CTW
                  ([Date] TEXT, 
                  [Vacancies] TEXT)
                  ''')

        print("Started CTW")

        # Creating static variables
        date = datetime.date.today()
        yesterday = date - timedelta.Timedelta(days=1)
        file = os.path.exists(path+"Recovery_Data/htmls/index_"+str(date)+".html")
        url = "https://join.criticaltechworks.com/jobs?location=Porto&query="
        vacancies = []

        # Making request to ctw site if it wasn't made today already
        if file is False:
            headers = {
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/107.0.0.0 Safari/537.36"
            }

            print("Parsing started")
            bot.send_message(owner, "CTW Parsing started")

            src = requests.get(url, headers=headers).text

            # """Checking if the data was received, saving data from the site to
            # make sure that in case of an error request won't be sent again"""
            if src[0] == "<":
                with open(path+"Recovery_Data/htmls/index_"+str(date)+".html", "w", encoding="utf-8") as f:
                    f.write(src)
                    f.close()
        else:
            print("Parsing not needed")

        print("Started reading html")

        # Reading data from previous save
        with open(path+"Recovery_Data/htmls/index_"+str(date)+".html", encoding="utf-8") as f:
            src = f.read()
            f.close()

        # Processing data from the site by collecting titles of open vacancies
        all_vacancies = BeautifulSoup(src, "lxml").find_all(
            class_="text-block-base-link sm:min-w-[25%] sm:truncate company-link-style"
        )

        # Changing the appearance of vacancies
        for vacancy in all_vacancies:
            vacancies.append(vacancy.text)

        # Sorting vacancies for easier visual day to day recognition
        vacancies.sort()
        vacancies_exit = "\n".join(vacancies)
        with open(path+"Recovery_Data/vacancies/vacancies_"+str(date)+".txt", "w", encoding="utf-8") as vtoday:
            vtoday.write(vacancies_exit)
            vtoday.close()

        # Adding data to the database if there is no row for today
        c.execute("SELECT * FROM CTW WHERE Date='" + str(date) + "';")
        sql_today_value = c.fetchall()
        conn.commit()

        if sql_today_value:
            pass
        else:
            c.execute("INSERT INTO CTW (Date, Vacancies) "
                      "VALUES ('" + str(date) + "', '" + str(vacancies_exit) + "')")
            conn.commit()

        vacancies = vacancies_exit.split("\n")
        vacancies.sort()

        print("Started comparing")

        # Comparing today's vacancies with yesterday's
        c.execute("SELECT * FROM CTW WHERE Date='"+str(yesterday)+"';")
        yesterday_row = c.fetchall()
        conn.commit()
        conn.close()

        try:
            bot.send_document(static.owner, telebot.types.InputFile(path+"db.db"))
            bot.send_document(static.owner, telebot.types.InputFile(
                path+"Recovery_Data/htmls/index_"+str(date)+".html")
                              )
            bot.send_document(static.owner, telebot.types.InputFile(
                path+"Recovery_Data/vacancies/vacancies_"+str(date)+".txt")
                              )
        except Exception as e:
            bot.send_message(static.owner, "Failed to send backup files")
            print(e)

        f2 = yesterday_row[0][1]
        f2 = f2.split("\n")
        f1 = vacancies_exit.split("\n")

        if len(f1) > len(f2):
            forl = len(f1)
        else:
            forl = len(f2)

        if f1 == f2:
            print("\nThere is no new vacancies today\n")
            bot.send_message(owner, "There is no new vacancies today")

        # Sending a message to frontend about the today's vacancies
        else:
            for i in range(0, forl):
                try:
                    if f1[i] in f2:
                        pass
                    else:
                        print("\nNew vacancy found! \n"+f1[i])
                        bot.send_message(owner, "\nNew vacancy found! \n"+f1[i])
                except IndexError:
                    pass

                try:
                    if f2[i] in f1:
                        pass
                    else:
                        print("\n"+str(f2[i])+" vacancy was deleted")
                        bot.send_message(owner, "\n"+str(f2[i])+" vacancy was deleted")
                except IndexError:
                    pass

    # Creating logs in case of an error
    except Exception as e:
        with open(path+"logs_ctw.txt", "a", encoding="utf-8") as logs:
            logs.write(f"Error {e} happened at {datetime.datetime.now()}\n")
            logs.close()
        print(f"Error {e} happened")


# Launching program without implementation in frontend in infinite loop
if __name__ == "__main__":
    while True:
        app(static.owner, telebot.TeleBot(static.bot_token, parse_mode="HTML"))
        time.sleep(86400)
