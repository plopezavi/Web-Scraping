from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd

class RobotScraper:
    soup = None
    df_games_calendar = None

    def __init__(self):
        # page = requests.get(url)
        # self.soup = BeautifulSoup(page.content, 'html.parser')
        self.df_games_calendar = pd.DataFrame(columns=['Date', 'Away Team', 'Home Team', 'Result', 'Max Winner', 'Pts Winner', 'Max Loser', 'Pts Loser', 'URL Game'])
        self.df_games_detailed_calendar = pd.DataFrame(columns=['Id Game', 'FG AT', 'FG HT', 'Field Goal % AT', 'Field Goal % HT', '3PT AT', '3PT HT', 'Three Point % AT', 'Three Point % HT', 'FT AT', 'FT HT', 'Free Throw % AT', 'Free Throw % HT', 'Rebounds AT', 'Rebounds HT', 'Offensive Rebounds AT', 'Offensive Rebounds HT', 'Defensive Rebounds AT', 'Defensive Rebounds HT', 'Assists AT', 'Assists HT', 'Steals AT', 'Steals HT', 'Blocks AT', 'Blocks HT', 'Total Turnovers AT', 'Total Turnovers HT', 'Points Off Turnovers AT', 'Points Off Turnovers HT', 'Fast Break Points AT', 'Fast Break Points HT', 'Points in Paint AT', 'Points in Paint HT', 'Fouls AT', 'Fouls HT', 'Technical Fouls AT', 'Technical Fouls HT', 'Flagrant Fouls AT', 'Flagrant Fouls HT', 'Largest Lead AT', 'Largest Lead HT'])


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
                    max_winner = columns[3].find('a').string
                    pts_winner = columns[3].find('span').text
                    max_loser = columns[4].find('a').string
                    pts_loser = columns[4].find('span').text

                    dict_game = {'Date': date, 'Away Team': away_team, 'Home Team': home_team, 'Result': result, 'Max Winner': max_winner, 'Pts Winner': pts_winner, 'Max Loser': max_loser, 'Pts Loser': pts_loser}
                    self.df_games_calendar = self.df_games_calendar.append(dict_game, ignore_index=True)

    def init_extract_game_detail(self):

        for index, row in self.df_games_calendar.iterrows():
            # Componemos la nueva URL, modificando la extension para mostrar la pestaña deseada
            url = self.hostname + row['URL Game'].replace("/juego?", "/duelo?")
            id_game = url[url.find("juegoId=") + 8:]

            page = requests.get(url)
            self.soup = BeautifulSoup(page.content, 'html.parser')

            main_content = self.soup.find('div', id="gamepackage-wrap").find('div', class_ = "col-two").find('tbody').find_all('tr')

            dict_game = {
                'Id Game': id_game
                , 'FG AT': main_content[0].find_all('td')[1].string.strip()
                , 'FG HT': main_content[0].find_all('td')[2].string.strip()
                , 'Field Goal % AT': main_content[1].find_all('td')[1].string.strip()
                , 'Field Goal % HT': main_content[1].find_all('td')[2].string.strip()
                , '3PT AT': main_content[2].find_all('td')[1].string.strip()
                , '3PT HT': main_content[2].find_all('td')[2].string.strip()
                , 'Three Point % AT': main_content[3].find_all('td')[1].string.strip()
                , 'Three Point % HT': main_content[3].find_all('td')[2].string.strip()
                , 'FT AT': main_content[4].find_all('td')[1].string.strip()
                , 'FT HT': main_content[4].find_all('td')[2].string.strip()
                , 'Free Throw % AT': main_content[5].find_all('td')[1].string.strip()
                , 'Free Throw % HT': main_content[5].find_all('td')[2].string.strip()
                , 'Rebounds AT': main_content[6].find_all('td')[1].string.strip()
                , 'Rebounds HT': main_content[6].find_all('td')[2].string.strip()
                , 'Offensive Rebounds AT': main_content[7].find_all('td')[1].string.strip()
                , 'Offensive Rebounds HT': main_content[7].find_all('td')[2].string.strip()
                , 'Defensive Rebounds AT': main_content[8].find_all('td')[1].string.strip()
                , 'Defensive Rebounds HT': main_content[8].find_all('td')[2].string.strip()
                , 'Assists AT': main_content[9].find_all('td')[1].string.strip()
                , 'Assists HT': main_content[9].find_all('td')[2].string.strip()
                , 'Steals AT': main_content[10].find_all('td')[1].string.strip()
                , 'Steals HT': main_content[10].find_all('td')[2].string.strip()
                , 'Blocks AT': main_content[11].find_all('td')[1].string.strip()
                , 'Blocks HT': main_content[11].find_all('td')[2].string.strip()
                , 'Total Turnovers AT': main_content[12].find_all('td')[1].string.strip()
                , 'Total Turnovers HT': main_content[12].find_all('td')[2].string.strip()
                , 'Points Off Turnovers AT': main_content[13].find_all('td')[1].string.strip()
                , 'Points Off Turnovers HT': main_content[13].find_all('td')[2].string.strip()
                , 'Fast Break Points AT': main_content[14].find_all('td')[1].string.strip()
                , 'Fast Break Points HT': main_content[14].find_all('td')[2].string.strip()
                , 'Points in Paint AT': main_content[15].find_all('td')[1].string.strip()
                , 'Points in Paint HT': main_content[15].find_all('td')[2].string.strip()
                , 'Fouls AT': main_content[16].find_all('td')[1].string.strip()
                , 'Fouls HT': main_content[16].find_all('td')[2].string.strip()
                , 'Technical Fouls AT': main_content[17].find_all('td')[1].string.strip()
                , 'Technical Fouls HT': main_content[17].find_all('td')[2].string.strip()
                , 'Flagrant Fouls AT': main_content[18].find_all('td')[1].string.strip()
                , 'Flagrant Fouls HT': main_content[18].find_all('td')[2].string.strip()
                , 'Largest Lead AT': main_content[19].find_all('td')[1].string.strip()
                , 'Largest Lead HT': main_content[19].find_all('td')[2].string.strip()
            }

            self.df_games_detailed_calendar = self.df_games_detailed_calendar.append(dict_game, ignore_index=True)

    def get_df(self):
        return self.df_games_calendar

    def get_df_games_detail(self):
        return self.df_games_detailed_calendar

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
