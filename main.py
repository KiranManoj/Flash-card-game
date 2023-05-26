
# ------------------------------ Packages ----------------------------------------
from tkinter import *
import pandas
from random import *


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
# ------------------------------- Button Functionality -----------------------------------------

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    try:
        current_card = choice(to_learn)
    except IndexError:
        canvas.itemconfig(card_title, text="Well done")
        canvas.itemconfig(card_word, text="No more words to learn", font=("Ariel", 50, "italic"))
        known_button.destroy()
        unknown_button.destroy()
    else:
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=current_card["French"], fill="black")
        canvas.itemconfig(card_background, image=front_card_img)
        flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_card_img)
    
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv")
    next_card()
    

# ------------------------------- UI setup-----------------------------------------

# Window set up

window = Tk()
window.title("Flash card Project")
window.config(padx=50, pady=50, bg= BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Canvas for images 

canvas = Canvas(width=800, height=526)

front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_card_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card() # inorder to fill the canvas with random frnch words.

window.mainloop()

