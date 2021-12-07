import sys,os, getopt

from Game import Game
import pandas as pd
import numpy as np



def main(argv):
    
    directory = ''
    outputfile = ''
    
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
    
    
    files = os.listdir(directory)
    print('Total number of games: ' + str(len(files)))
    count = 0
    columns=['Game ID', 'Home Team', 'Home Shots', 'Home Shots Used', 'Home CHAD', 'Away Team', 'Away Shots', 'Away Shots Used', 'Away CHAD']
    df = pd.DataFrame(columns=columns)
    
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
            
        except OSError:
            print('Error accessing file: ' + file)
        except Exception as e:
            print('Error with game: ' + file[:10])
            print(e)
            errors.append([file[:10], e])
        
        print('Games processed: ' + str(count))
    
    print('Successfully processed ' + str(count) + ' of ' + str(len(files)) + ' games')
    
   
    try:
        df.to_csv(outputfile, index = False)
    except OSError:
        df.to_csv('backup.csv', index = False)
        print('Error writing to output file')
        print('Data written to backup.csv')
        sys.exit()
	
    try:
        with open('errors.txt', 'w') as f:
            f.write(errors)
    except OSError:
        print(errors)
	
	
	
if __name__ == '__main__':
	main(sys.argv[1:])
	
	
	
	
	
