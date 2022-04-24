from tkinter import *
import w_s_streamlined as w_s
from ctypes import windll

# Fix blurry text
windll.shcore.SetProcessDpiAwareness(1) 

words_label = None
new_label = None

width = '350'
original_height = '150'
extended_height = '850'
height = original_height
dimensions = f"{width}x{height}"


def focus_next_window(e):
    '''
    Press tab to go to next window
    '''
    e.widget.tk_focusNext().focus() # Focus -> pointer in a text field
    return("break") # prevents class binding from firing. It is this class binding that inserts the tab character, which we don't want

def restart_on_click():
    # Reset all  variables
    w_s.allowed_words_fstring = w_s.allowed_words_OGstring
    w_s.letters_not_in_word = []
    w_s.pat = [".", ".", ".", ".", "."]
    # Reset text
    global words_label, new_label # we need to save object value of labels to be able to completely destroy it
    if new_label is None:
        pass
    else:
        new_label.destroy()
    if words_label is None:
        pass
    else:
        words_label.destroy()
    # Reset size
    global height, original_height # Unfortunately it looks like we can't pass parameters since this function is only passed in (not called with ()) so we need to reference them through global keyword
    if height != original_height:
        height = original_height
        root.geometry(f'{width}x{height}')
    return

    
def filterList(e):
    global words_label, new_label # we need to save object value of labels to be able to completely destroy it
    # get reads from 1.0 to end-1c.
    # 1.0 -> line 1 . character 0 --> start from first character in first line.
    # end-2c -> end at whatever is defined as end (the default) but 2 chars less/before (this is done to remove \n which is last char).
    word = word_tb.get("1.0", "end-1c").lower() # Gets input from word_tb textbox
    info = info_tb.get("1.0", "end-2c").lower() # Gets input from info_tb textbox

    # do calculations from main file
    wordsList = w_s.entireProcess(word, info)
    
    # if new_label exists, destroy it
    if new_label is None:
        pass
    else:
        new_label.destroy()
    # add new_label (previous one would be destroyed if existed)
    new_label = Label(root, text = f"Entered: {word}, Pat: {''.join(w_s.pat)}", fg="white", bg="black", font=('Lucida Bright',12))
    new_label.grid(row=2, column=0, columnspan=2, sticky=W+E)

    # same thing with wordlist label
    if words_label is None:
        pass
    else:
        words_label.destroy()
    words_label = Label(root, text = wordsList, fg="white", bg="black", font=('Lucida Bright',14))
    words_label.grid(row=3, column=0, columnspan=2, sticky=W+E)
    
    # Clear text from textboxes
    word_tb.delete("1.0", END)
    info_tb.delete("1.0", END)

    # Resize window
    global height, extended_height # Unfortunately it looks like we can't pass parameters since this function is only passed in (not called with ()) so we need to reference them through global keyword
    if height != extended_height:
        height = extended_height
        root.geometry(f'{width}x{height}')

# Main window frame
root = Tk()
root.geometry(f'{width}x{height}') # Set dimensions
root.title("Wordle Assistant") # Set title
root.configure(bg="black") # Set background color
root.iconbitmap("wordle_icon.ico") # Set icon
root.resizable(False, False) # Restrict resizing

# Giving columns sizes. For understanding, visit: https://stackoverflow.com/questions/45847313/what-does-weight-do-in-tkinter
for i in range(2):
    root.grid_columnconfigure(i, weight=1)
for i in range(5):
    root.grid_rowconfigure(i, weight=1)

# Labels
word_label = Label(root, text = "Word", fg="white", bg="black", font=('Lucida Bright',12))
word_label.grid(row=0, column=0, sticky=SE)

info_label = Label(root, text = "Letters", fg="white", bg="black", font=('Lucida Bright',12))
info_label.grid(row=1, column=0, sticky=NE)

# Textboxes
word_tb = Text(root, height=1, width=20)
word_tb.grid(row=0, column=1, sticky=SW, padx=10, pady=5)

info_tb = Text(root, height=1, width=20)
info_tb.grid(row=1, column=1, sticky=NW, padx=10, pady=5)

# Restart button
restart_button = Button(root, text = "Restart", fg="white", bg="black", font=('Lucida Bright',12), command=restart_on_click)
restart_button.grid(row=5, column=0, columnspan=2, sticky=W+E)

# Enter key as input calls function.
root.bind("<Return>", filterList)
# Tab key to move to next text_field (source: https://stackoverflow.com/questions/1450180/change-the-focus-from-one-text-widget-to-another)
word_tb.bind("<Tab>", focus_next_window)
info_tb.bind("<Tab>", focus_next_window)

# Main loop continuously updates main window.
root.mainloop()