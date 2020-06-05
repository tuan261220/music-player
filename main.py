from tkinter import  *
import tkinter.messagebox
from  tkinter import  filedialog
import os
from pygame import mixer
from tkinter import ttk
from mutagen.mp3 import MP3
import threading
import time
from ttkthemes import themed_tk as tk
from PIL import ImageTk
from PIL import Image
import stagger
import io

mixer.init()

# Global variables
playlist = []
paused = False
muted = False
index = 0
btnState = False

# making tkinter window
root = tk.ThemedTk()
root.get_themes()
root.set_theme("breeze")
root.geometry('800x450')
root.title('Music')
root.iconbitmap(r'C:\Users\DELL\PycharmProjects\python\Project\hnet.com-image.ico')

# browse file in computer
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


# add file to playlist,musicbox
def add_to_playlist(filename):
    playlist.append(filename)
    Musicbox.delete(0, END)
    for song in playlist:
        Musicbox.insert(END, os.path.basename(song))

# author
def about_us():
    tkinter.messagebox.showinfo('About Music','Built using Python by @WarEnd and @Tungto')

# del song in music box and playlist
def del_song():
    selected_song = Musicbox.curselection()
    selected_song = int(selected_song[0])
    Musicbox.delete(selected_song)
    playlist.pop(selected_song)

# change picture in GUi
def change_picture(song):
    mp3 = stagger.read_tag(song)
    by_data = mp3[stagger.id3.APIC][0].data
    im = io.BytesIO(by_data)

    #set size picture in app
    imageFile = Image.open(im).resize((300, 180),Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(imageFile)

    # change picture when music next and previous
    ImageLabel.configure(image=photo)
    ImageLabel.image = photo

# cal time in file mp3
def show_details(song):
    file_data = os.path.splitext(song)

    if file_data[1] == '.mp3':
        audio = MP3(song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(song)
        total_length = a.get_length()


    mins,secs = divmod(total_length,60)
    mins = round(mins)
    secs = round(secs)
    timeFormat = '{:02d}:{:02d}'.format(mins,secs)
    TimeLabel['text'] = "Total length" + '-' + timeFormat

    t1 = threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current = 0
    while current <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current, 60)
            mins = round(mins)
            secs = round(secs)
            timeFormat = '{:02d}:{:02d}'.format(mins, secs)
            CurrentTime['text'] = "CurrentTime" + '-' + timeFormat
            time.sleep(1)
            current+=1


# play music
def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusBar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            global  i
            selected_song = Musicbox.curselection()
            i = int(selected_song[0])
            play_it = playlist[0]
            mixer.music.load(play_it)
            mixer.music.play()
            statusBar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            change_picture(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Music could not find the file. Please check again.')


# stop music
def stop_music():
    mixer.music.stop()
    TimeLabel['text'] = 'Total length : --:--'
    CurrentTime['text'] = 'Current Time: --:--'
    statusBar['text'] = 'Stop Music'

# pause music
def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusBar['text'] = 'Pause music'

#previous music
def rewind_music():
    global i
    i -= 1
    if (i >= 0 ):
        stop_music()
        time.sleep(1)
        mixer.music.load(playlist[i])
        mixer.music.play()
        statusBar['text'] = "Playing music" + ' - ' + os.path.basename(playlist[i])
        show_details(playlist[i])
        change_picture(playlist[i])
    else:
        i = 0
        stop_music()
        time.sleep(1)
        mixer.music.load(playlist[0])
        mixer.music.play()
        statusBar['text'] = "Playing music" + ' - ' + os.path.basename(playlist[0])
        show_details(playlist[0])
        change_picture(playlist[i])

# next music
def next_music():
    global i
    i+=1
    if(i < len(playlist)):
        stop_music()
        time.sleep(1)
        mixer.music.load(playlist[i])
        mixer.music.play()
        statusBar['text'] = "Playing music" + ' - ' + os.path.basename(playlist[i])
        show_details(playlist[i])
        change_picture(playlist[i])
    else :
        i = 0
        stop_music()
        time.sleep(1)
        mixer.music.load(playlist[0])
        mixer.music.play()
        statusBar['text'] = "Playing music" + ' - ' + os.path.basename(playlist[0])
        show_details(playlist[0])
        change_picture(playlist[i])

# Set volume
def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE

#Set volume deafault
def set_vol(val):
    volume = scale.get()
    mixer.music.set_volume(volume/100)

# Closing app
def on_closing():
    stop_music()
    root.destroy()


#Status bar in the bottom
statusBar = Label(root,text = 'Welcom',relief  = SUNKEN,anchor = W)
statusBar.pack(side = BOTTOM, fill  = X)

# Menu bar - all the menu_cascades and menu_commands.
MenuBar = Menu(root)
root.config(menu = MenuBar)

# Open Menu : open file and exit app
OpenMenu = Menu(MenuBar, tearoff = 0)
MenuBar.add_cascade(label = 'File',menu = OpenMenu)
OpenMenu.add_command(label = 'Open',command = browse_file)
OpenMenu.add_command(label = 'Exit', command=root.destroy)

# Help menu : About Author
HelpMenu = Menu(MenuBar, tearoff = 0)
MenuBar.add_cascade(label = 'Help' ,  menu = HelpMenu)
HelpMenu.add_command(label = 'About Us',command = about_us)

# Left frame in app
LeftFrame = Frame(root)
LeftFrame.pack(side = LEFT,padx = 30)

# music box
Musicbox = Listbox(LeftFrame)
Musicbox.pack()

# add music
AddButton = ttk.Button(LeftFrame,text = "Add",command=browse_file)
AddButton.pack(side = LEFT)

# del music
DelButton = ttk.Button(LeftFrame,text = 'Delete',command=del_song)
DelButton.pack(side = LEFT)

# right frame in app
RightFrame = Frame(root)
RightFrame.pack()

topFrame = Frame(RightFrame)
topFrame.pack()

# time music
TimeLabel = Label(topFrame,text = 'Total length : --:--')
TimeLabel.pack(pady = 5)

# time when music ran
CurrentTime = Label(topFrame,text = 'Current Time: --:--',relief = GROOVE)
CurrentTime.pack()

#loading waiting choose music image
img = ImageTk.PhotoImage(file = 'music-and-multimedia.png')

# image waiting
ImageLabel = Label(topFrame,image = img,borderwidth = 1,relief="groove")
ImageLabel.pack(pady = 30)

middleFrame = Frame(root)
middleFrame.pack(side = BOTTOM,pady = 40,padx = 10)

# loading photo play music
photoPlay = PhotoImage(file='arrow.png')

# button play music
Playbtn = ttk.Button(middleFrame,image = photoPlay,command = play_music)
Playbtn.grid(row = 0,column = 1)

# loading photo pause music
photoPause = PhotoImage(file = 'pause.png')

# button pause music
PauseBtn = ttk.Button(middleFrame,image = photoPause,command = pause_music)
PauseBtn.grid(row = 0,column = 2)

# loading photo  stop music
photoStop = PhotoImage(file = 'stop.png')

# button stop music
StopBtn = ttk.Button(middleFrame,image = photoStop,command = stop_music)
StopBtn.grid(row = 0,column = 3)

# loading photo previous music
rewindPhoto = PhotoImage(file='rewind.png')

#button previous music
rewindBtn = ttk.Button(middleFrame, image=rewindPhoto,command = rewind_music)
rewindBtn.grid(row=0,column=0)

# loading photo next music
NextPhoto = PhotoImage(file='next.png')

# button next music
NextBtn = ttk.Button(middleFrame, image=NextPhoto,command = next_music)
NextBtn.grid(row=0,column=4)

# loading photo mute volumn
mutePhoto = PhotoImage(file = 'mute.png')

# loading photo sound
volumePhoto = PhotoImage(file = 'sound.png')

# button mute and sound music
volumeBtn = ttk.Button(middleFrame,image = volumePhoto, command=mute_music)
volumeBtn.grid(row = 0,column = 5)

# set default volumn
scale = ttk.Scale(middleFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0,column=6,pady=15,padx=30)


root.mainloop()