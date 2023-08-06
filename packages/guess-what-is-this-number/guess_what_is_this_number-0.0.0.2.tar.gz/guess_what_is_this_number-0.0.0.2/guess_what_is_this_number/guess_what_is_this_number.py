# number guessing game
import random



class Guess_Number():

    """ A number guessing Game. Start the game usning Guess_Number().start_game()
    
    Attributes:
    none
    
    """

    
    def __init__(self):
        self.random_number = 0
        self.guess = 0
        self.no_of_tries = 0
    
    def get_random(self):
        """Function to get a random number between 0 and 100

        Args: 
            None

        Returns: 
            int: random number
            
        """


        self.random_number = random.randint(0,100)
        return self.random_number
    
    
    def get_input_from_user(self):
        """Function to get guess from user. Also checks validity of input.

        Args: 
            None

        Returns: 
            int: user guess between 0 and 100.
            
        """


        while (1):
            txt = '\n\nNumber of tries: ' + str(self.no_of_tries) + '\nEnter mumber between 0-100: '
            input_val = input(txt)
            if input_val.isdigit():
                input_val = int(input_val)
                if input_val>=0 and input_val<=100:
                    self.guess = input_val
                    self.no_of_tries = self.no_of_tries+1
                    return self.guess
                else:
                    print('Number of tries: ',self.no_of_tries,'\nError! Number not in range.  Please enter number between 0-100')
            else:
                print('Number of tries: ',self.no_of_tries,'\nError! Not a number.  Please enter number between 0-100')
    

    def check_player_guess(self):
        """Function to check players guess.

        Args: 
            None

        Returns: 
            int: 1 if guess is correct. 0 if wrong guess.
            
        """


        if self.guess == self.random_number:
            print('**************************')
            print('    Hurray! You Won in ',self.no_of_tries,' tries')
            print('**************************')
            return 1
        elif self.guess > self.random_number:
            print('You guessed HIGH. Try to guess low number')
            return 0
        elif self.guess < self.random_number:
            print('You guessed LOW. Try to guess high number')
            return 0
        
    def start_game(self):
        
        """Main game function loop.

        Args: 
            None

        Returns: 
            none
            
        """
        self.random_number = self.get_random()
        while(1):
            self.guess = self.get_input_from_user()

            result = self.check_player_guess()

            if result == 1 :
                return 

    def __repr__(self):
        
        """ Repr unction 

        Args:
            None

        Returns:
            string: instructions oin how to start.

        """
   
        return "Start the game usning Guess_Number().start_game()"   
                    