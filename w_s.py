# 6 tries
# Gray -> not in the word, Yellow -> in the word but wrong place, Green -> in the word & right place
# for now, we refer gray to as black for easy intials, G -> Green and B -> Gray
# Start with a random combination of most used letters in the alphabet
# If all are gray, retry but with different letters (going down the most-used-letter frequency hierarchy)
# Continue till we get at least 1 letter
# then start matching words

# THINGS TO DO AFTER BASIC SYSTEM IMPLEMENTATION
    # include a success rate to show off this bot
    # GUI

# remember when we find a Y, find words with that letter NOT IN that place.
# remember when we find a Green, find words with that letter IN that place.

# Imports
from string import printable
import sys
import xlrd
import re

frequencies = open("frequencies_Edited.csv", "r")
allowed_words = open("allowed_answers_freqSorted.txt", "r")
allowed_words_fstring = allowed_words.read().strip()

letters_in_place = [] # green
letters_in_word = [] # yellow
letters_not_in_word = [] # gray/black
negate = []
pat = [".", ".", ".", ".", "."]
found = False

def info_allocator(word, info):
    if len(info) != 5:
        print("Wrong input. Terminated.")
        sys.exit()
    for i in range(5):
        if info[i] in "Gg":
            letters_in_place.append([word[i],i]) # add letter and its index
        elif info[i] in "Yy":
            letters_in_word.append([word[i],i]) # add letter and its index (refer to this index as NOT INDEX, meaning the index with the char associated in this list is not the true index of the char)
        elif info[i] in "Bb":
            letters_not_in_word.append([word[i],i]) # add letter and its index (in case of double letters)
        else:
            print("Wrong input. Terminated.")
            sys.exit()

def doubleLetter_Fixer(): # in place = [[e,4], [e,3]], not in word = [e, e]
    for i in letters_not_in_word:
        for j in letters_in_place:
            if i[0] == j[0]:
                pat[i[1]] = f"[^{i[0]}]" if pat[i[1]] == "." else pat[i[1]].replace(pat[i[1]], pat[i[1]][:2] + f"{i[0]}" + pat[i[1]][2:])
                letters_not_in_word.remove(i)
        for j in letters_in_word:
            if i[0] == j[0]:
                letters_not_in_word.remove(i)

def checkRepetition(k):
            # k = element of letters in word
            count = 0
            for p in letters_in_place:
                if k[0] == p[0]:
                    count += 1
            return count

print("Start")

while True:
    info = "retry"
    word = ""
    while info == "retry":
        word = input("Word input: ").lower()
        info = input("-> ") # e.g. bgybb
    if word.lower() == "true":
        break
    info_allocator(word, info)
    doubleLetter_Fixer()

    for i in letters_not_in_word:
        allowed_words_fstring = allowed_words_fstring.replace(i[0], "") # this will just remove the letter, not the word. but then the word becomes 4 letters so remove any <5letter word
    allowed_words_fstring = '\n'.join(re.findall(".....", allowed_words_fstring)) + "\n" # Words with 5 letters kept, others removed
    
    for j in letters_in_place: # [char, index]
        pat[j[1]] = j[0] # => to the index of the pattern, add the corresponding char
    print("".join(pat))
    allowed_words_fstring = "".join(re.findall("".join(pat) + "\n", allowed_words_fstring)) + "\n" # Include only those words with given letters in place

    # in place = [[e,0]], in word = [[..., ...], [e,1], [..., ...]], not in word = [[e,-1]] || Negatiion (not in word) works fine, but repetition needs to be handled. EDIT: HANDLED.
    for k in letters_in_word:
        let = f"{k[0]}"
        if 1 + checkRepetition(k) > 1:
            let = let+".*"+let
        allowed_words_fstring = "".join(re.findall(f".*{let}.*\n", allowed_words_fstring)) + "\n" # Include only those words with given letters in word

    # add letters negation to indices
    for l in range(len(pat)):
        letters_to_negate = ""
        if "[" in pat[l] or pat[l] == ".": # if pat letter is already modified or is still untouched a.k.a. as long as its not an alphabetical letter (meaning its been decided the letter at THIS index)
            for m in letters_in_word:
                if m[1] == l:
                    letters_to_negate += m[0]
            if letters_to_negate:
                pat[l] = f"[^{letters_to_negate}]"    
    allowed_words_fstring = "".join(re.findall("".join(pat) + "\n", allowed_words_fstring)) + "\n"

    printable_list = allowed_words_fstring.split("\n")
    printable_list.pop(-1)

    for a in printable_list:
        print(f"\t{a}")
    print(letters_not_in_word,"-",letters_in_word,"-", "".join(pat))
    letters_in_word = [] # clearing letters_in_word out for optimization I guess? We don't have to filter the previously filtered in letters again for one of the above loops.

print("Success.")
# Close file
allowed_words.close()
frequencies.close()

# CREDITS
# word_frequency = hackerb9/gwordlist (Github, https://github.com/hackerb9/gwordlist/blob/master/frequency-alpha-gcide.txt)
