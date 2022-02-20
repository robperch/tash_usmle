## FUNCTIONS TO READ THROUGH ALL THE VIDEOS AND ORGANIZE THEIR DATA





"----------------------------------------------------------------------------------------------------------------------"
############################################# Imports ##################################################################
"----------------------------------------------------------------------------------------------------------------------"


"--- Standard library imports ---"
import os

"--- Third party imports ---"
from moviepy.editor import VideoFileClip
import pandas as pd

"--- Local application imports ---"
from pkg_dir.config import *
from pkg_dir.src.parameters import *






"----------------------------------------------------------------------------------------------------------------------"
############### Reading through all the video files stored locally #####################################################
"----------------------------------------------------------------------------------------------------------------------"


## Reading through all the video files and store names and durations in a list
def videos_entries_list():
    """
    Reading through all the video files and store names and durations in a list

    :return videos_entries: (list) list of tuples containing topics, subtopics, videos and durations
    """


    ## Dictionary comprehension to build nested dict
    videos_entries = [

        (
            topic,
            subtopic,
            video,
            VideoFileClip(usmle_2020_videos_path + "/" + topic + "/" + subtopic + "/" + video).duration/60
        )

        for topic in os.listdir(usmle_2020_videos_path) if ".DS_Store" not in topic
        for subtopic in os.listdir(usmle_2020_videos_path + "/" + topic) if ".DS_Store" not in subtopic
        for video in os.listdir(usmle_2020_videos_path + "/" + topic + "/" + subtopic) if ".mp4" in video

    ]


    return videos_entries



## Creating a dataframe from the video data stored as tuples
def video_data_to_df(videos_entries, save_csv):
    """
    Creating a dataframe from the video data stored as tuples

    :param videos_entries: (list) list of tuples containing topics, subtopics, videos and durations
    :param save_csv: (boolean) condition to specify if the df is saved locally as a csv file
    :return dfx: (dataframe) df with all data arranged in dataframe
    """


    ## Generating dataframe from tuples
    dfx = pd.DataFrame(videos_entries)

    ## Assigning the df's column names based
    dfx.columns = videos_df_colnames

    ## Rounding the length values (mins)
    dfx["video_length_[mins]"] = round(dfx["video_length_[mins]"], 2)

    ## Adding column with the video length time in hours
    dfx["video_length_[hrs]"] = round(dfx["video_length_[mins]"]/60, 2)

    ## Sorting values
    dfx.sort_values(by=["topic", "subtopic", "video"], inplace=True)
    
    ## Restarting index
    dfx.reset_index(inplace=True, drop=True)

    ## Saving a local copy of the df
    if save_csv:
        dfx.to_csv(usmle_videos_csv_copy_path + usmle_2020_videos_df_filename)


    return dfx





"----------------------------------------------------------------------------------------------------------------------"
"----------------------------------------------------------------------------------------------------------------------"
############################################# END OF FILE ##############################################################
"----------------------------------------------------------------------------------------------------------------------"
"----------------------------------------------------------------------------------------------------------------------"
