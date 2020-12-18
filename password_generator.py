# Source for the list of passwords: 
# https://www.ncsc.gov.uk/news/most-hacked-passwords-revealed-as-uk-cyber-survey-exposes-gaps-in-online-security

import re
import random
import string
import sys
from argparse import ArgumentParser

class Generator:
    """ Get user's suggestion of what to put in the password, 
        compare the suggestion with regularly used passwords 
        and either reject it or accept it;
        Generate password based on suggestion and level of 
        personalization desired by the user.
    """
    
    def __init__(self):
        """ Initializes Generator's attributes"""
        filename = "100000_regularly_used_passwords_breached.txt"
        # all_same stores whole regularly used passwords breached 
        self.all_same = []
        # all_too_similar stores parts of regularly used passwords breached
        self.all_too_similar = []
        self.get_passwords(filename)
        self.suggestion = ''
        self.user_suggestion_status = 'Denied'
        self.requirements = {}
        
    def get_passwords(self, filename):
        ''' Read content from file and put it into two lists, 
            one for whole passwords and the other for parts of passwords
        
        Args:
            filename(str): the path to a file to be read in
        
        Side effects:
            changes the variable "all_same"
            changes the variable "all_too_similar"
        '''
        
        with open(filename, "r", encoding = "utf-8") as f:
            content = f.read()        
            same = (r"(.*\S)")
            too_similar = (r"([0-9]{3,})|([a-zA-Z]{3,})")
            
            self.all_same = [same_words for same_words in 
                            re.findall(same, content) if len(same_words) > 0]
            self.all_too_similar = [part for too_similar_words 
                                    in re.findall(too_similar, content) 
                                    for part in too_similar_words if
                                    len(too_similar_words) > 0 and part != '']
            
        return self.all_same,self.all_too_similar
        
    def evaluate_suggestion(self, suggestion):
        ''' Compare the suggestion provided by the user with the contents  
            in each list created in the get_passwords function and evaluate 
            if it passes or not (if the suggestion is too similar or exactly 
            the same as a password in the .txt file, then reject it)
        
        Args:
            suggestion(str): user's suggestion of what to include in 
            the generated password
            
        Side effects:
            changes the variable "suggestion"
            changes the variable "requirements"
            changes the variable "user_suggestion_status"
        '''
        self.suggestion = suggestion
        
        if self.suggestion in self.all_same:
            print("Exact password found in the regularly used password file")
        elif self.suggestion in self.all_too_similar:
            print("This is part of a regularly used password")
        else:
            self.requirements = self.password_requirements()
            if self.requirements['1'] < (len(self.suggestion) + 
                                         len(self.requirements) - 1):
                print("A greater length is necessary to fulfill all \
                    requirements while including your suggestion.")
            else:
                self.user_suggestion_status = 'Approved'
                print("Your suggestion passed. It will be used when "
                      "generating your password")
            
    def password_requirements(self):
        """ Get password requirements, defined by the service provider,
            from user's input
        
        Returns:
            requirements (dict): the requirements necessary for the password 
            as keys and details as values
        """
        
        requirements = {'1':len(self.suggestion)}
        print('\n------ REQUIREMENTS ------\n'
                '1 - Password length\n'
                '2 - Include numbers\n'
                '3 - Include lowercase and uppercase letters\n'
                '4 - Include mix of letters, numbers, and symbols\n'
                '5 - Done\n')
        while True:
            pass_req_query = input('Enter the number of the requirement(s) '
                                   'necessary for your password found above '
                                   '(one by one) that is not fulfilled by '
                                   'your suggestion: ')
            if pass_req_query == '5':
                break
            elif pass_req_query == '1':
                length = int(input('Enter the full amount of characters '
                                   'for the password: '))
                requirements[pass_req_query] = length
            elif pass_req_query in ['2','3','4']:
                requirements[pass_req_query] = ''
            else:
                print('Invalid input. Try again (1-5).')
                continue
        return requirements
    
    def level_of_personalization(self):
        """ From the user's choices, modify the suggestion based on 
            the classifications of each level of personalization (1-3):
                1: User's suggestion remains unbroken within the password.
                2: User's suggestion is broken apart within the password.
                3: User's suggestion is broken apart
                    and scattered randomly throughout the password.
            This function works together with generate_password()
        """
        
        lop = input('Select level of security for Password Suggestion (1-3), \
            with 1 being least secure and 3 being most secure')
        
        if lop == 2:
            #slice user's suggestion into a pieces, stores into a list
            lop2_list = list(self.suggestion)
            return lop2_list
        elif lop == 3:
            # slice suggestion into pieces, stores into a list
            lop3_list = list(self.suggestion)
            # randomizes the list
            random.shuffle(lop3_list)
            return lop3_list
        
        
        
    def generate_password(self):
        """ Generates a random password based on the user’s suggestion and 
            password requirements defined by the user or, if the suggestion
            was not approved, a totally randomized password
            that agrees with the password requirements
            This function works together with level_of_personalization()
            and password_requirements().
        """
        requirements = self.password_requirements()
        
        alphabet = string.ascii_lowercase + string.ascii_uppercase
        pw_length = requirements[1] - len(self.suggestion)  #pw_length
        
        random_nums = ''.join(["{}".format(random.randint(0, 9)) 
                               for num in range(0, pw_length)])
        random_chars = ''.join(random.choice(alphabet) 
                               for char in range(pw_length))
        insert_range = random.randint(1, pw_length) #insert_range
        
        if self.user_suggestion_status == "Approved":
            if 2 in requirements:
                #convert the randomly generatred numbers into a list.
                num_list = list(random_nums) 
                #adds User's Suggestion into the list at a random index.
                num_list.insert(insert_range, self.suggestion) 
                #convert this list to a string with no spaces
                pw = ''.join(str(i) for i in num_list) 
                return pw #this is the password
                
            if 3 in requirements:
                pw1 = random_chars1.append(lop2_list)
                random.shuffle(pw1)
                #print(random_chars)
                #print(random_chars_list)
                #print("password:")
                #print(pw1)
                return pw1

            if 4 in requirements:
                # add mix of letters, numbers, and symbols to user's suggestion
                pw = random_chars.append(lop3_list)
                pwchars = alphabet + random_nums + string.punctuation
                pw2 = "".join(pwchars) + "".join((pw) for i in range(0, pw_length))
                random.shuffle(pw2)
                return pw2
                pass # this is temporary while there is no code
                
        elif self.user_suggestion_status == "Denied":
            pass      
                            
    def password_manager():
        """ Asks the user if they would like to input their newly generated 
            password into a generated text document to keep track of them.
            The user will be able to input the account type, account 
            username/email, and generated password to store on each line in 
            the text file. The user can elect to not use the password manager
            after they create their passwords.
            
            Args:
                response (str): Whether the user wants to use the password
                    manager or not, Y for yes or N for no
                account (str): the name of the account, ie. Google
                username (str): the username or email for the account
                
            Side effects: 
                Creates and/or updates a text document (pwdmanager.txt)
                with account types, usernames, and passwords.
        """
        response = input("Would you like to store your username and password\
                         in a password manager? Type Y for yes or N for no: ")
        if response == "Y":
            with open("pwdmanager.txt","a+") as pwdmanager:
                account = input("Please enter the account name (ie. Google, \
                                Apple, Netflix, etc: ")
                username = input("Please enter the username/email address \
                                 for the account: ")
                pwdmanager.write(f"{account} {username} {self.pw}\n") 
                #unsure if its pw or self.pw (or generate_password.pw?) ^
                pwdmanager.close()
                print("Your password information has been stored in \
                      pwdmanager.txt.")
        elif response != "Y":
            print("Your password will not be saved.")
    
def find_password(username):
    """Allows user to find their password in their text file when
    they put in their username.
    
    Argument:
    username (str): username of an account
    
    Returns:
    the password that corresponds with the username that the user
    inputs
    """
    with open('pwdmanager.txt', 'r') as f:
        total_lines = f.readlines()
        for line in total_lines:
            account = line.split()
            if username == account[0]:
                print(account[1])
                return account[1]
    print("Username not found.")
    
def reset_password(username,password):
    """ Allows user to reset existing password if the password 
        is entered incorrectly more than 3 times in the login page;
        
    Returns:
        the newly generated password, if the user decides to reset their password
    """
    with open('pwdmanager.txt', 'r') as f:
        username = input("Enter username:")
        password = input("Enter password:")
        attempts = 0
        is_finished = False
        while attempts < 4 and is_finished == False:
            for line in f:
                if username in line and password in line:
                    is_finished = True
                else:
                    print(f"Sorry, the password is incorrect. Please try again.")
                    attempts += 1
                    password = input("Enter password:")
    
    g = Generator()          
    if attempts >= 4:
        answer = input("Reset your password? Please enter Yes or No")
        if answer == "Yes":
            g.password_requirements = password.password_requirements
            new_password = g.generate_password() #should generate a new password
            return new_password
        else:
            print(f"Sorry, the password is incorrect. Please try again.")
    


def main(suggestion):
    """ Get user's suggestion of what to put in the password, compare the
        suggestion with regularly used passwords and
        either reject it or accept it;
        Generate password based on suggestion and level of personalization
        desired;
        Allows user to save his/her usernames/emails and their respective
        passwords;
        Returns the generated password and, if asked, the previously
        generated passwords
    Args:
        suggestion(str): user's suggestion of what to include in the 
        generated password 
    """
    gen = Generator()
    # "password" isn't an acceptable suggestion to be in the pasword. Try "l0ve"
    gen.evaluate_suggestion(suggestion) 
    # ^ test __init__, get_passwords, evaluate_suggestion, password_requirements

def parse_args(arglist):
    """ Parse command-line arguments. """
    parser = ArgumentParser(arglist)
    parser.add_argument("suggestion", help="suggestion of a sequence of \
        characters to be used in the password")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.suggestion) 
