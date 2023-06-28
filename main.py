import tkinter as tk
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
language_file = "./data/french_words.csv"

# create word list from csv file
try:
    words_list = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    words_list = pandas.read_csv(language_file)

words_dict = words_list.to_dict(orient="records")
random_word ={}


def flashcard(word):
    language_1 = list(word.keys())[0]
    language_2 = list(word.keys())[1]

    if canvas.itemcget(text_1, "text") == language_1:
        # change to backside
        canvas.itemconfigure(text_1, text=language_2, fill="white")
        canvas.itemconfigure(text_2, text=word[language_2], fill="white")
        canvas.itemconfig(canvas_picture, image=image_back)
    else:
        # change to front side
        canvas.itemconfigure(text_1, text=language_1, fill="black")
        canvas.itemconfigure(text_2, text=word[language_1], fill="black")
        canvas.itemconfig(canvas_picture, image=image_front)


def get_word():
    global timer, random_word
    root.after_cancel(timer)
    random_word = random.choice(words_dict)
    # to get language - it's the first key in the dictionary
    # change list of all keys to list and get first position from the list
    language = list(random_word.keys())[1]

    canvas.itemconfigure(text_1, text=language)
    canvas.itemconfigure(text_2, text=random_word[language])

    timer = root.after(3000, flashcard, random_word)

    flashcard(random_word)


def remove_word():
    global random_word
    words_dict.remove(random_word)
    print(random_word)
    words_dict_new_df = pandas.DataFrame(words_dict)
    words_dict_new_df.to_csv("./data/words_to_learn.csv",  index=False)
    get_word()


root = tk.Tk()
root.title("Flashcard app")
root.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

timer = root.after(3000, flashcard, random_word)

image_front = tk.PhotoImage(file="./images/card_front.png")
image_back = tk.PhotoImage(file="./images/card_back.png")

# flashcards
canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
canvas_picture = canvas.create_image(400, 263, image=image_front)

# text on the flashcard - we don't need text= attribute because we change it right away
text_1 = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
text_2 = canvas.create_text(400, 263, font=("Arial", 60, "bold"))

# buttons
image_ok = tk.PhotoImage(file="./images/right.png")
image_nok = tk.PhotoImage(file="./images/wrong.png")

button_ok = tk.Button(image=image_ok, highlightthickness=0, relief="ridge", command=remove_word)
button_ok.grid(column=0, row=1)

button_nok = tk.Button(image=image_nok, highlightthickness=0, relief="ridge", command=get_word)
button_nok.grid(column=1, row=1)

get_word()

root.mainloop()
