import pandas as pd
import numpy as np
from Event import Event
from Team import Team
from Constant import Constant


class Game:
    """A class for keeping info about the games"""
    def __init__(self, path_to_json, event_index=0):
        # self.events = None
        self.home_team = None
        self.guest_team = None
        self.event = None
        self.game_number = path_to_json
        self.event_index = event_index
        self.shots_home = None
        self.shots_away = None
        self.shot_events = None

    def read_json(self):
        data_frame = pd.read_json('data\\'  + self.game_number + '.json')
        last_default_index = len(data_frame) - 1
        self.event_index = min(self.event_index, last_default_index)
        index = self.event_index

        #print(Constant.MESSAGE + str(last_default_index))
        event = data_frame['events'][index]
        self.event = Event(event)
        self.home_team = Team(event['home']['teamid'])
        self.guest_team = Team(event['visitor']['teamid'])
        
          
        
        event_data = pd.read_csv('events\\'  + self.game_number + '.csv')
        events = data_frame['events']
        event_ids = {int(j['eventId']):i for i,j in enumerate(events)}
        
        shots = event_data[event_data['EVENTMSGTYPE'].isin([1,2])]
        shots_home = shots[shots['PLAYER1_TEAM_ID'] == self.home_team.id]
        shots_away = shots[shots['PLAYER1_TEAM_ID'] == self.guest_team.id]
        self.shot_events = shots
        
        self.shots_home = []
        for index, row in shots_home.iterrows():
            if row['EVENTNUM'] in event_ids:
                self.shots_home.append(events[event_ids[row['EVENTNUM']]])
            
        self.shots_away = []
        for index, row in shots_away.iterrows():
            if row['EVENTNUM'] in event_ids:
                self.shots_away.append(events[event_ids[row['EVENTNUM']]])
        
        return(len(shots_home), len(shots_away))



    def get_CHADS(self):
        home_chads = []
        for shot in self.shots_home:
            tmp = Event(shot)
            #ignore events which don't contain any moments
            if tmp.moments:
                shot_time = self.shot_events[self.shot_events['EVENTNUM'] == int(shot['eventId'])]['PCTIMESTRING'].values[0]
                t = tmp.get_CHAD(self.home_team.id, shot_time)[0]
                if len(t) >= 75:
                    home_chads.append(np.mean(t))
    
        away_chads = []
        for shot in self.shots_away:
            tmp = Event(shot)
            #ignore events which don't contain any moments
            if tmp.moments:
                shot_time = self.shot_events[self.shot_events['EVENTNUM'] == int(shot['eventId'])]['PCTIMESTRING'].values[0]
                t = tmp.get_CHAD(self.guest_team.id, shot_time)[0]
                if len(t) >= 75:
                    away_chads.append(np.mean(t))
        
        return home_chads, away_chads
        
        
        
        
        
    def start(self, output):
        self.event.show(output)
