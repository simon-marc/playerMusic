from tkinter import *
import pygame
import os
import threading
import random
import time
from mutagen.mp3 import MP3
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter import ttk
from PIL import Image, ImageTk


                        #L'utilisation de la librarie "threading" a pour but de fluidifier l'exécution de certaines fonctionnalités du player


#Création de la classe
class Player:
    def __init__(self,master):
        self.master = master
        pygame.init()
        pygame.mixer.init()

        #Création du container pour lister les sons
        self.scroll = Scrollbar(master)
        self.play_list = Listbox(master, font="Sasarif 12 bold", bd=5, bg="white", width=37, height=19, selectbackground="#c9c8c5")
        self.play_list.place(x=600 , y=77)
        self.scroll.place(x=946, y=80, height=389, width=15)
        self.scroll.config(command=self.play_list.yview())
        self.play_list.config(yscrollcommand=self.scroll.set)

        #Image de fond du player
        file= "mars.png"
        self.back_img = Image.open(file)
        self.back_img = self.back_img.resize((600, 470), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.back_img)
        self.img_label = Label(master)
        self.img_label.grid(row=0, column=0)
        self.img_label["compound"] = LEFT
        self.img_label["image"] = self.img

        #Symboles et variables du player
        PLAY = "►"
        PAUSE = "║║"
        PREV = "<<"
        NEXT = ">>"
        STOP = "■"
        UNPAUSE = "||"
        mute = "Mute"
        unmute = "unmute"
        vol_mute = 0.0
        vol_unmute = 1

        #Fonction pour ajouter une track
        def add_song():
            try:
                directory = askdirectory()
                os.chdir(directory)
                song_list = os.listdir()
                song_list.reverse()
                for song in song_list:
                    pos= 0
                    if song.endswith(('mp3')):
                        self.play_list.insert(pos, song)
                    pos += 1

                index = 0
                self.play_list.selection_set(index)
                self.play_list.see(index)
                self.play_list.activate(index)
                self.play_list.selection_anchor(index)

            except:
                showerror("File isn't supported !")

        def add_song_playlist():
            threads = threading.Thread(target=add_song())
            threads.start()

        #Fonction pour initialiser le minuteur du lecteur
        def get_time():
            current_time = pygame.mixer.music.get_pos() / 1000
            formated_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
            next_one = self.play_list.curselection()
            song = self.play_list.get(next_one)
            song_timer = MP3(song)
            song_length = int(song_timer.info.length)
            format_for_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            self.label_time.config(text=f"{ format_for_length} / {formated_time}")
            self.progress_bar["maximum"] = song_length
            self.progress_bar["value"] = int(current_time)
            master.after(100, get_time)

        #Fonction pour lancer la track
        def play_music():
            try:
                track = self.play_list.get(ACTIVE)
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()
                get_time()
            except:
                print('')

        def play_thread():
            threads= threading.Thread(target=play_music)
            threads.start()
        master.bind("<space>", lambda x:play_thread())

        #Fonction pour répéter la track
        def repeat_song():
            try:
                index = 0
                self.play_list.select_clear(0, END)
                self.play_list.selection_set(index, last=None)
                self.play_list.see(index)
                self.play_list.activate(index)
                self.play_list.selection_anchor(index)
                track = self.play_list.get(index)
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()

            except:
                showerror("Add a song !")

        def repeat():
            threads = threading.Thread(target=repeat_song)
            threads.start()

        #Fonction pour pouvoir mettre en pause la track (switch visible entre pause et unpause)
        def pause_unpause():
            if self.pause["text"] == PAUSE:
                pygame.mixer.music.pause()
                self.pause["text"] = UNPAUSE
            elif self.pause["text"] == UNPAUSE:
                pygame.mixer.music.unpause()
                self.pause["text"] = PAUSE

        #Fonction destinée à l'arrêt complet du lecteur
        def stop():
            pygame.mixer.music.stop()

        #Fonction destinée à régler le volume
        def volume(x):
            pygame.mixer.music.set_volume(self.volume_slider.get())

        #Fonction pour passer à la track suivante
        def next_song():
            next_one = self.play_list.curselection()
            next_one = next_one[0]+1
            song = self.play_list.get(next_one)
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.play_list.select_clear(0, END)
            self.play_list.activate(next_one)
            self.play_list.selection_set(next_one,last=None)
            self.var.set(song)
            get_time()
            self.play_list.see(next_one)

        def next():
            threads= threading.Thread(target=next_song)
            threads.start()

        #Fonction pour retourner à la track précédente
        def prev_song():
            next_one =self.play_list.curselection()
            next_one = next_one[0]-1
            song = self.play_list.get(next_one)
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.play_list.select_clear(0, END)
            self.play_list.activate(next_one)
            self.play_list.selection_set(next_one,last=None)
            self.var.set(song)
            get_time()
            self.play_list.see(next_one)

        def prev():
            threads= threading.Thread(target=prev_song)
            threads.start()

        ################################################################################################################################################

                                                                       # GUI #

        ################################################################################################################################################

        self.master.bind("<Left>", lambda x:prev())
        self.master.bind("<Right>", lambda x:next())

        self.var = StringVar()
        self.var.set("########################################################################################################################""")
        self.song_title = Label(master, font="Helvetica 12 bold", bg="black", fg="white", width=67, textvariable=self.var)
        self.song_title.place(x=1, y=0)

        self.menu = Menu(self.img_label, font="helvetica, 7")
        master.config(menu=self.menu)

        self.separator = ttk.Separator(self.img_label, orient="horizontal")
        self.separator.place(relx=0, rely=0.87, relwidth=1, relheight=1)

        self.play = Button(self.master, text=PLAY, width=3, bd=5, bg="black", fg="white", font="helvetica, 8", command=play_thread)
        self.play.place(x=140, y=415)

        self.stop = Button(self.master, text=STOP, width=3 , bd=5, bg="black", fg="white", font="helvetica, 8",command=stop)
        self.stop.place(x=200, y=415)

        self.prev = Button(self.master, text=PREV, width=3, bd=5, bg="black", fg="white", font="helvetica, 8", command=prev)
        self.prev.place(x=10, y=415)

        self.next = Button(self.master, text=NEXT, width=5, bd=5, bg="black", fg="white", font="helvetica, 8", command=next)
        self.next.place(x=260, y=415)

        self.pause = Button(self.master, text=PAUSE, width=5, bd=5, bg="black", fg="white", font="helvetica, 8", command=pause_unpause)
        self.pause.place(x=70, y=415)

        self.repeat_button = Button(self.master, text="Rep", width=5, bd=5, bg="black", fg="white", font="helvetica, 8", command=repeat)
        self.repeat_button.place(x=400, y=415)

        self.load_music = Button(self.master, text="Click here to load your track", width=47, bd=5, bg="black", fg="white", font="helvetica, 8", command=add_song_playlist)
        self.load_music.place(x=602, y=45)

        self.style = ttk.Style()
        self.style.configure("myStyle.Horizontal.Tscale",background="#505050")
        self.volume_slider = ttk.Scale(self.img_label, from_=0, to=1, orient=HORIZONTAL,value=1, length=120, style="myStyle.Horizontal.TScale", command=volume)
        self.volume_slider.place(x=475, y=423)

        self.progress_bar = ttk.Progressbar(self.img_label, orient=HORIZONTAL, value=0, length=453, mode='determinate')
        self.progress_bar.place(x=0, y=392)

        self.label_time = Label(master, text="00:00:00 / 00:00:00", width=17, font="helvetica 10", bg="black", fg="white")
        self.label_time.place(x=455, y=392)

        self.label_playlist = Label(master, text="Your Playlist",width=47, height=2, bd=5, font="helvetica 11 bold", bg="white", fg="black")
        self.label_playlist.place(x=602, y=1)


def main():
    root =  Tk()
    ui = Player(root)
    root.geometry("963x470+200+100")
    root.title("playerMusic")
    root.configure(bg="black")
    root.resizable(False,False)
    root.mainloop()

if __name__ == "__main__":
    main()


