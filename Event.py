from Constant import Constant
from Moment import Moment
from Team import Team
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Rectangle, Arc, Polygon

from scipy.spatial import ConvexHull
import numpy as np
from datetime import datetime

import os


class Event:
    """A class for handling and showing events"""

    def __init__(self, event):
        moments = event['moments']
        self.moments = [Moment(moment) for moment in moments]
        home_players = event['home']['players']
        guest_players = event['visitor']['players']
        players = home_players + guest_players
        player_ids = [player['playerid'] for player in players]
        player_names = [" ".join([player['firstname'],
                        player['lastname']]) for player in players]
        player_jerseys = [player['jersey'] for player in players]
        values = list(zip(player_names, player_jerseys))
        # Example: 101108: ['Chris Paul', '3']
        self.player_ids_dict = dict(zip(player_ids, values))
        self.CHAD = []
        self.CHAO = []

    def update_radius(self, i, player_circles, ball_circle, chad, annotations, clock_info, column_labels):
        moment = self.moments[i]
        offense_pts = []
        defense_pts = []
        for j, circle in enumerate(player_circles):
            if(j >= len(moment.players)):
                break
            circle.center = moment.players[j].x, moment.players[j].y
            if(moment.players[j].team.id == moment.players[0].team.id):
                offense_pts.append([moment.players[j].x, moment.players[j].y])
            else:
                defense_pts.append([moment.players[j].x, moment.players[j].y])   
            annotations[j].set_position(circle.center)
            if(moment.shot_clock == None):
                break
            clock_test = 'Quarter {:d}\n {:02d}:{:02d} {:03.1f}\n'.format(
                         moment.quarter,
                         int(moment.game_clock) % 3600 // 60,
                         int(moment.game_clock) % 60,
                         moment.shot_clock)
            clock_info.set_text(clock_test)
        ball_circle.center = moment.ball.x, moment.ball.y
        ball_circle.radius = moment.ball.radius / Constant.NORMALIZATION_COEF
        
        #updated the plotting to include convex hull area
        if(len(defense_pts) != 0):
            hull = ConvexHull(defense_pts)
            chad.xy = [defense_pts[i] for i in hull.vertices]
            
            clock_test = 'Quarter {:d}  {:02d}:{:02d}\n {:03.1f}\n CHAD: {:04.1f}'.format(
                             moment.quarter,
                             int(moment.game_clock) % 3600 // 60,
                             int(moment.game_clock) % 60,
                             moment.shot_clock,
                             hull.volume)
            clock_info.set_text(clock_test)
            
        return player_circles, ball_circle, chad
        
        
        

##################### Code by Chris Spennato ###########################

#function to calculate the average CHAD for this play
#takes offense_id to know which team is on offense_id
#takes shot_time to stop calculating CHAD after shot taken

#returns a list of CHAD, one for each frame, for each team
    def get_CHAD(self, offense_id, shot_time):
        pt = datetime.strptime(shot_time,'%M:%S')
        shot_seconds = pt.second + pt.minute*60
        
        #iterate through all frames of the play
        for i, moment in enumerate(self.moments):
            #if data is missing player data skip
            if len(moment.players) == 0:
                continue
                
            #if time has passed shot_time, stop
            if moment.game_clock <= shot_seconds:
                break
                
            #gather points for each team at this frame
            offense_pts = []
            defense_pts = []
            for j, circle in enumerate(self.moments[0].players):
                if(j >= len(moment.players)):
                    break
                if(moment.players[j].team.id == offense_id):
                    offense_pts.append([moment.players[j].x, moment.players[j].y])
                else:
                    defense_pts.append([moment.players[j].x, moment.players[j].y])      
            
            #if there are less than three players, ignore this frame
            if len(offense_pts) > 2 and len(defense_pts) > 2:
                #append the convex hull area to each list
                self.CHAD.append(ConvexHull(defense_pts).volume)
                self.CHAO.append(ConvexHull(offense_pts).volume)
                
        return self.CHAD, self.CHAO


############################################################################        


    def show(self, output):
        # Leave some space for inbound passes
        ax = plt.axes(xlim=(Constant.X_MIN,
                            Constant.X_MAX),
                      ylim=(Constant.Y_MIN,
                            Constant.Y_MAX))
        ax.axis('off')
        fig = plt.gcf()
        ax.grid(False)  # Remove grid
        start_moment = self.moments[0]
        player_dict = self.player_ids_dict

        clock_info = ax.annotate('', xy=[Constant.X_CENTER, Constant.Y_CENTER],
                                 color='black', horizontalalignment='center',
                                   verticalalignment='center')

        annotations = [ax.annotate(self.player_ids_dict[player.id][1], xy=[0, 0], color='w',
                                   horizontalalignment='center',
                                   verticalalignment='center', fontweight='bold')
                       for player in start_moment.players]

        # Prepare table
        sorted_players = sorted(start_moment.players, key=lambda player: player.team.id)
        
        home_player = sorted_players[0]
        guest_player = sorted_players[5]
        column_labels = tuple([home_player.team.name, guest_player.team.name])
        column_colours = tuple([home_player.team.color, guest_player.team.color])
        cell_colours = [column_colours for _ in range(5)]
        
        home_players = [' #'.join([player_dict[player.id][0], player_dict[player.id][1]]) for player in sorted_players[:5]]
        guest_players = [' #'.join([player_dict[player.id][0], player_dict[player.id][1]]) for player in sorted_players[5:]]
        players_data = list(zip(home_players, guest_players))
        
        
        table = plt.table(cellText=players_data,
                              colLabels=column_labels,
                              colColours=column_colours,
                              colWidths=[Constant.COL_WIDTH, Constant.COL_WIDTH],
                              loc='bottom',
                              cellColours=cell_colours,
                              fontsize=Constant.FONTSIZE,
                              cellLoc='center')
        table.scale(1, Constant.SCALE)
        table_cells = table.properties()['children']
        for cell in table_cells:
            cell._text.set_color('white')

        player_circles = [plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE, color=player.color)
                          for player in start_moment.players]
        ball_circle = plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE,
                                 color=start_moment.ball.color)
                                 
        chad = plt.Polygon([[0,0],[0,0]], color=home_player.team.color, alpha=0.3)                         
        
        for circle in player_circles:
            ax.add_patch(circle)
        ax.add_patch(ball_circle)
        ax.add_patch(chad)

        anim = animation.FuncAnimation(
                         fig, self.update_radius,
                         fargs=(player_circles, ball_circle, chad, annotations, clock_info, column_labels),
                         frames=len(self.moments), interval=Constant.INTERVAL)
        court = plt.imread("court.png")
        plt.imshow(court, zorder=0, extent=[Constant.X_MIN, Constant.X_MAX - Constant.DIFF,
                                            Constant.Y_MAX, Constant.Y_MIN])
        #plt.show()
        
        
        #modified to save the output rather than showing it
        f = os.path.join(os.getcwd(), output + '.gif')
        writergif = animation.PillowWriter(fps=30) 
        anim.save(f, writer=writergif)
