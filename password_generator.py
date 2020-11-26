
# Source for the list of passwords: https://www.ncsc.gov.uk/news/most-hacked-passwords-revealed-as-uk-cyber-survey-exposes-gaps-in-online-security

import re

class Generator:
    """ Get user's suggestion of what to put in the password, 
        compare the suggestion with regularly used passwords and either reject it or accept it;
        Generate password based on suggestion and level of personalization desired
    """
    def __init__(self):
        """ Initializes Generator's attributes"""
        
        self.filename = "100000_regularly_used_passwords_breached.txt"
        # all_same stores whole regularly used passwords breached to access sensitive information 
        self.all_same = []
        # all_too_similar stors parts of regularly used passwords breached to access sensitive information
        self.all_too_similar = []
        self.get_passwords()
        
    def get_passwords(self):
        ''' Read content from file and put it in two lists, 
            one for whole passwords and another for parts of passwords
        
        Args:
            filename(str): path to a file to be read in
        '''
        
        with open(self.filename, "r", encoding = "utf-8") as f:
            content = f.read()        
            same = (r".*")
            too_similar = (r"([0-9]{3,})|([a-zA-Z]{3,})")
            
            self.all_same = [same_words for same_words in re.findall(same, content) if len(same_words) > 0]
            self.all_too_similar = [part for too_similar_words in re.findall(too_similar, content) 
                                    for part in too_similar_words if len(too_similar_words) > 0 and part != '']    
            
            
    def evaluate_suggestion(self, suggestion):
        ''' Compare the suggestion provided by the user with the contents in each list created 
            in the get_passwords function and evaluate if it passes or not 
            (if the suestion is too similar or exactly the same as a password in the .txt file, then reject it)
        
        Args:
            filename(str): path to a file to be read in
            suggestion(str): user's suggestion of what to include in the generated password
        '''
        
        #all_same = self.get_passwords()
        #all_too_similar = self.get_passwords()
        #self.get_passwords()
        
        if suggestion in self.all_same:
            print("Exact password found in the regularly used password file")
        if suggestion in self.all_too_similar:
            print("This is part of a regularly used password")
        else:
            #print(self.all_same)
            print("Your suggestion passed. It will be used when generating your password")

    def password_requirements(self):
        """ Get password requirements, defined by the service provider, from user's input
        
        Returns:
            requirements (dict): requirements necessary for the password as keys and details as values
        """
        
        requirements = {}
        print('\n------ REQUIREMENTS ------\n'
                '1 - Min number of caracters\n'
                '2 - Include numbers\n'
                '3 - Include lowercase and uppercase letters\n'
                '4 - Have a mix of letters, numbers & symbols\n'
                '5 - Done\n')
        while True:
            pass_req_query = input('Enter the number of the requirement necessary'
                                    'for your password found above (one by one):')
            if pass_req_query == '5':
                break
            elif pass_req_query == '1':
                min_length = int(input('Min number of caracters: '))
                requirements[pass_req_query] = min_length
            elif pass_req_query in ['2','3','4']:
                requirements[pass_req_query] = ''
            else:
                print('This option is not valid. Try again.')
                continue
        return requirements
    
    def level_of_personalization():
        """ From user's choice, modify the suggestion based on the classifications 
            of each level of personalization (goes from 1-3):
                1: sugggestion as a whole in the generated password
                2: partially recognizable suggestion in the g.p. at a glance
                3: characters/symbols/numbers syggested are used but 
                they are spplitted into parts and scatttered randomly through the p.g.
            This function works together with generate_password()
        
        """
    
    def generate_password():
        """ Generate a random password based on the user’s suggestion and password requirements defined by the user
            or, if the suggestion was not approved, 
            a totally randomized password that agrees with the password requirements
            This function works together with level_of_personalization() and password_requirements()
        
        """
        
    def report_unaccepted_suggestion():
        """ Report to the user that his/her suggestion was not approved and why; 
            has options to either input another suggestion or get a totally randomized password
        
        """
        
    def reset_password():
        """Allows user to reset existing passwords;
        Returns the newly generated password, if the user decides to reset their password.
        """

class Manager:
    """Allows user to save his/her usernames/emails and their respective passwords;
        If asked, returns the previously generated passwords
    """        
    def password_manager():
        """ Asks the user if they would like to input their newly generated passwords 
            into a text document to keep track of them.
            The user will be able to input the account type, username/email, 
            and generate a password to store on each line in the text file.
            The user can elect to not use the password manager after they create their passwords."""


def main():
    """ Get user's suggestion of what to put in the password, 
        compare the suggestion with regularly used passwords and either reject it or accept it;
        Generate password based on suggestion and level of personalization desired;
        Allows user to save his/her usernames/emails and their respective passwords;
        Returns the generated password and, if asked, the previously generated passwords
    """
    #gen = Generator()
    #suggestion = "Anna"
    #gen.evaluate_suggestion(suggestion)
    

main()    



