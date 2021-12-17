import groupy
import re
from time import sleep, time
from QueueEngine import queueSong, playlistData, removeSong, clearPlaylist, songStatus

groups = groupy.Group.list()
for group in groups:
    if "30294367" in group.id: #30294367
        break

PLAYLIST_ID = 0
uri_grab = r"https://open\.spotify\.com/track/(\w+)"
DJBot_Active = 0
numQueue = 0
tracklist = []
a = time()
botList = groupy.Bot.list()
for bot in botList:
    if "DJBot" in bot.name:
        break

current_uri = "0"
while True:
    try:
        messages = group.messages()
        message = messages.newest
        sleep(0.2)
        track_uri_search = re.search(uri_grab, message.text)
        if track_uri_search is not None and DJBot_Active:
            if time() - a > 180 and numQueue > 0:
                a = time()
                numQueue = numQueue - 1
            if message.is_from_me() and 'Veto' in message.text:
                trackname, numQueue = removeSong(track_uri_search.group(1), numQueue)  # remove song vetoed
                bot.post("Make better choices next time. " + trackname + " removed.")
            elif 'spotify:track:' + track_uri_search.group(1) not in tracklist:
                trackname, numQueue = queueSong(track_uri_search.group(1), numQueue)
                bot.post(trackname + " will be on soon!")
                tracklist += ['spotify:track:' + track_uri_search.group(1)]
            else:
                bot.post("We've already played that song tonight, or its coming up soon!")
        elif track_uri_search is not None:
            bot.post("I'm not playing right now. Try again later.")
        if message.is_from_me(): #master controls
            if "Go()" in message.text:
                DJBot_Active = 1
                bot.post("Let's party!")
                tracklist = playlistData()
                a = time()
                current_uri = songStatus() #have to start playback before go() TODO: Maybe try/catch if fail to just get first song in list?
            elif "Gg()" in message.text:
                DJBot_Active = 0
                numQueue = 0
                tracklist = []
                bot.post("Good night yall!")
            elif "Reset()" in message.text: #TODO: test
                bot.post("Recalibrating things. Hang on a minute.")
                numQueue = 0
                clearPlaylist()
                tracklist = playlistData()
                DJBot_Active = 1
                a = time()
                current_uri = songStatus() #have to start playback before go()
    except Exception as e:
        print(e)
