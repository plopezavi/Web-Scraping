from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd

class RobotScraper:
    hostname = None
    extension = None
    soup = None
    df_games_calendar = None
    df_games_detailed_calendar = None

    def __init__(self):
        # page = requests.get(url)
        # self.soup = BeautifulSoup(page.content, 'html.parser')
        self.df_games_calendar = pd.DataFrame(columns=['Date', 'Away Team', 'Home Team', 'Result', 'Max Winner', 'Pts Winner', 'Max Loser', 'Pts Loser', 'URL Game'])

    # def __init__(self, url):
    #     page = requests.get(url)
    #     self.soup = BeautifulSoup(page.content, 'html.parser')
    #     self.df_games_calendar = pd.DataFrame(columns=['Date', 'Away Team', 'Home Team', 'Result', 'Max Winner', 'Pts Winner', 'Max Loser', 'Pts Loser'])


    def set_page(self, hostname, extension):
        self.hostname = hostname
        self.extension = extension

        page = requests.get(hostname + extension)
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def init_extract(self):
        main_content = self.soup.find('div', class_="Wrapper Card__Content overflow-visible").find_all('div', class_="mt3")[1]
        weekly_content = main_content.find_all(['div', 'section'], class_ = ["ScheduleTables mb5 ScheduleTables--nba", "EmptyTable"])

        for daily_content in weekly_content:
            if daily_content.name == "div" and daily_content['class'][0] == "ScheduleTables":
                date_raw = daily_content.find('div', class_ = "Table__Title").string
                date = datetime.strptime(self.convert_day_ESP_ENG(date_raw), '%d de %B, %Y')


                daily_games = daily_content.find('tbody', class_ = "Table__TBODY").find_all('tr', class_ = "Table__TR Table__TR--sm Table__even")

                for game in daily_games:
                    columns = game.find_all('td')

                    away_team = columns[0].find_all('a')[1].string
                    home_team = columns[1].find_all('a')[1].string
                    result = columns[2].find('a').string
                    url_game = columns[2].find('a')['href']
                    max_winner = columns[3].find('a').string
                    pts_winner = columns[3].find('span').text
                    max_loser = columns[4].find('a').string
                    pts_loser = columns[4].find('span').text

                    dict_game = {'Date': date, 'Away Team': away_team, 'Home Team': home_team, 'Result': result, 'Max Winner': max_winner, 'Pts Winner': pts_winner, 'Max Loser': max_loser, 'Pts Loser': pts_loser, 'URL Game': url_game}
                    self.df_games_calendar = self.df_games_calendar.append(dict_game, ignore_index=True)



    def get_df_games(self):
        return self.df_games_calendar


    def save_df(self, path = '../data/'):
        self.df_games_calendar.to_csv(path + 'NBACalendarDataFrame.csv')

    @staticmethod
    def convert_day_ESP_ENG(day):

        splited_day = day.split(",")[1].split(" ")
        splited_year = day.split(",")[2]

        # Diccionario con los valores a intercambiar
        dict = {
            "enero": "January",
            "febrero": "February",
            "marzo": "March",
            "abril": "April",
            "mayo": "May",
            "junio": "June",
            "julio": "July",
            "agosto": "August",
            "septiembre": "September",
            "octubre": "October",
            "noviembre": "November",
            "diciembre": "December"
        }

        # Método Translate para pasar los carácteres acentuados y especiales a un formato aceptado por el ENG
        a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
        trans = str.maketrans(a,b)

        return splited_day[1] + " " + splited_day[2] + " " + dict[splited_day[3].translate(trans).lower()] + "," + splited_year
