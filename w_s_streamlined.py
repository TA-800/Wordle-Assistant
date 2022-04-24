import sys
import re

allowed_words = open("allowed_answers_freqSorted.txt", "r")
allowed_words_fstring = allowed_words.read().strip()
allowed_words_OGstring = allowed_words_fstring # Save in case for restart
allowed_words.close()

letters_not_in_word = [] # gray/black
pat = [".", ".", ".", ".", "."]


def info_allocator(word, info):
    global letters_not_in_word
    letters_in_place, letters_in_word = [], []
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
    return letters_in_place, letters_in_word

def doubleLetter_Fixer(letters_in_place, letters_in_word): # in place = [[e,4], [e,3]], not in word = [e, e]
    global letters_not_in_word
    for i in letters_not_in_word:
        for j in letters_in_place:
            if i[0] == j[0]:
                pat[i[1]] = f"[^{i[0]}]" if pat[i[1]] == "." else pat[i[1]].replace(pat[i[1]], pat[i[1]][:2] + f"{i[0]}" + pat[i[1]][2:])
                letters_not_in_word.remove(i)
        for j in letters_in_word:
            if i[0] == j[0]:
                letters_not_in_word.remove(i)


def checkRepetition(k, letters_in_place):
            # k = element of letters in word
            count = 0
            for p in letters_in_place:
                if k[0] == p[0]:
                    count += 1
            return count

def entireProcess(word, info):
    global allowed_words_fstring, letters_not_in_word, pat
    
    letters_in_place, letters_in_word = info_allocator(word, info)
    doubleLetter_Fixer(letters_in_place, letters_in_word)

    for i in letters_not_in_word:
        allowed_words_fstring = allowed_words_fstring.replace(i[0], "")
    allowed_words_fstring = '\n'.join(re.findall(".....", allowed_words_fstring)) + "\n"
    
    for j in letters_in_place:
        pat[j[1]] = j[0]
    print("".join(pat))
    allowed_words_fstring = "".join(re.findall("".join(pat) + "\n", allowed_words_fstring)) + "\n"

    for k in letters_in_word:
        let = f"{k[0]}"
        if 1 + checkRepetition(k, letters_in_place) > 1:
            let = let+".*"+let
        allowed_words_fstring = "".join(re.findall(f".*{let}.*\n", allowed_words_fstring)) + "\n"

    # add letters negation to indices
    for l in range(len(pat)):
        letters_to_negate = ""
        if "[" in pat[l] or pat[l] == ".":
            for m in letters_in_word:
                if m[1] == l:
                    letters_to_negate += m[0]
            if letters_to_negate:
                pat[l] = f"[^{letters_to_negate}]"    
    allowed_words_fstring = "".join(re.findall("".join(pat) + "\n", allowed_words_fstring)) + "\n"

    
    print("Final Filter:", len(allowed_words_fstring)-1)

    printable_list = allowed_words_fstring.split("\n")
    printable_list.pop(-1)
    print("List form:", len(printable_list)-1)

    printable_string = ""
    for a in printable_list[:25]:
        printable_string += f"{a}\n"
    printable_string = printable_string[:-1]
    print("".join(pat))
    return printable_string
