from math import *

# remove all the print() because it's much slower with that

# this program assumes: the game's words are all from the database, the ai knows all the words in the database
# a program where the ai would have the list but has to form words on its own would need a few tries and would be a different type of ai with no features or something along those lines, it also wouldn't make sense if the ai didn't know all words when it can scan all the words unless it only scans from previous game data

class Program():
    def __init__(self):
        initial_file = open("words_alpha.txt")
        self.all_words_string = initial_file.read()
        initial_file.close()

        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        self.word_length = 5 # word length (for wordle, it's 5)

        n_of_words = self.convert_txt_to_list(self.word_length) # convert initial text file to a list of words
        print(n_of_words)

        self.frequency_per_spot = self.most_frequent_letter_for_every_spot()
    
        self.letter_occurrences()

        self.letter_occurences_by_occurence_number()

        self.assign_probability_to_every_word(["based_on_alphabet_contained", ""])

    def assign_probability_to_every_word(self, factors):
        all_probabilities = []
        for word in self.all_words_list: # for every word
            prob = 1
            for factor in factors: # for every probability factor
                factor_prob = self.get_factor_probabillity(factor, word) # get the probability from that factor
                prob *= factor_prob

            # print(word, prob)
            all_probabilities.append(prob)
            
        sorted_words = sorted(all_probabilities)

        print(15, "likeliest words:")
        for item in sorted_words[slice(15)]:
            print(self.all_words_list[all_probabilities.index(item)], "with a probability of", item)
        
            
    def get_factor_probabillity(self, factor, word):
        factor_prob = 1
        if factor == "based_on_alphabet_contained":
            frequencies_per_spot = self.frequency_per_spot
            i = 0
            for letter in word:
                letter_index = self.alphabet.index(letter)
                factor_prob *= frequencies_per_spot[i][letter_index]/sum(frequencies_per_spot[i])
                i += 1

        return factor_prob


    def frequency_for_every_word_length(self): # this is does a cool bell curve (une gaussienne)
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
            # print(f"Least used letter at spot {i}: {self.alphabet[most_used_letter.index(min(most_used_letter))]}")
        # print(spots)
        return spots

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

            print(f"Most frequent letter with {j+1} occurence:      {most_used_letter}")
            self.output_probabilities(most_used_letter, 0)
            
    def output_probabilities(self, frequency_list, k):
            sorted_list = sorted(frequency_list, reverse=True)
            sum_list = sum(frequency_list)
            if sum_list == 0:
                sum_list = 1

            for i in range(k): # top k letter stats:
                top_letter = frequency_list.index(sorted_list[k])
                print(f"{self.alphabet[top_letter]} with a probability of {sorted_list[k]/sum_list}")

            
                

Program()





