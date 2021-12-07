################ WARNING - This can take a very long time to run depending on the number of games ##############


#Script to calculate average CHADs for many games at a time
#takes in path to a directory containing the json files
#requires json data to be in directory called data and event data to be in csv format in directory called events
#both files should simply be called <game_id>.json or <game_id>.csv

import sys,os, getopt

from Game import Game
import pandas as pd
import numpy as np



def main(argv):
    
    directory = ''
    outputfile = ''
    
    #takes in the output file location/name as an argument
    try:
        opts, args = getopt.getopt(argv,"hd:o:")
    except getopt.GetoptError:
        print('python getCHADS.py -d /path/to/directory -o <output_file.csv>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('python getCHADS.py -d /path/to/directory -o <output_file.csv>')
            sys.exit()
        elif opt in ("-o"):
            outputfile = arg
        elif opt in ("-d"):
            directory = arg
    
    
    #iterates through each file in the json directory provided
    files = os.listdir(directory)
    print('Total number of games: ' + str(len(files)))
    count = 0
    columns=['Game ID', 'Home Team', 'Home Shots', 'Home Shots Used', 'Home CHAD', 'Away Team', 'Away Shots', 'Away Shots Used', 'Away CHAD']
    df = pd.DataFrame(columns=columns)
    
    #for each file get the chad, shots, etc and append to the dataframe
    errors = []
    for file in files:
        try:
            print('Processing game ' + file[:10])
            game = Game(path_to_json=file[:10])
            total_shots = game.read_json()
            chads = game.get_CHADS()
            
            data = [game.game_number, game.home_team.name, total_shots[0], len(chads[0]), np.mean(chads[0]), game.guest_team.name, total_shots[1], len(chads[1]), np.mean(chads[1])]
            df = df.append(pd.DataFrame(data=[data],columns=columns))
            
            print('Completed processing game ' + file[:10])
            count += 1 
         
        #catch any errors so script doesn't crash 
        except OSError:
            print('Error accessing file: ' + file)
        except Exception as e:
            print('Error with game: ' + file[:10])
            print(e)
            errors.append([file[:10], e])
        
        print('Games processed: ' + str(count))
    
    print('Successfully processed ' + str(count) + ' of ' + str(len(files)) + ' games')
    
   #write the output to the given outputfile
    try:
        df.to_csv(outputfile, index = False)
    #backup in case outputfile has issue
    except OSError:
        df.to_csv('backup.csv', index = False)
        print('Error writing to output file')
        print('Data written to backup.csv')
        sys.exit()
	
    #write errors to a file as well
    try:
        with open('errors.txt', 'w') as f:
            f.write(errors)
    except OSError:
        print(errors)
	
	
	
if __name__ == '__main__':
	main(sys.argv[1:])
	
	
	
	
	
