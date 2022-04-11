from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import progressbar

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
        self.df_games_detailed_calendar = pd.DataFrame(columns=['Id Game', 'FG AT', 'FG HT', 'Field Goal % AT', 'Field Goal % HT', '3PT AT', '3PT HT', 'Three Point % AT', 'Three Point % HT', 'FT AT', 'FT HT', 'Free Throw % AT', 'Free Throw % HT', 'Rebounds AT', 'Rebounds HT', 'Offensive Rebounds AT', 'Offensive Rebounds HT', 'Defensive Rebounds AT', 'Defensive Rebounds HT', 'Assists AT', 'Assists HT', 'Steals AT', 'Steals HT', 'Blocks AT', 'Blocks HT', 'Total Turnovers AT', 'Total Turnovers HT', 'Points Off Turnovers AT', 'Points Off Turnovers HT', 'Fast Break Points AT', 'Fast Break Points HT', 'Points in Paint AT', 'Points in Paint HT', 'Fouls AT', 'Fouls HT', 'Technical Fouls AT', 'Technical Fouls HT', 'Flagrant Fouls AT', 'Flagrant Fouls HT', 'Largest Lead AT', 'Largest Lead HT'])
        self.df_games_detailed_players = pd.DataFrame(columns=['Id Game', 'Team', 'Name', 'Position', 'First/Substitute', 'MIN', 'FG', '% TC3', 'TL A-I', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'PÉR', 'PF', '+/-', 'PTS'])

    # def __init__(self, url):
    #     page = requests.get(url)
    #     self.soup = BeautifulSoup(page.content, 'html.parser')
    #     self.df_games_calendar = pd.DataFrame(columns=['Date', 'Away Team', 'Home Team', 'Result', 'Max Winner', 'Pts Winner', 'Max Loser', 'Pts Loser'])

    def get_id_game(self, row):

        if row['URL Game'] is not None:
            url = row['URL Game']
            return url[url.find("juegoId=") + 8:]
        else:
            return '-1'

    def set_page(self, hostname, extension):
        self.hostname = hostname
        self.extension = extension

        page = requests.get(hostname + extension)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        self.df_games_detailed_calendar = pd.DataFrame(columns=['Id Game', 'FG AT', 'FG HT', 'Field Goal % AT', 'Field Goal % HT', '3PT AT', '3PT HT', 'Three Point % AT', 'Three Point % HT', 'FT AT', 'FT HT', 'Free Throw % AT', 'Free Throw % HT', 'Rebounds AT', 'Rebounds HT', 'Offensive Rebounds AT', 'Offensive Rebounds HT', 'Defensive Rebounds AT', 'Defensive Rebounds HT', 'Assists AT', 'Assists HT', 'Steals AT', 'Steals HT', 'Blocks AT', 'Blocks HT', 'Total Turnovers AT', 'Total Turnovers HT', 'Points Off Turnovers AT', 'Points Off Turnovers HT', 'Fast Break Points AT', 'Fast Break Points HT', 'Points in Paint AT', 'Points in Paint HT', 'Fouls AT', 'Fouls HT', 'Technical Fouls AT', 'Technical Fouls HT', 'Flagrant Fouls AT', 'Flagrant Fouls HT', 'Largest Lead AT', 'Largest Lead HT'])


    def init_extract(self):

        print("Init extract games data in week", datetime.strptime(self.extension[self.extension.find("/_/fecha/") + 9:], '%Y%m%d').date())

        main_content = self.soup.find('div', class_="Wrapper Card__Content overflow-visible").find_all('div', class_="mt3")[1]
        weekly_content = main_content.find_all(['div', 'section'], class_ = ["ScheduleTables mb5 ScheduleTables--nba", "EmptyTable"])

        for daily_content in weekly_content:

            if daily_content.name == "div" and daily_content['class'][0] == "ScheduleTables":
                date_raw = daily_content.find('div', class_ = "Table__Title").string
                date = datetime.strptime(self.convert_day_ESP_ENG(date_raw), '%d de %B, %Y')


                daily_games = daily_content.find('tbody', class_ = "Table__TBODY").find_all('tr', class_ = "Table__TR Table__TR--sm Table__even")

                for game in daily_games:

                    columns = game.find_all('td')

                    if columns[2].find('a').string.lower() == "pospuesto":
                        if len(columns[0].find_all('a')) == 1:
                            away_team = columns[0].find('span', class_ = 'Table__Team away').find('span').text
                        else:
                            away_team = columns[0].find_all('a')[1].string

                        if len(columns[1].find_all('a')) == 1:
                            home_team = columns[1].find('span', class_ = 'Table__Team').find('span').text
                        else:
                            home_team = columns[1].find_all('a')[1].string

                        result = columns[2].find('a').string
                        url_game = None
                        max_winner = None
                        pts_winner = None
                        max_loser = None
                        pts_loser = None
                    else:
                        if len(columns[0].find_all('a')) == 1:
                            away_team = columns[0].find('span', class_ = 'Table__Team away').find('span').text
                        else:
                            away_team = columns[0].find_all('a')[1].string

                        if len(columns[1].find_all('a')) == 1:
                            home_team = columns[1].find('span', class_ = 'Table__Team').find('span').text
                        else:
                            home_team = columns[1].find_all('a')[1].string

                        result = columns[2].find('a').string
                        url_game = columns[2].find('a')['href']
                        max_winner = columns[3].find('a').string
                        pts_winner = columns[3].find('span').text
                        max_loser = columns[4].find('a').string
                        pts_loser = columns[4].find('span').text

                    dict_game = {'Date': date, 'Away Team': away_team, 'Home Team': home_team, 'Result': result, 'Max Winner': max_winner, 'Pts Winner': pts_winner, 'Max Loser': max_loser, 'Pts Loser': pts_loser, 'URL Game': url_game}
                    self.df_games_calendar = self.df_games_calendar.append(dict_game, ignore_index=True)

    def init_extract_game_detail(self):

        print("Init extract detail games data...")

        bar = progressbar.ProgressBar(maxval=len(self.df_games_calendar), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for index, row in self.df_games_calendar.iterrows():

            if row['URL Game'] is not None:

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

            bar.update(index+1)

        bar.finish()

    def init_extract_players_detail(self):

        print("Init extract detail players data...")

        bar = progressbar.ProgressBar(maxval=len(self.df_games_calendar), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for index, row in self.df_games_calendar.iterrows():

            if row['URL Game'] is not None:

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

            bar.update(index+1)

        bar.finish()

    def join_info_df(self, path = '../data/'):

        print("Init join Dataframes...")

        self.df_games_calendar['Id Game'] = self.df_games_calendar.apply(lambda row: self.get_id_game(row), axis=1)
        self.df_games_calendar = self.df_games_calendar.drop(['URL Game'], axis=1)

        df = pd.merge(self.df_games_calendar, self.df_games_detailed_calendar, on = 'Id Game', how='left')
        df = pd.merge(df, self.df_games_detailed_players, on = 'Id Game', how='left')

        print("Save Dataframes...")
        self.save_df(df, path)


    def get_df_games(self):
        return self.df_games_calendar

    def get_df_games_detailed_players(self):
        return self.df_games_detailed_players

    def get_df_games_detail(self):
        return self.df_games_detailed_calendar

    def save_df(self, df, path):
        df.to_csv(path + 'NBACalendarDataFrame.csv')

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
