from password_generator import Generator
import pytest

g = Generator()

def test_get_passwords():
    """
    Test the function get_passwords() - check for type and 
    the existence of information inside the returned tuple of lists
    """
    assert isinstance(g.get_passwords(), tuple), "get_passwords() should return a tuple"
    assert isinstance(g.get_passwords()[0], list), "should return a list"
    assert isinstance(g.get_passwords()[1], list), "should return a list"
    
    assert len(g.get_passwords()[0]) > 0
    assert len(g.get_passwords()[1]) > 0
    
