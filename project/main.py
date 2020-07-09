from tkinter import  *
import tkinter.messagebox
import os
import pygame
from tkinter.filedialog import askopenfilenames
from tkinter import ttk
from mutagen.mp3 import MP3
import threading
import time
from ttkthemes import themed_tk as tk
from PIL import ImageTk
from PIL import Image
import stagger
import io

pygame.init()

class MusicPlayer(Frame):
    def __init__(self, master):
        super(MusicPlayer, self).__init__(master)

        self.playlist = []
        self.paused = False
        self.muted = False
        self.index = 0
        self.btnState = False

        # Status bar in the bottom
        self.statusBar = Label(root, text='Welcom', relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)

        # Menu bar - all the menu_cascades and menu_commands.
        self.MenuBar = Menu(root)
        root.config(menu=self.MenuBar)

        # Open Menu : open file and exit app
        self.OpenMenu = Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label='File', menu=self.OpenMenu)
        self.OpenMenu.add_command(label='Open', command=self.browse_file)
        self.OpenMenu.add_command(label='Exit', command=root.destroy)

        # Help menu : About Author
        self.HelpMenu = Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label='Help', menu=self.HelpMenu)
        self.HelpMenu.add_command(label='About Us', command=self.about_us)

        # Left frame in app
        self.LeftFrame = Frame(root)
        self.LeftFrame.pack(side=LEFT, padx=30)

        # music box
        self.Musicbox = Listbox(self.LeftFrame)
        self.Musicbox.pack()

        # add music
        self.AddButton = ttk.Button(self.LeftFrame, text="Add", command=self.browse_file)
        self.AddButton.pack(side=LEFT)

        # del music
        self.DelButton = ttk.Button(self.LeftFrame, text='Delete', command=self.del_song)
        self.DelButton.pack(side=LEFT)

        # right frame in app
        self.RightFrame = Frame(root)
        self.RightFrame.pack()

        self.topFrame = Frame(self.RightFrame)
        self.topFrame.pack()

        # time music
        self.TimeLabel = Label(self.topFrame, text='Total length : --:--')
        self.TimeLabel.pack(pady=5)

        # time when music ran
        self.CurrentTime = Label(self.topFrame, text='Current Time: --:--', relief=GROOVE)
        self.CurrentTime.pack()

        # loading waiting choose music image
        # img = ImageTk.PhotoImage(file=r'C:\Users\Dell\PycharmProjects\MusicPlayer\image\music-and-multimedia.png')

        # image waiting
        self.ImageLabel = Label(self.topFrame, image=img, borderwidth=1, relief="groove")
        self.ImageLabel.pack(pady=30)

        self.middleFrame = Frame(root)
        self.middleFrame.pack(side=BOTTOM, pady=40, padx=10)

        # loading photo play music
        # photoPlay = PhotoImage(file=r'C:\Users\Dell\PycharmProjects\MusicPlayer\image\arrow.png')

        # button play music
        self.Playbtn = ttk.Button(self.middleFrame, image=photoPlay, command=self.play_music)
        self.Playbtn.grid(row=0, column=1)

        # loading photo pause music
        # photoPause = PhotoImage(file=r'C:\Users\Dell\PycharmProjects\MusicPlayer\image\pause.png')

        # button pause music
        self.PauseBtn = ttk.Button(self.middleFrame, image=photoPause, command=self.pause_music)
        self.PauseBtn.grid(row=0, column=2)

        # loading photo  stop music
        # photoStop = PhotoImage(file=r'C:\Users\Dell\PycharmProjects\MusicPlayer\image\stop.png')

        # button stop music
        self.StopBtn = ttk.Button(self.middleFrame, image=photoStop, command=self.stop_music)
        self.StopBtn.grid(row=0, column=3)

        # loading photo previous music
        # rewindPhoto = PhotoImage(file=r'C:\Users\Dell\PycharmProjects\MusicPlayer\image\rewind.png')

        # button previous music
        self.rewindBtn = ttk.Button(self.middleFrame, image=rewindPhoto, command=self.rewind_music)
        self.rewindBtn.grid(row=0, column=0)

        # loading photo next music
        # NextPhoto = PhotoImage(file=r'C:\Users\Dell\PycharmProjects\MusicPlayer\image\next.png')

        # button next music
        self.NextBtn = ttk.Button(self.middleFrame, image=NextPhoto, command=self.next_music)
        self.NextBtn.grid(row=0, column=4)

        # loading photo random
        # randomPhoto = PhotoImage(file=r'C:\Users\Dell\PycharmProjects\MusicPlayer\image\random.png')

        # button random music
        # self.RandomBtn = ttk.Button(self.middleFrame, image=randomPhoto, command=self.random_music())
        # self.RandomBtn.grid(row=0, column=5)

        # loading photo mute volumn
        # mutePhoto = PhotoImage(file=r'C:\Users\Dell\PycharmProjects\MusicPlayer\image\mute.png')

        # loading photo sound
        # volumePhoto = PhotoImage(file=r'C:\Users\Dell\PycharmProjects\MusicPlayer\image\sound.png')

        # button mute and sound music
        self.volumeBtn = ttk.Button(self.middleFrame, image=volumePhoto, command=self.mute_music)
        self.volumeBtn.grid(row=0, column=6)

        # set default volumn
        self.scale = ttk.Scale(self.middleFrame, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol)
        self.scale.set(70)
        pygame.mixer.music.set_volume(0.7)
        self.scale.grid(row=0, column=7, pady=15, padx=30)

        # set event to not predefined value in pygame
        self.SONG_END = pygame.USEREVENT + 1

    def browse_file(self):
        global filename_path
        filename_path = askopenfilenames()
        self.add_to_playlist(filename_path)

    # add file to playlist,musicbox
    def add_to_playlist(self, filename):
        for files in filename:
            self.playlist.append(files)
        self.Musicbox.delete(0, END)
        for song in self.playlist:
            self.Musicbox.insert(END, os.path.basename(song))

    # author
    def about_us(self):
        tkinter.messagebox.showinfo('About Music', 'Built using Python by @WarEnd and @tunggto')

    # del song in music box and playlist
    def del_song(self):
        selected_song = self.Musicbox.curselection()
        selected_song = int(selected_song[0])
        self.Musicbox.delete(selected_song)
        self.playlist.pop(selected_song)

    # change picture in GUi
    def change_picture(self, song):
        mp3 = stagger.read_tag(song)
        by_data = mp3[stagger.id3.APIC][0].data
        im = io.BytesIO(by_data)

        # set size picture in app
        imageFile = Image.open(im).resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(imageFile)

        # change picture when music next and previous
        self.ImageLabel.configure(image=photo)
        self.ImageLabel.image = photo

    # cal time in file mp3
    def show_details(self, song):
        file_data = os.path.splitext(song)

        if file_data[1] == '.mp3':
            audio = MP3(song)
            total_length = audio.info.length
        else:
            a = pygame.mixer.Sound(song)
            total_length = a.get_length()

        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeFormat = '{:02d}:{:02d}'.format(mins, secs)
        self.TimeLabel['text'] = "Total length" + '-' + timeFormat

        t1 = threading.Thread(target=self.start_count, args=(total_length,))
        t1.start()

    def start_count(self, t):
        # global paused
        current = 0
        while current <= t and pygame.mixer.music.get_busy():
            if self.paused:
                continue
            else:
                mins, secs = divmod(current, 60)
                mins = round(mins)
                secs = round(secs)
                timeFormat = '{:02d}:{:02d}'.format(mins, secs)
                self.CurrentTime['text'] = "CurrentTime" + '-' + timeFormat
                time.sleep(1)
                current += 1

    # play music
    def play_music(self):

        if self.paused:
            pygame.mixer.music.unpause()
            self.statusBar['text'] = "Music Resumed"
            self.paused = FALSE
        else:
            try:
                self.stop_music()
                time.sleep(1)
                selected_song = self.Musicbox.curselection()
                self.index = int(selected_song[0])
                play_it = self.playlist[self.index]
                pygame.mixer.music.load(play_it)
                pygame.mixer.music.play(1, 0.0)
                self.statusBar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
                self.change_picture(play_it)
                self.show_details(play_it)
            except:
                tkinter.messagebox.showerror('File not found', 'Music could not find the file. Please check again.')


    # stop music
    def stop_music(self):
        pygame.mixer.music.stop()
        self.TimeLabel['text'] = 'Total length : --:--'
        self.CurrentTime['text'] = 'Current Time: --:--'
        self.statusBar['text'] = 'Stop Music'

    # pause music
    def pause_music(self):
        # global paused
        self.paused = True
        pygame.mixer.music.pause()
        self.statusBar['text'] = 'Pause music'

    # previous music
    def rewind_music(self):
        # global i
        self.index -= 1
        if (self.index >= 0):
            self.stop_music()
            time.sleep(1)
            pygame.mixer.music.load(self.playlist[self.index])
            pygame.mixer.music.play()
            self.statusBar['text'] = "Playing music" + ' - ' + os.path.basename(self.playlist[self.index])
            self.show_details(self.playlist[self.index])
            self.change_picture(self.playlist[self.index])
        else:
            self.index = 0
            self.stop_music()
            time.sleep(1)
            pygame.mixer.music.load(self.playlist[0])
            pygame.mixer.music.play()
            self.statusBar['text'] = "Playing music" + ' - ' + os.path.basename(self.playlist[0])
            self.show_details(self.playlist[0])
            self.change_picture(self.playlist[self.index])

    # next music
    def next_music(self):
        if self.index + 1 < len(self.playlist):
            self.stop_music()
            time.sleep(1)
            pygame.mixer.music.load(self.playlist[self.index + 1])
            pygame.mixer.music.play()
            self.statusBar['text'] = "Playing music" + ' - ' + os.path.basename(self.playlist[self.index + 1])
            self.show_details(self.playlist[self.index + 1])
            self.change_picture(self.playlist[self.index + 1])
            self.index+=1
        else:
            self.index = 0
            self.stop_music()
            time.sleep(1)
            pygame.mixer.music.load(self.playlist[0])
            pygame.mixer.music.play()
            self.statusBar['text'] = "Playing music" + ' - ' + os.path.basename(self.playlist[0])
            self.show_details(self.playlist[0])
            self.change_picture(self.playlist[0])


    # Play random music
    def random_music(self):
        index = 0

    # Set volume
    def mute_music(self):
        if self.muted:
            pygame.mixer.music.set_volume(0.7)
            self.volumeBtn.configure(image=volumePhoto)
            self.scale.set(70)
            self.muted = FALSE
        else:
            pygame.mixer.music.set_volume(0)
            self.volumeBtn.configure(image=mutePhoto)
            self.scale.set(0)
            self.muted = TRUE

    # Set volume deafault
    def set_vol(self, val):
        volume = self.scale.get()
        pygame.mixer.music.set_volume(volume / 100)

    # Closing app
    def on_closing(self):
        self.stop_music()
        root.destroy()

# making tkinter window
root = tk.ThemedTk()
root.get_themes()
root.set_theme("breeze")
root.geometry('1000x600')
root.title('Music')
root.iconbitmap('hnet.com-image.ico')

volumePhoto = PhotoImage(file='sound.png')
photoPlay = PhotoImage(file='arrow.png')
img = ImageTk.PhotoImage(file='music-and-multimedia.png')
photoPause = PhotoImage(file='pause.png')
rewindPhoto = PhotoImage(file='rewind.png')
NextPhoto = PhotoImage(file='next.png')
mutePhoto = PhotoImage(file='mute.png')
photoStop = PhotoImage(file='stop.png')
# randomPhoto = PhotoImage(file='random.png')

app = MusicPlayer(root)
app.mainloop()





