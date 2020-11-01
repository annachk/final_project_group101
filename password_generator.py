
# Source for the list of passwords: https://www.ncsc.gov.uk/news/most-hacked-passwords-revealed-as-uk-cyber-survey-exposes-gaps-in-online-security

import re

def get_passwords(filename):
    ''' Read content from file and put it in two lists, one for whole passwords and another for parts of passwords
    Args:
        filename(str): path to a file to be read in
    Returns:
        all_same(list): contains whole regularly used passwords breached to access sensitive information 
        all_too_similar(list): contains parts of regularly used passwords breached to access sensitive information
    '''
    
    with open(filename, "r", encoding = "utf-8") as f:
        content = f.read()        
        same = (r".*")
        too_similar = (r"([0-9]{3,})|([a-zA-Z]{3,})")
        
        all_same = [same_words for same_words in re.findall(same, content) if len(same_words) > 0]
        all_too_similar = [part for too_similar_words in re.findall(too_similar, content) for part in too_similar_words if len(too_similar_words) > 0 and part != '']    
        
        #print(all_same, len(all_same))
        #print(all_too_similar, len(all_too_similar))
        
        return all_same, all_too_similar
        
def evaluate_suggestion(filename, suggestion):
    ''' Compare the suggestion provided by the user with the contents in each list created in the get_passwords function and evaluate if it passes or not
    Args:
        filename(str): path to a file to be read in
        suggestion(str): user's suggestion of what to include in the generated password
    '''
    
    all_same = get_passwords(filename)
    all_too_similar = get_passwords(filename)
    
    if suggestion in all_same:
        print("Exact password found in the regularly used password file")
    if suggestion in all_too_similar:
        print("This is part of a regularly used password")
    else:
        print("Your suggestion passed. It will be used when generating your password")

filename = "100000_regularly_used_passwords_breached.txt"
suggestion = ""

evaluate_suggestion(filename, suggestion)



# level of personalization (1-3)
    # 1: sugggestion as a whole in the generated password
    # 2: partially recognizable suggestion in the g.p. at a glance
    # 3: characters/symbols/numbers syggested are used but they are spplitted into parts and scatttered randomly through the p.g.


