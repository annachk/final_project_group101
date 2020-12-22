from password_generator import Generator
import pytest
from pathlib import Path
import builtins
from unittest import mock
#from password_generator import find_password
from sys import stderr

g = Generator()

def test_get_passwords():
    ''' Test the get_passwords() function.
    Side effects:
        Creates and deletes a temporary file
    '''    
    passwords_sample = ("123456\n123456789\nqwerty\n"
                "password\n111111\n12345678\n"
                "abc123\n1234567\npassword1\n"
                "12345")

    filename = "temp_regularly_used_passwords_breached.txt"
    try:
        # create temporary file
        with open(filename, "w", encoding="utf-8") as temp_f:
            temp_f.write(passwords_sample)
        
        result = g.get_passwords(filename)
        
        # check the type of the parts of the return
        assert isinstance(result, tuple), \
            "get_passwords() should return a tuple"
        assert isinstance(result[0], list), \
            "get_passwords()[0] should return a list"
        assert isinstance(result[1], list), \
            "get_passwords()[1] should return a list"
        
        # check length of the parts of the return
        assert len(result) == 2, \
            "get_passwords() should return 2 results"
        assert len(result[0]) == 10, \
            "get_passwords()[0] has an unexpected number of items"
        assert len(result[1]) == 11, \
            "get_passwords()[1] has an unexpected number of items"
        
        # check values of each list
        assert result[0][0] == "123456"
        assert result[0][6] == "abc123"
        assert result[0][8] == "password1"
        assert result[1][0] == "123456"
        assert result[1][6] == "abc"
        assert result[1][9] == "password"
        
    finally:
        try:
            # deletes temporary file
            Path(filename).unlink()
        except:
            pass    
        
def test_password_manager(capsys):
    '''Test the password_manager function.'''
    
    
    with mock.patch("builtins.input",side_effect=['Y','Google','joey@gmail.com']):
        assert g.password_manager() == "Your password information has been saved in pwdmanager.txt."
        captured = capsys.readouterr()
        assert captured.out == ""
    with mock.patch("builtins.input",side_effect=['N']):
        assert g.password_manager() == "Your password will not be saved."
        captured = capsys.readouterr()
        assert captured.out == ""
    with mock.patch("builtins.input",side_effect=['U']):
        assert g.password_manager() == "Your password will not be saved."
        captured = capsys.readouterr()
        assert captured.out == ""

    '''
    with mock.patch("builtins.input",side_effect=['Y','Google','joey@gmail.com']):
        g.password_manager()
        captured = capsys.readouterr()
        assert captured.out == "Your password information has been saved in pwdmanager.txt.\n"
    with mock.patch("builtins.input",side_effect=['N']):
        g.password_manager()
        captured = capsys.readouterr()
        assert captured.out == "Your password will not be saved.\n"
    with mock.patch("builtins.input",side_effect=['U']):
        g.password_manager()
        captured = capsys.readouterr()
        assert captured.out == "Your password will not be saved.\n"
    '''

def test_find_account():
    """Test the find_account function"""
    
    sample_line = ("Google jess123@gmail.com Snowman1\nFacebook anna123@gmail.com finalprojectyey!")
    
    filename_manager = "sample_accounts.txt"
    try:
        with open(filename_manager, "w", encoding="utf-8") as temp_f:
            temp_f.write(sample_line)
        
        assert g.find_account(filename_manager, "Google") == "Username: jess123@gmail.com Password: Snowman1"
        assert g.find_account(filename_manager, "Facebook") == "Username: anna123@gmail.com Password: finalprojectyey!"
        assert g.find_account(filename_manager, "goooogle") == "Account not found."
        assert g.find_account(filename_manager, "jess123@gmail.com") == "Account not found."
    
    finally:
        try:
            Path(filename_manager).unlink()
        except:
            pass
