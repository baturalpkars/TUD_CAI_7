import os, requests
import sys
import csv
import glob
import pathlib
from SaR_gui import visualization_server
from worlds1.WorldBuilder import create_builder
from pathlib import Path
from loggers.OutputLogger import output_logger

if __name__ == "__main__":
    fld = os.getcwd()
    print("\nEnter one of the task types 'tutorial' or 'official':")
    choice1=input()
    print("\nEnter a name or id for the human agent:")
    choice2=input()
    if choice1=='tutorial':
        builder = create_builder(task_type='tutorial',condition='tutorial', name=choice2, folder=fld)
    else:
        print("\nEnter one of the human conditions 'normal', 'strong', or 'weak':")
        choice3=input()
        if choice3=='normal' or choice3=='strong' or choice3=='weak':
            builder = create_builder(task_type=choice1, condition=choice3, name=choice2, folder=fld)
        else:
            print("\nWrong condition name entered")

    # Start overarching MATRX scripts and threads, such as the api and/or visualizer if requested. Here we also link our own media resource folder with MATRX.
    media_folder = pathlib.Path().resolve()
    builder.startup(media_folder=media_folder)
    print("Starting custom visualizer")
    vis_thread = visualization_server.run_matrx_visualizer(verbose=False, media_folder=media_folder)
    world = builder.get_world()
    print("Started world...")
    builder.api_info['matrx_paused'] = False
    world.run(builder.api_info)
    print("DONE!")
    # current_file = folder + '/beliefs/currentTrustBelief.csv'
    # all_file = folder + '/beliefs/allTrustBeliefs.csv'
    #
    # # Write the current trust beliefs (overwrite)
    # with open(current_file, mode='w', newline='') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     writer.writerow(['name', 'task', 'competence', 'willingness'])
    #     for name, tasks in trustBeliefs.items():
    #         for task, values in tasks.items():
    #             writer.writerow([name, task, values['competence'], values['willingness']])
    #
    # # Append the trust beliefs to `allTrustBeliefs.csv` (long-term memory)
    # with open(all_file, mode='a', newline='') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     for name, tasks in trustBeliefs.items():
    #         for task, values in tasks.items():
    #             writer.writerow([name, task, values['competence'], values['willingness']])
    print("Shutting down custom visualizer")
    r = requests.get("http://localhost:" + str(visualization_server.port) + "/shutdown_visualizer")
    vis_thread.join()
    if choice1=="official":
        # Generate one final output log file for the official task type
        output_logger(fld)
    builder.stop()
