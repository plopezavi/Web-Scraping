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
    df_games_detailed_players = None

    def __init__(self):
        # page = requests.get(url)
        # self.soup = BeautifulSoup(page.content, 'html.parser')
        self.df_games_calendar = pd.DataFrame(columns=['Date', 'Away Team', 'Home Team', 'Result', 'Max Winner', 'Pts Winner', 'Max Loser', 'Pts Loser', 'URL Game'])
        self.df_games_detailed_players = pd.DataFrame(columns=['Id Game', 'Team', 'Name', 'Position', 'First/Substitute', 'MIN', 'FG', '% TC3', 'TL A-I', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'PÉR', 'PF', '+/-', 'PTS'])

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



    def init_extract_players_detail(self):

            for index, row in self.df_games_calendar.iterrows():
                # Componemos la nueva URL, modificando la extension para mostrar la pestaña deseada
                url = self.hostname + row['URL Game'].replace("/juego?juegoId=", "/ficha/_/juegoId/")
                id_game = url[url.find("juegoId/") + 8:]

                page = requests.get(url)
                self.soup = BeautifulSoup(page.content, 'html.parser')

                main_content = self.soup.find('div', id="gamepackage-box-score").find('div', class_ = "row-wrapper").find_all('div',  class_ = ["col column-one gamepackage-away-wrap", "col column-two gamepackage-home-wrap"])

                awayTeamName = main_content[0].find('div', class_ = 'team-name').text
                homeTeamName = main_content[1].find('div', class_ = 'team-name').text

                awayTeam = main_content[0].find('table', class_ = 'mod-data').find_all('tbody')
                awayTeamFirst = awayTeam[0].find_all('tr')
                awayTeamSubstitute = awayTeam[1].find_all('tr', class_ = '')
                homeTeam = main_content[1].find('table', class_ = 'mod-data').find_all('tbody')
                homeTeamFirst = homeTeam[0].find_all('tr')
                homeTeamSubstitute = homeTeam[1].find_all('tr', class_ = '')

                # Equipo visitante, titular
                for item in awayTeamFirst:

                    data_player = item.find_all('td')

                    dict_away_team = {
                        'Id Game': id_game
                        , 'Team': awayTeamName
                        , 'Name': data_player[0].find('span').string
                        , 'Position': data_player[0].find('span', class_ = 'position').string
                        , 'First/Substitute': 'First'
                        , 'MIN': data_player[1].string
                        , 'FG': data_player[2].string
                        , '% TC3': data_player[3].string
                        , 'TL A-I': data_player[4].string
                        , 'OREB': data_player[5].string
                        , 'DREB': data_player[6].string
                        , 'REB': data_player[7].string
                        , 'AST': data_player[8].string
                        , 'STL': data_player[9].string
                        , 'BLK': data_player[10].string
                        , 'PÉR': data_player[11].string
                        , 'PF': data_player[12].string
                        , '+/-': data_player[13].string
                        , 'PTS': data_player[14].string
                    }

                    self.df_games_detailed_players = self.df_games_detailed_players.append(dict_away_team, ignore_index=True)

                # Equipo visitante, suplente
                for item in awayTeamSubstitute:

                    if item.find('td', class_ = 'dnp') is not None:
                        data_player = item.find_all('td')

                        dict_away_team = {
                            'Id Game': id_game
                            , 'Team': awayTeamName
                            , 'Name': data_player[0].find('span').string
                            , 'Position': data_player[0].find('span', class_ = 'position').string
                            , 'First/Substitute': 'Substitute'
                            , 'MIN': None
                            , 'FG': None
                            , '% TC3': None
                            , 'TL A-I': None
                            , 'OREB': None
                            , 'DREB': None
                            , 'REB': None
                            , 'AST': None
                            , 'STL': None
                            , 'BLK': None
                            , 'PÉR': None
                            , 'PF': None
                            , '+/-': None
                            , 'PTS': None
                        }
                    else:
                        data_player = item.find_all('td')

                        dict_away_team = {
                            'Id Game': id_game
                            , 'Team': awayTeamName
                            , 'Name': data_player[0].find('span').string
                            , 'Position': data_player[0].find('span', class_ = 'position').string
                            , 'First/Substitute': 'Substitute'
                            , 'MIN': data_player[1].string
                            , 'FG': data_player[2].string
                            , '% TC3': data_player[3].string
                            , 'TL A-I': data_player[4].string
                            , 'OREB': data_player[5].string
                            , 'DREB': data_player[6].string
                            , 'REB': data_player[7].string
                            , 'AST': data_player[8].string
                            , 'STL': data_player[9].string
                            , 'BLK': data_player[10].string
                            , 'PÉR': data_player[11].string
                            , 'PF': data_player[12].string
                            , '+/-': data_player[13].string
                            , 'PTS': data_player[14].string
                        }

                    self.df_games_detailed_players = self.df_games_detailed_players.append(dict_away_team, ignore_index=True)

                # Equipo local, titular
                for item in homeTeamFirst:

                    data_player = item.find_all('td')

                    dict_away_team = {
                        'Id Game': id_game
                        , 'Team': homeTeamName
                        , 'Name': data_player[0].find('span').string
                        , 'Position': data_player[0].find('span', class_ = 'position').string
                        , 'First/Substitute': 'First'
                        , 'MIN': data_player[1].string
                        , 'FG': data_player[2].string
                        , '% TC3': data_player[3].string
                        , 'TL A-I': data_player[4].string
                        , 'OREB': data_player[5].string
                        , 'DREB': data_player[6].string
                        , 'REB': data_player[7].string
                        , 'AST': data_player[8].string
                        , 'STL': data_player[9].string
                        , 'BLK': data_player[10].string
                        , 'PÉR': data_player[11].string
                        , 'PF': data_player[12].string
                        , '+/-': data_player[13].string
                        , 'PTS': data_player[14].string
                    }

                    self.df_games_detailed_players = self.df_games_detailed_players.append(dict_away_team, ignore_index=True)

                # Equipo local, suplente
                for item in homeTeamSubstitute:

                    if item.find('td', class_ = 'dnp') is not None:
                        data_player = item.find_all('td')

                        dict_away_team = {
                            'Id Game': id_game
                            , 'Team': homeTeamName
                            , 'Name': data_player[0].find('span').string
                            , 'Position': data_player[0].find('span', class_ = 'position').string
                            , 'First/Substitute': 'Substitute'
                            , 'MIN': None
                            , 'FG': None
                            , '% TC3': None
                            , 'TL A-I': None
                            , 'OREB': None
                            , 'DREB': None
                            , 'REB': None
                            , 'AST': None
                            , 'STL': None
                            , 'BLK': None
                            , 'PÉR': None
                            , 'PF': None
                            , '+/-': None
                            , 'PTS': None
                        }
                    else:
                        data_player = item.find_all('td')

                        dict_away_team = {
                            'Id Game': id_game
                            , 'Team': homeTeamName
                            , 'Name': data_player[0].find('span').string
                            , 'Position': data_player[0].find('span', class_ = 'position').string
                            , 'First/Substitute': 'Substitute'
                            , 'MIN': data_player[1].string
                            , 'FG': data_player[2].string
                            , '% TC3': data_player[3].string
                            , 'TL A-I': data_player[4].string
                            , 'OREB': data_player[5].string
                            , 'DREB': data_player[6].string
                            , 'REB': data_player[7].string
                            , 'AST': data_player[8].string
                            , 'STL': data_player[9].string
                            , 'BLK': data_player[10].string
                            , 'PÉR': data_player[11].string
                            , 'PF': data_player[12].string
                            , '+/-': data_player[13].string
                            , 'PTS': data_player[14].string
                        }

                    self.df_games_detailed_players = self.df_games_detailed_players.append(dict_away_team, ignore_index=True)


    def get_df_games(self):
        return self.df_games_calendar

    def get_df_games_detailed_players(self):
        return self.df_games_detailed_players

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
