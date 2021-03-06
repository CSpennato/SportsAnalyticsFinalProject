#Script to generate plots using data generated by getCHADS.py


import pandas
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

###### This code is identical to the 'Final Notebook' jupyter notebook ################

chads_initial = pandas.read_csv(r'stats\final.csv')
chads_initial[chads_initial['Home Team'] == 'TOR']

chads = chads_initial[chads_initial['Home Shots Used'] >= chads_initial['Home Shots']/2]
chads = chads[chads['Away Shots Used'] >= chads['Away Shots']/2]
chads

away = chads.iloc[:,[5,4]]
away.columns = ['Team', 'CHAD']
home = chads.iloc[:,[1,8]]
home.columns = ['Team', 'CHAD']
achad = pandas.concat([away,home])
achad = achad.groupby('Team').mean()
achad

chads = chads.copy()
chads = chads.join(achad, on=['Home Team'])
chads = chads.rename(columns={'CHAD':'Home Avg CHAD'})
chads = chads.join(achad, on=['Away Team'])
chads = chads.rename(columns={'CHAD':'Away Avg CHAD'})
chads['Home Impact'] = chads['Home CHAD'] - chads['Away Avg CHAD']
chads['Away Impact'] = chads['Away CHAD'] - chads['Home Avg CHAD']
chads['Home Impact %'] = 100*chads['Home Impact']/chads['Away Avg CHAD']
chads['Away Impact %'] = 100*chads['Away Impact']/chads['Home Avg CHAD']
chads

away = chads.iloc[:,[5,14]]
away.columns = ['Team', 'Impact']
home = chads.iloc[:,[1,13]]
home.columns = ['Team', 'Impact']
avgImpact = pandas.concat([away,home])
avgImpact = avgImpact.groupby('Team').mean()
#avgImpact.sort_values(by='Impact')
avgImpact

#https://www.basketball-reference.com/leagues/NBA_2016.html#all_per_game_team-opponent
#Sports Reference LLC "(title of a particular page or blank for general citation)." Basketball-Reference.com - Basketball Statistics and History. https://www.basketball-reference.com/. (date of your visit)
#Provided by Basketball-Reference.com
#Generated 12/1/2021.
teams = {'Atlanta Hawks':'ATL', 'Boston Celtics':'BOS', 'Brooklyn Nets':'BKN', 'Charlotte Hornets':'CHA', 'Chicago Bulls':'CHI',
        'Cleveland Cavaliers':'CLE', 'Dallas Mavericks':'DAL', 'Denver Nuggets':'DEN','Detroit Pistons':'DET','Golden State Warriors':'GSW',
        'Houston Rockets':'HOU', 'Indiana Pacers':'IND','Los Angeles Clippers':'LAC','Los Angeles Lakers':'LAL', 'Memphis Grizzlies':'MEM',
        'Miami Heat':'MIA','Milwaukee Bucks':'MIL','Minnesota Timberwolves':'MIN','New Orleans Pelicans':'NOP','New York Knicks':'NYK',
        'Oklahoma City Thunder':'OKC','Orlando Magic':'ORL','Philadelphia 76ers':'PHI','Phoenix Suns':'PHX','Portland Trail Blazers':'POR',
        'Sacramento Kings':'SAC','San Antonio Spurs':'SAS','Toronto Raptors':'TOR','Utah Jazz':'UTA','Washington Wizards':'WAS'}

team_stats_per100 = pandas.read_csv(r'stats\15-16 Team Stats.csv')
team_stats_per100 = team_stats_per100.iloc[:,[1,8,9]]
team_stats_per100.sort_values(by='Team')
team_stats_per100['Team'] = team_stats_per100['Team'].str.replace('*','')
team_stats_per100['Team Code'] = team_stats_per100['Team'].map(teams)
team_stats_per100

#############################################################


def getImage(path):
    return OffsetImage(plt.imread(path), zoom=0.15)

#paths to each logo
paths = ['Logos\\' + a + '.png' for a in team_stats_per100.sort_values(by='Team Code')['Team Code']]

fig, ax = plt.subplots()
ax.scatter(team_stats_per100.sort_values(by='Team Code')['3PA'], avgImpact) 

for x0, y0, path in zip(team_stats_per100.sort_values(by='Team Code')['3PA'], avgImpact['Impact'],paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
    ax.add_artist(ab)

ax.set_ylim([-20,25])
ax.set_facecolor('whitesmoke')
plt.title('NBA Spacing Impact 2015-16 Season', fontsize=30)
plt.ylabel('ASID (%)', fontsize=20)
plt.xlabel('Three Point Attempts (per 100 possessions)', fontsize=20)

plt.show()

colors = [
        '#E13A3E',
        '#008348',
        '#061922',
        '#1D1160',
        '#CE1141',
        '#860038',
        '#007DC5',
        '#4D90CD',
        '#006BB6',
        '#FDB927',
        '#CE1141',
        '#00275D',
        '#ED174C',
        '#552582',
        '#0F586C',
        '#98002E',
        '#00471B',
        '#005083',
        '#002B5C',
        '#006BB6',
        '#007DC3',
        '#007DC5',
        '#006BB6',
        '#1D1160',
        '#E03A3E',
        '#724C9F',
        '#BAC3C9',
        '#CE1141',
        '#00471B',
        '#002B5C']
        
color_dict = {t:c for t,c in zip(avgImpact.index, colors)}

def getImage(path):
    return OffsetImage(plt.imread(path), zoom=0.13)

plt.bar(avgImpact.sort_values(by='Impact').index, avgImpact.sort_values(by='Impact')['Impact'], color=[color_dict[i] for i in avgImpact.sort_values(by='Impact').index])
ax = plt.gca()
ax.set_ylim([-23,28])

paths = ['Logos\\' + a + '.png' for a in avgImpact.sort_values(by='Impact').index]

icon_pts = [i+2 if i > 0 else i-2 for i in avgImpact.sort_values(by='Impact')['Impact']]
for x0, y0, path in zip(avgImpact.sort_values(by='Impact').index, icon_pts,paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
    ax.add_artist(ab)
    
    
ax.set_facecolor('whitesmoke')
plt.title('NBA Spacing Impact 2015-16 Season', fontsize=30)
plt.ylabel('ASID (%)', fontsize=20)
ax.get_xaxis().set_visible(False)

plt.show()