from RobotScraper import RobotScraper

rs = RobotScraper("https://espndeportes.espn.com/basquetbol/nba/calendario/_/fecha/20211018")
rs.init_extract()
# print(rs.get_df())
rs.save_df()
