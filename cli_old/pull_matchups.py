from lxml import html
import requests
from bs4 import BeautifulSoup as BSoup

def pull_matchups(year, month, day):

    day = day if day>=10 else f'0{day}'
    month = month if month>=10 else f'0{month}'

    day_url = f'https://www.espn.com/nba/scoreboard/_/date/{year}{month}{day}'
    # print (day_url)
    boxscore = requests.get(day_url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
    boxStr = boxscore.content.decode('utf-8')
    gamesData = BSoup(boxStr, features="lxml")

    linkBase = 'https://www.espn.com'
    linkStr = 'nba/game/_/gameId/'

    matchups = []

    games = gamesData.find_all('div', {"class": "Scoreboard__RowContainer"})
    # print (len(games),'games')
    for game in games:
        teams = game.find_all('span', {"class": "Athlete__NameDetails"})
        home=False
        matchup = []
        for team in teams:

            team_txt = team.getText().split('- ')[1].strip()

            if home:
                matchup = [team_txt] + matchup
            else:
                matchup = [team_txt]
                home = True
        if matchup==None:
            continue

        matchups.append(matchup)

    # print (matchups)
    return matchups

