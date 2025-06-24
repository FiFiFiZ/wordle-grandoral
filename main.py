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

        self.assign_probability_to_every_word(["based_on_method1", [("i", [3])], [("n", [0])], [("i", [1]), ("k", [2]), ("s", [4])]])

    def assign_probability_to_every_word(self, factors):
        all_probabilities = []
        for word in self.all_words_list: # for every word
            factor_prob = self.get_factor_probabillity(factors, word) # get the probability from that factor
            prob = factor_prob

        
            # below was for when every factor was separate, but now it's used as useful data for every method

            # for factor in factors: # for every probability factor
            #     factor_prob = self.get_factor_probabillity(factor, word) # get the probability from that factor
            #     prob *= factor_prob

            # print(word, prob)
            all_probabilities.append(prob)
            
        sorted_words = sorted(all_probabilities, reverse=True)

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

        elif factor == "based_on_alphabet_contained*":
            frequencies_per_spot = self.frequency_per_spot
            i = 0
            check_repeating_letters = set(list(word)) # turn word into a list, then the list into a set (of unique items only)

            if len(check_repeating_letters) != self.word_length: # if there are repeating letters, return 0
                return 0

            for letter in word:
                letter_index = self.alphabet.index(letter)
                factor_prob *= frequencies_per_spot[i][letter_index]/sum(frequencies_per_spot[i])
                i += 1

        elif factor[0] == "based_on_method1": # method 1: calculates probability of every word, eliminating all impossible cases 
            frequencies_per_spot = self.frequency_per_spot
            i = 0
            black_letters_list = []
            black_letter_position = []
                    
            for black_letter in factor[3]: # for every black letter

                black_letters_list.append("#" + black_letter[0]) # add letter to the list of black letters in this word
                black_letter_position.append([black_letter[1]]) # make a list of positions for which it's black (at the start it's only one position, but with the abscence or presence of yellow letters it will narrow down)

                for black_letter_pos in black_letter[1]:
                    if word[black_letter_pos] == black_letter[0]: # if the black letter is in the word, return 0
                        return 0

            for yellow_letter in factor[2]: # for every yellow letter:
                if word.count(yellow_letter[0]) < len(yellow_letter[1]): # if there are at least as many yellow letters as there are yellow instances of it, it's good (if there are 2 yellow letters, and in the word there's 2 of them, or 3 of them, or more, then it's good), otherwise return 0
                    return 0

                if "#" + yellow_letter[0] in black_letters_list: # if yellow letter is also in black letters (we now know how many instances of the letter there are and where it isn't located)
                    position_index = black_letters_list.index("#" + yellow_letter[0]) # find the letter number in the list
                    black_letters_list[position_index] = yellow_letter[0] # mark it as checked (it's initially under the format "#X" with X being the letter but set it to "X" to tell that there is indeed another yellow instance of it)
                    yellow_letter[1].append(black_letter_position[position_index]) # add the black position to the list of yellow positions
                    black_letter_position[position_index] = yellow_letter[1] # replace black positions with yellow positions (because the letter can't be at those positions)

                for yellow_letter_position in yellow_letter[1]: # for every position of this yellow letter:
                    if word[yellow_letter_position] == yellow_letter[0]: # if for that position, the letter in the word is the yellow letter (which we established it can't be), return 0:
                        return 0
                    
            for valid_letter in factor[1]: # if valid letters fit at their place, keep word

                if "#" + valid_letter[0] in black_letters_list or valid_letter[0] in black_letters_list: # if yellow letter is also in black letters (we now know how many instances of the letter there are and where it isn't located)
                    if valid_letter[0] in black_letters_list:
                        position_index = black_letters_list.index("#" + valid_letter[0])
                    elif "#" + valid_letter[0] in black_letters_list:
                        position_index = black_letters_list.index("#" + valid_letter[0]) # find the letter number in the list
                    black_letters_list[position_index] = valid_letter[0] # mark it as checked (it's initially under the format "#X" with X being the letter but set it to "X" to tell that there is indeed another yellow instance of it)
                    black_letter_position[position_index] = [0, 1, 2, 3, 4]
                    for item in valid_letter[1]:
                        black_letter_position.remove(item)

                for valid_letter_position in valid_letter[1]: # for every position of this valid letter
                    if word[valid_letter_position] != valid_letter[0]: # check if the valid letter is in the word and fits at that spot, if not return 0:
                        return 0

            for letter in black_letters_list:
                if "#" in letter: 
                    black_letter_position[black_letters_list.index(letter)] = [0, 1, 2, 3, 4] # for every unchecked letter (black and never yellow), make it black everywhere
                    if letter[1] in word: # if the letter is in the word (letter[0] is "#" and letter[1] is the letter), return 0
                        print(black_letters_list, word)
                else:
                    for i in black_letter_position[black_letters_list.index(letter)]:
                        for j in i:
                            if word[j] == letter[1]:
                                return 0

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

    def method_try_next_likeliest(self):
        pass

Program()





