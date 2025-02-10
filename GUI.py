from tkinter import *  # pip install tkinter
from PIL import Image, ImageTk, ImageSequence  # pip install Pillow
import time
from pygame import mixer  # pip install pygame

mixer.init()

root = Tk()
root.state('zoomed')  # Start the window maximized
root.title("GIF Player")

# Load music and GIF
mixer.music.load("startmusic.mp3")
gif = Image.open("GUI.gif")

lbl = Label(root)
lbl.place(x=0, y=0, relwidth=1, relheight=1)

# Function to display the GIF frame by frame
def play_gif(frame_index=0):
    try:
        gif.seek(frame_index)
        frame = gif.resize((1500, 750))
        img_frame = ImageTk.PhotoImage(frame)
        
        lbl.config(image=img_frame)
        lbl.image = img_frame  # Keep a reference to avoid garbage collection
        
        frame_index = (frame_index + 1) % gif.n_frames
        root.after(80, play_gif, frame_index)  # Update frame every 80ms
    except Exception as e:
        print(f"Error: {e}")

# Start playing music and GIF
mixer.music.play()
play_gif()

root.mainloop()
