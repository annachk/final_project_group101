# Source for the list of passwords: 
# https://www.ncsc.gov.uk/news/most-hacked-passwords-revealed-as-uk-cyber-survey-exposes-gaps-in-online-security

import re
import random
import string
import sys
from argparse import ArgumentParser
import random
import string

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
        self.password = ''
        self.lop = ''
        
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
                print('A greater length is necessary to fulfill all '
                    'requirements while including your suggestion')
            else:
                self.user_suggestion_status = 'Approved'
                print("Your suggestion passed. It will be used when "
                      "generating your password")
                self.generate_password()
            
    def password_requirements(self):
        """ Get password requirements, defined by the service provider,
            from user's input
        
        Returns:
            requirements (dict): the requirements necessary for the password 
            as keys and details as values
        """
        
        requirements = {'1':len(self.suggestion)}
        print('\n--- REQUIREMENTS ---\n'
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
                while True:
                    try:
                        length = int(input('Enter the full amount of characters '
                                        'for the password: '))
                        
                        requirements[pass_req_query] = length
                        break
                    except ValueError:
                        print('Please enter a whole number.')
                        continue
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
        
        Returns:
            Either one:
                lop1_list(list): the suggestion in a list
                lop2_list(list): a list of characters splitted into groups 
                    of random numbers of characters
                lop3_list(list): a list of characters splitted into groups 
                    of one and then randomized
        """
        print('\n--- LEVEL OF PERSONALIZATION ---\n'
                '1 - Suggestion remains unbroken within the password\n'
                '2 - Suggestion is broken apart into groups of random length\n'
                '3 - Suggestion is broken apart into groups of one character\n')
        while True:
            self.lop = input('Select level of security for Password Suggestion '
                        '(1-3), with 1 being least secure and 3 being most '
                        'secure: ')
            if self.lop in ('1','2','3'):
                if self.lop == '1':
                    lop1_list = self.suggestion
                    return lop1_list
                    
                if self.lop == '2':
                    groups_of = random.randint(2, 4)
                    lop2_list = self.suggestion
                    #slice user's suggestion into a pieces, stores into a list
                    lop2_list = [lop2_list[chars:chars + groups_of] 
                                for chars in range(0, len(lop2_list), groups_of)]
                    return lop2_list
                    
                elif self.lop == '3':
                    #slice suggestion, stores into a list,randomizes the list
                    lop3_list = list(self.suggestion)
                    random.shuffle(lop3_list)
                    return lop3_list
                    
            else: 
                continue
        
        
        
    def num(self, pw, insert_range):
        ''' If requirement number 2(num) was chosen,
            this function adds a series of numbers to
            the user's suggestion
        
        Args:
            pw(list): list with user's suggestion
            insert_range(int): the number of characters missing in the password
        
        Side effects:
            changes pw (num_let_sym_list is the increented pw)
            changes insert_range
            
        Returns:
            num_list(list): list with suggestion and added numbers
            insert_range(int): number of characters still missing
        
        '''
        if '3' in self.requirements:
            #guarantees that it will be possible to include req 3
            insert_range -= 1
            range_value = random.randint(1, insert_range)
        else:
            range_value = insert_range
        random_nums = ''.join(["{}".format(random.randint(0, 9)) 
                               for num in range(range_value)])
        #convert the randomly generatred numbers into a list
        num_list = list(random_nums)
        for c in pw:
            #adds user's suggestion into the list
            num_list.insert(len(random_nums), c)
        if self.lop != '1':
            num_list = list(num_list)
            random.shuffle(num_list)
            num_list = ''.join(num_list)
        #updates insert_range
        insert_range -= range_value
        return num_list, insert_range
    
    def let(self, pw, insert_range):
        ''' If requirement number 3(low and upp case letters) was chosen,
            this function adds a series of letters to
            the user's suggestion
        
        Args:
            pw(list): list with user's suggestion
            insert_range(int): the number of characters missing in the password
        
        Side effects:
            changes pw (num_let_sym_list is the increented pw)
            changes insert_range
            
        Returns:
            num_let_sym_list(list): list with suggestion and added letters
            insert_range(int): number of characters still missing
        '''
        if '2' in self.requirements:
            #guarantees that it will be possible to include req 3
            insert_range += 1
            range_value = insert_range
        else:
            range_value = insert_range
            
        alphabet = string.ascii_lowercase + string.ascii_uppercase
        #gives a sequence of random, lower and upper case, letters
        random_let = ''.join([random.choice(alphabet) 
                              for char in range(range_value)])
        #insert_here = random.randint(1, insert_range)
        let_list = list(random_let)
        for c in pw:
            #adds user's suggestion into the list
            let_list.insert(len(random_let), c)
        if self.lop != '1':
            random_let = list(random_let)
            random.shuffle(random_let)
            random_let = ''.join(random_let)
        insert_range -= range_value
        
        return let_list, insert_range
    
    def num_let_sym(self, pw, insert_range):
        ''' If requirement number 4(nums, letters, and symbols) was chosen,
            this function adds a series of numbers, letters, and symbols to
            the user's suggestion
        
        Args:
            pw(list): list with user's suggestion
            insert_range(int): the number of characters missing in the password
        
        Side effects:
            changes pw (num_let_sym_list is the increented pw)
            
        Returns:
            num_let_sym_list(list): list with suggestion and 
                added numbers, letters, and symbols
        '''
        #gives a sequence of random numbers, letters, and symbols
        random_num_let_sym = ''.join([random.choice(string.ascii_letters + 
                                    string.digits + string.punctuation) 
                                    for n in range(insert_range)])
        num_let_sym_list = list(random_num_let_sym)
        for c in pw:
            #adds user's suggestion into the list
            num_let_sym_list.insert(len(random_num_let_sym), c)
        if self.lop != '1':
            num_let_sym_list = list(num_let_sym_list)
            random.shuffle(num_let_sym_list)
            num_let_sym_list = ''.join(num_let_sym_list)
        return num_let_sym_list   
        
    def generate_password(self):
        """ Generates a random password based on the user’s suggestion and 
            password requirements defined by the user
        Returns:
            pw_final(str): final state of the generated password
        """
        pw = self.level_of_personalization()

        #determines the range of the insert
        pw_length = self.requirements['1'] - len(self.suggestion)
        insert_range = pw_length

        if self.user_suggestion_status == "Approved":
            if '4' in self.requirements:
                pw = self.num_let_sym(pw, insert_range)
                #convert this list to a string with no spaces
                pw_final = ''.join(str(i_nls) for i_nls in pw)
                print(f'Password: {pw_final}')
                self.password = pw_final
            else:
                if '2' in self.requirements:
                    pw, insert_range = self.num(pw, insert_range)
                if '3' in self.requirements:
                    pw, insert_range = self.let(pw, insert_range)
                #convert the list to a string with no spaces
                pw_final = ''.join(str(i) for i in pw)
                self.password = pw_final
                print(f'Password: {pw_final}')
            
        else:
            pass
                            
    def password_manager(self):
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
        
        
        while True:
            response = input("Would you like to store your username and "
                         "password in a password manager? Type Y for yes "
                         "or N for no: ")
            if response == "Y":
                with open("pwdmanager.txt","a+") as pwdmanager:
                    account = input("Please enter the account name (ie. Google,"
                                    " Apple, Netflix, etc): ")
                    username = input("Please enter the username/email address "
                                    "for the account: ")
                    pwdmanager.write(f"{account} {username} {self.password}\n")
                    pwdmanager.close()
                    print("Your password information has been stored in "
                          "pwdmanager.txt.")
                    break
            elif response == "N":
                print("Your password will not be saved.")
                break
            else:
                continue
    
    def reset_password(self):
        """ Allows user to get access to other functions of the program and 
            reset existing password if the password 
            is entered incorrectly more than 3 times in the login page;
        
        Returns:
            the newly generated password, if the user decides to reset 
                their password
        """
        filename_manager = "pwdmanager.txt"
        with open(filename_manager, 'r') as f:
            attempts = 1
            is_finished = False
            while attempts < 4 and is_finished == False:
                username = input("Enter username: ")
                password = input("Enter password: ")
                
                for line in f:
                    if username in line and password in line:
                        account = input('Enter account name: ')
                        print(self.find_account("pwdmanager.txt", account))
                        is_finished = True
                        break
                    else:
                        print("The username or password is incorrect. Please try again.")
                        attempts += 1
                        break
               
        if attempts >= 4:
            answer = input("Reset your password? Please enter Y (Yes) or N (No): ")
            if answer == "Y":
                #g.password_requirements = password.password_requirements
                self.generate_password() #should generate a new password
                print("Reset Password Successful.")
            else:
                print(f"Sorry, the password is incorrect.")    
    
    def find_account(self, filename_manager, account):
        """ Allows user to find their username and password in their text file
            when they put in their account type.
        
        Parameters:
            filename_manager (str): contains path to a file of accounts that 
                                    will be read
        
        Argument:
            account (str): type of account user is looking for
                           (i.e. Google, Facebook, Twitter, etc.)
        
        Returns:
            the username and password that corresponds with the account 
            that the user inputs
        """
        with open(filename_manager, 'r') as f:
            total_lines = f.readlines()
            for line in total_lines:
                account_info = line.split()
                if account == account_info[0]:
                    #print(f'Username: {account_info[1]} Password: {account_info[2]}')
                    return f'Username: {account_info[1]} Password: {account_info[2]}'
        return "Account not found."
    

    


def main(suggestion):
    """ Get user's suggestion of what to put in the password, compare the
        suggestion with regularly used passwords and
        either reject it or accept it;
        Generate password based on suggestion and level of personalization
        desired;
        Allows user to save his/her usernames/emails and their respective
        passwords;
        Returns the generated password and, if asked, the previously
        generated passwords, as long as the login and password to access
        such info is correct
    Args:
        suggestion(str): user's suggestion of what to include in the 
        generated password 
    """
    gen = Generator()
   
    print('\n------ PASSWORD GENERATOR ------\n')
    # "password" isn't an acceptable suggestion to be in the pasword. Try "l0ve"
    gen.evaluate_suggestion(suggestion)
    
    print('\n------ PASSWORD MANAGER ------\n')
    gen.password_manager()
    
    print('\n------ PASSWORD FINDER ------\n')
    while True:
        see_passwords = input('Do you want to see your other passwords? '
                              'Please enter Y (Yes) or N (No): ')
        if see_passwords == "Y":
            gen.reset_password()
            break
        elif see_passwords == "N":
            break
        else:
            continue

def parse_args(arglist):
    """ Parse command-line arguments. """
    parser = ArgumentParser(arglist)
    parser.add_argument("suggestion", help="suggestion of a sequence of \
        characters to be used in the password")
    return parser.parse_args(arglist)
    

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.suggestion) 
