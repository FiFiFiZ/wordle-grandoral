from math import *

# remove all the print() because it's much slower with that

class Program():
    def __init__(self):
        initial_file = open("words_alpha.txt")
        self.all_words_string = initial_file.read()
        initial_file.close()

        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        self.word_length = 5 # word length (for wordle, it's 5)

        n_of_words = self.convert_txt_to_list(self.word_length) # convert initial text file to a list of words
        print(n_of_words)

        self.most_frequent_letter_for_every_spot()
    
        self.letter_occurrences()

        self.letter_occurences_by_occurence_number()


    def frequency_for_every_word_length(self): # this is does a cool bell curve
        n_of_words = []
        for i in range(20):
            returned = self.convert_txt_to_list(i)
            n_of_words.append(returned)

        for i in range(len(n_of_words)):
            print(f"{i}: {n_of_words[i]}")

    def convert_txt_to_list(self, word_length): # converts initial text file to the desired usable list
        i = 0
        self.all_words_list = []
        while i < len(self.all_words_string): # for the whole text string
            item = ""
            while self.all_words_string[i] != "\n": # forms a word until it finds an "enter"
                item += self.all_words_string[i]
                i += 1

            if len(item) == word_length: # add only five-letter words
                self.all_words_list.append(item)
                # print(item)
            i += 1 # skip the "enter" found 

        return len(self.all_words_list)

    def most_frequent_letter(self, type=None):
        most_used_letter = self.reset_most_used_letters()

        for item in self.all_words_list:
            for i in range(self.word_length):
                letter = item[i]
                most_used_letter[self.alphabet.index(letter)] += 1 # find letter number in alphabet, add 1 to the frequency of that letter
        

    def reset_most_used_letters(self): # returns an empty "most used letter" list
        most_used_letter = []
        for item in self.alphabet:
            most_used_letter.append(0)

        return most_used_letter

    def most_frequent_letter_for_every_spot(self):
        spots = []
        for i in range(self.word_length):
            most_used_letter = self.reset_most_used_letters()

            for item in self.all_words_list:
                letter = item[i]
                most_used_letter[self.alphabet.index(letter)] += 1

            spots.append(most_used_letter)

            alphabetical_rank_of_most_used_letter = most_used_letter.index(max(most_used_letter))
            # print(f"Most used letter at spot {i}: {self.alphabet[alphabetical_rank_of_most_used_letter]}")
            print(f"Least used letter at spot {i}: {self.alphabet[most_used_letter.index(min(most_used_letter))]}")
        # print(spots)

    def letter_occurrences(self):
        most_used_letter = self.reset_most_used_letters()

        for i in range(len(most_used_letter)):
            letter = self.alphabet[i]
            for item in self.all_words_list:
                most_used_letter[i] += item.count(letter)
                
        print(most_used_letter)

    def letter_occurences_by_occurence_number(self):
        

        for j in range(self.word_length): # up to 6 occurences for a letter

            most_used_letter = self.reset_most_used_letters()
            for i in range(len(most_used_letter)): # for every alphabet letter
                letter = self.alphabet[i]
                for item in self.all_words_list: # count occurences of it in every word
                    occurences = item.count(letter)
                    if occurences == j+1:
                        most_used_letter[i] += occurences

            alphabetical_rank_of_most_used_letter = most_used_letter.index(max(most_used_letter))
            print(f"Most frequent letter with {j+1} occurence: {self.alphabet[alphabetical_rank_of_most_used_letter]}")
            
            
            
                

Program()





