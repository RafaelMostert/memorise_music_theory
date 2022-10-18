import numpy as np
import pickle
import sys
import time
import os

"""
A simple command-line program to
Learn key signatures, their signs, scales and chords.
"""

class LearnMusicTheory(object):

    # Master dicts
    key_to_n_sharps = {'C':0,'G':1,'D':2,'A':3,'E':4,'B':5,'F#':6,'C#':7}
    key_to_n_flats = {'F':1,'Bb':2,'Eb':3,'Ab':4,'Db':5,'Gb':6,'Cb':7}
    chord_dict = {'C':'c e g b c',
                  'G':'g b d fis g',
                  'D':'d fis a cis d',
                  'A':'a cis e gis a',
                  'E':'e gis b dis e',
                  'B':'b dis fis ais b',
                  'F#':'fis ais cis eis fis',
                  'C#':'cis eis gis bis cis',
                  'F':'f a c e f',
                  'Bb':'bes d f a bes',
                  'Eb':'es g bes d es',
                  'Ab':'as c es g as',
                  'Db':'des f as c des',
                  'Gb':'ges bes des f ges',
                  'Cb':'ces es ges bes ces'}
    sharp_keys = 'fcgdaeb'
    flat_keys = sharp_keys[::-1]
    relevant_flat_sharp_keys = ''
    dk = {'flat':flat_keys,'sharp':sharp_keys}

    def __init__(self, verbose=False):
        """Set up cache directory and file and start learning cycle."""
        self.verbose=verbose
        project_path = sys.argv[0].replace('keys.py','')
        os.makedirs(os.path.join(project_path,"cache"),exist_ok=True)
        self.savepath = os.path.join(project_path,'cache/saved_probability_dict.pkl')
        if os.path.exists(self.savepath):
            with open(self.savepath, 'rb') as f:
                (self.sharp_probability, self.flat_probability) = pickle.load(f)
            print("[Previous performance loaded from memory.]")
        else:
            self.sharp_probability = {'C':1,'G':1,'D':1,'A':1,'E':1,'B':1,'F#':1,'C#':1/2}
            self.flat_probability = {'F':1,'Bb':1,'Eb':1,'Ab':1,'Db':1,'Gb':1,'Cb':1/2}
        self.d = {'flat':self.key_to_n_flats, 'sharp':self.key_to_n_sharps}
        self.dp = {'flat':self.flat_probability,'sharp':self.sharp_probability}

        self.start_learn_cycle()

    def chose_key_signature(self):
        """Pick a key signature at random"""
        # Flip coin for flat or sharp
        if self.repeat_last_key =='':
            self.flat_or_sharp = np.random.choice(['flat','sharp'])
            #self.flat_or_sharp = 'flat'
        # Choose one of eight keys
        if self.repeat_last_key =='':
            prob_values = np.array(list(self.dp[self.flat_or_sharp].values()))
            self.chosen_key = np.random.choice(list(self.d[self.flat_or_sharp].keys()),
                    p=prob_values/np.sum(prob_values))
        else:
            self.chosen_key = self.repeat_last_key
        # Assign
        self.n= self.d[self.flat_or_sharp][self.chosen_key]
        self.relevant_flat_sharp_keys = self.dk[self.flat_or_sharp][:self.n]
        if self.verbose:
            print(f"Relevant {self.flat_or_sharp} notes:", self.relevant_flat_sharp_keys)

    def check_for_quit(self):
        """Check input to see if user wants to exit the program."""
        if self.input[0] == 'q':
            self.save()
            print("Exiting program.")
            exit()

    def check_n(self): 
        """Check if the user knows how many flats or sharps go with a key signature.
        Example input for the key signature of D would be: '2 flats' or '2flats'
        """
        # Get student input
        print(self.chosen_key)
        print('How many flats or sharps does the key signature above have?')
        self.input = input()
        self.check_for_quit()
        # Parse first character (the number of flats/sharps in the key signature)
        
        try:
            self.inputted_n = int(self.input[0])
            assert 0<=self.inputted_n<=7
        except:
            print("First character of input must be integer between 0 and 7 inclusive.")
            print("Key signature D, for example, requires the following input: 2 flats")
            return False
        inputted_sign = self.input[1:].replace(' ','')


        # Give feedback on number of flats/sharps
        if self.n == 0:
            should_be_sign=''
        elif self.n == 1: 
            should_be_sign = self.flat_or_sharp
        else:
            should_be_sign = self.flat_or_sharp + 's'
        if self.inputted_n==self.n and inputted_sign == should_be_sign:
            if self.verbose:
                print(f"Number of {self.flat_or_sharp}s correct!")
        else:
            print(f"Incorrect. Key signature {self.chosen_key} has {self.n} {self.flat_or_sharp}s.")
            if self.verbose:
                print("inputted sign:", inputted_sign)
            return False

    def check_sharps_flats(self):
        """Check if the user knows which flats or sharps go with a key signature.
        Example input for the key signature of D would be: 'f c' or 'fc'
        """
        print(f"Which {self.flat_or_sharp}s does this key signature have?")
        if self.n > 0:
            self.input = input()
            self.check_for_quit()
            inputted_rest = self.input.replace(",",' ').split(' ')
            # Keep first character of every word only
            if len(inputted_rest)>1:
                if self.verbose:
                    print("inputted_rest", inputted_rest)
                inputted_rest = [w[0] for w in inputted_rest if w !='']
                if self.verbose:
                    print("After processing:", inputted_rest)
            else:
                inputted_rest = inputted_rest[0]
            inputted_rest = ''.join(inputted_rest)
            if self.verbose:
                print("After final processing:", inputted_rest)
        else:
            inputted_rest=''

        # Give feedback on which flats/sharps
        #print("inputted_rest:", inputted_rest, "Compared to:",dk[self.flat_or_sharp])
        if inputted_rest==self.dk[self.flat_or_sharp][:self.n]:
            if self.verbose:
                print(f"All correct!")
        else:
            print(f"Remember: Key signature {self.chosen_key} has the following {self.flat_or_sharp}s:")
            if self.verbose:
                print("inputted_rest:", inputted_rest, "Compared to:",self.dk[self.flat_or_sharp][:self.n] )
            print(f"{' '.join(self.dk[self.flat_or_sharp][:self.n])}")
            return False

    def check_chords(self):
        """Check if the user knows which keys go in the major scale
        of a key signature.
        Example input for the key signature of D would be: 'd fis a cis d'
        """
        # Parse chords
        # Expecting input like so, for D (2sharps fc): 'd fis a cis d'
        print(f"Which notes make up the {self.chosen_key} major scale?")
        self.input = input()
        self.check_for_quit()
        inputted_chord = self.input.replace(",",' ').split(' ')

        if self.verbose:
            print("input vs check chord:",inputted_chord, self.chord_dict[self.chosen_key].split(' '))
        for input_note, reference_note in zip(inputted_chord,self.chord_dict[self.chosen_key].split(' ')):
            if input_note.lower() != reference_note.lower():
                print(f"Incorrect. The answer should be "
                f"\'{self.chord_dict[self.chosen_key].split(' ')}\', not \'{inputted_chord}\'.")
                return False
        if self.verbose:
            print("Major scale correct!")


    def save(self):
        """Save progress."""
        self.dp[self.flat_or_sharp][self.chosen_key] /=2 
        self.repeat_last_key=''
        if self.verbose:
            print("Sharp probabilities:", self.sharp_probability)
            print("Flat probabilities:", self.flat_probability)
        with open(self.savepath, 'wb') as f:
            pickle.dump((self.sharp_probability, self.flat_probability), f)

    def mistake_made(self):
        """Increase probability of picking the key signature for which a mistake was made."""
        self.dp[self.flat_or_sharp][self.chosen_key] *=5 
        self.repeat_last_key=self.chosen_key

    def check_key_signature(self):
        """Check if the user knows which key signature goes with the depicted
        flats or sharps.
        Example input for the depiction of two sharps would be: 'D'
        """
        if self.flat_or_sharp=='sharp':
            t=['-',' ',' ','-',' ',' ','-']
            for i in range(self.n):
                t[i]='#'
            t=''.join(t)

            teken =f"""
        {t[2]}
----{t[0]}-----------------------
              {t[5]}
----------{t[3]}-----------------
      {t[1]}
----------------{t[6]}-----------
            {t[4]}
----------------------------

----------------------------

    """
        else:
            t=['-',' ',' ','-',' ',' ','-']
            for i in range(self.n):
                t[i]='b'
            t=''.join(t)
            teken =f"""
            {t[4]}
----------------{t[6]}-----------
      {t[1]}
----------{t[3]}-----------------
              {t[5]}
----{t[0]}-----------------------
        {t[2]}
----------------------------

----------------------------

    """
        print("Which key signature is depicted below?")
        print(teken)
        self.input = input()
        self.check_for_quit()
        input_key = self.input.replace(" ",'')
        if input_key != self.chosen_key:
            print("Incorrect. The answer is {self.chosen_key} not {input_key}.")
            return False

    def start_learn_cycle(self):
        """Iterate over cycle where the user is asked a number of questions
        about a given key signature or a given staff."""
        self.repeat_last_key=''
        while True:
            print()     
            self.chose_key_signature()
            if np.random.choice([True,False]):
                # Query for a given key signature (in characters)
                success = self.check_n()
                if success==False:
                    self.mistake_made()
                    continue
            else:
                # Query for a given staff
                success = self.check_key_signature()

            success = self.check_sharps_flats()
            if success==False:
                self.mistake_made()
                continue
            success = self.check_chords()
            if success==False:
                self.mistake_made()
                continue
            self.save()

                
myLearnMusicTheory = LearnMusicTheory()
