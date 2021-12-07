# SportsAnalyticsFinalProject
Final project for sports analytics course at Concordia University

Final output of scripts can be found in the /stats folder, along with graphs and my report+presentation.

The 'Final Notebook' jupyter notebook was used for the final processing of the data, ie to get the ASID scores. Its code is also replicated in the graph.py script.

My code can be found in the getCHADS.py, Game.py, Event.py, and graph.py files.

/events folder contains the event data for all games

/Logos folder just contains images that are used when creating the graphs.

To run the getCHADS.py code the json files must be inserted into the /data folder. That data can be found here:
https://github.com/linouk23/NBA-Player-Movements

***Warning - getCHADS takes a very long time to run, be careful when processing large amount of games***
To run the getCHADS code use:
python3 getCHADS.py -d /path/to/directory -o <output_file.csv>

I also modified the main.py script so that it saves the output
To run it use:
python3 main.py --path=Celtics@Lakers.json --event=140 --out=<file_to_save.gif>

Credit for the original code goes to Kostya Linou (https://github.com/linouk23)

