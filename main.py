from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
random_word = ""

df = pd.read_csv("./data/french_words.csv")
to_dict = dict(zip(df["French"], df["English"]))
print(to_dict)


def randomize_word():
     global random_word
     random_word = random.choice(list(to_dict.items()))


def flip_card():
     canvas.create_image(430, 270, image=back_to_img)
     language_label.config(text="English", bg="#91c2af", fg="white")
     word_label.config(text=random_word[1], bg="#91c2af", fg="white")


def next_card():
     # 1) Cancel any flipping if there was any
     global flip
     window.after_cancel(flip)

     # 2) Rerandomize a word
     randomize_word()

     # 3) Flip back to front card display(FRENCH)
     canvas.create_image(430, 270, image=front_to_img)
     language_label.config(text="French", bg="white", fg="black")
     word_label.config(text=random_word[0], bg="white", fg="black")

     # 4) Flip card
     flip = window.after(3000, flip_card)


def remove_word_next_card():
     # 1) Cancel any flipping if there was any
     global flip
     window.after_cancel(flip)

     # 2) Access and update the dataframe and the dictionary
     global df
     global to_dict
     df = df[df['French'] != random_word[0]]
     to_dict = dict(zip(df["French"], df["English"]))
     print(df, to_dict)
     df.to_csv("./data/french_words.csv", index=False)

     # 3) Next card
     next_card()


# --------------------UI------------------------------------
randomize_word()
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, pady=20, padx=20)

# ToImages
front_to_img = PhotoImage(file="./images/card_front.png")
back_to_img = PhotoImage(file="./images/card_back.png")
right_to_img = PhotoImage(file="./images/right.png")
wrong_to_img = PhotoImage(file="./images/wrong.png")


# CANVAS
canvas = Canvas(width=850, height=550)
# NOTE TO SELF: the *args in create_image() are the coordinates on the x and y axis!!
canvas.create_image(430, 270, image=front_to_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=3)

# LABELS
language_label = Label(text="French", font=("Ariel", 40, "italic"), bg="white")
word_label = Label(text=random_word[0], font=("Ariel", 60, "bold"), bg="white")
language_label.place(x=340, y=150)
word_label.place(x=300, y=263)

# BUTTONS
right_button = Button(image=right_to_img, width=70, height=70, highlightthickness=0, command=remove_word_next_card)
right_button.grid(column=0, row=1)

wrong_button = Button(image=wrong_to_img, width=70, height=70, highlightthickness=0, command=next_card)
wrong_button.grid(column=2, row=1)

flip = window.after(3000, flip_card)
window.mainloop()


