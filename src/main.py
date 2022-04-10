from RobotScraper import RobotScraper
from datetime import datetime, timedelta
import sys

def print_menu():
    print("\n RobotScraper Definition                   Alpha Version")
    print(" #######################################################")
    print(" ## - Develop Team:                                   ##")
    print(" ##   - Placido A. Lopez Avila                        ##")
    print(" ##   - Alex Pardo Ramos                              ##")
    print(" ##                                                   ##")
    print(" ## - Alpha Version: 0.1                              ##")
    print(" ## - Alpha Date: 31/03/2022                          ##")
    print(" #######################################################\n")
    print(" Parameters Definitions:\n")

    print(" -h, --help\tShow complete menu\n")
    print(" -i, --init\tSet initial date for extract match calendar\n")
    print(" -e, --end\tSet last date for extract match calendar\n")
    print(" Note: If the help parameter (-h, --help) is included, the menu will always be displayed\n")

def first_week_day(date_arg):
    date = datetime.strptime(date_arg, '%Y%m%d')
    if date.weekday() != 0:
        date = date - timedelta(days=date.weekday())

    return date
    # return 10000*date.year + 100*date.month + date.day

def end_week_day(date_arg):
    date = datetime.strptime(date_arg, '%Y%m%d')
    if date.weekday() != 6:
        date = date + timedelta(days=(6 - date.weekday()))

    return date
    # return 10000*date.year + 100*date.month + date.day

def get_init_end():

    # Default values
    init_date = "20211018"
    end_date = None

    if len(sys.argv) > 1:
        if '-h' in sys.argv or '--help' in sys.argv:
            print_menu()
        else:
            cont = 1
            exe_loop = True
            while exe_loop:
                if sys.argv[cont] in ['-i', '--init'] and len(sys.argv) >= cont + 2:
                    init_date = sys.argv[cont + 1]
                    cont = cont + 2
                elif sys.argv[cont] in ['-e', '--end'] and len(sys.argv) >= cont + 2:
                    end_date = sys.argv[cont + 1]
                    cont = cont + 2

                if cont >= len(sys.argv):
                    exe_loop = False

            if end_date is None:
                end_date = init_date

            init, end = first_week_day(init_date), end_week_day(end_date)
            return init, end, (end.isocalendar()[1] - init.isocalendar()[1]) + 1, True

        return None, None, None, False
    else:
        print("Is necessary include parameters, try python main.py -h")
        return None, None, None, False



init, end, num_semanas, check_param = get_init_end()

if check_param:
    rs = RobotScraper()
    # rs = RobotScraper("https://espndeportes.espn.com/basquetbol/nba/calendario/_/fecha/" + str(10000*init.year + 100*init.month + init.day))

    for i in range(0, num_semanas):
        rs.set_page("https://espndeportes.espn.com", "/basquetbol/nba/calendario/_/fecha/" + str(10000*(init + (i * timedelta(days=7))).year + 100*(init + (i * timedelta(days=7))).month + (init + (i * timedelta(days=7))).day))

        # Extrae los datos generales del calendario
        rs.init_extract()


    # Extrae el detalle de los jugadores de cada partido
    rs.init_extract_players_detail()

    rs.join_info_df()
