# Web-Scraping
Repositorio fuente PRAC 1 Web Scraping

## Descripción

En esta práctica se ha extraido la información disponible para los partidos de la NBA desde la página de la [ESPN](https://espndeportes.espn.com/basquetbol/nba/calendario/_/fecha/20211018), pudiendo iterar por las diferentes semanas del calendario para generar un dataset diferente en cada ejecución.

## Instrucciones de ejecución

Para la extracción se debe ejecutar el main empleando como mínimo el parámetro -i (--init). Si empleamos el parámetro -h (--help) podrémos ver la lista de parámetros disponibles en el código:

```
python main.py -h
```

```
RobotScraper Definition                   Alpha Version
 #######################################################
 ## - Develop Team:                                   ##
 ##   - Placido A. Lopez Avila                        ##
 ##   - Alex Pardo Ramos                              ##
 ##                                                   ##
 ## - Alpha Version: 1                              ##
 ## - Alpha Date: 11/04/2022                          ##
 #######################################################

 Parameters Definitions:

 -h, --help     Show complete menu


 -i, --init     Set initial date for extract match calendar

 -e, --end      Set last date for extract match calendar
 
 -p, --path     Set path to load dataset (Default ../data/)

 Note: If the help parameter (-h, --help) is included, the menu will always be displayed
 ```
 
 ## Ejemplo de ejecución
 
```
python main.py -i 20211018 -e 20211101
```
```
Init extract games data in week 2021-10-18
Init extract games data in week 2021-10-25
Init extract games data in week 2021-11-01
Init extract detail games data...
[========================================================================] 100%
Init extract detail players data...
[========================================================================] 100%
Init join Dataframes...
Save Dataframes...
```

## Develop Team:   
    - Placido A. Lopez Avila
    - Alex Pardo Ramos
    
## Ficheros:
    - main.py
    - RobotScraper.py

## DOI Zenodo
[DOI](https://doi.org/10.5281/zenodo.6450203)
