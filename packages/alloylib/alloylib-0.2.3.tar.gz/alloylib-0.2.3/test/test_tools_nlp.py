
import pytest
from alloy.tools import convert_word_list_to_num_str


def parser_helper(incoming_str):
    return convert_word_list_to_num_str(incoming_str.split(' '))


def test_converting_digits():
    assert parser_helper('one') == '1'
    assert parser_helper('one one') == '11'
    assert parser_helper('one nine four three two') == '19432'
    assert parser_helper('zero') == '0'
    assert parser_helper('four two two one') == '4221'
    assert parser_helper('zero zero zero') == '000'

def test_converting_one_number():
    assert parser_helper('eleven') == '11'
    assert parser_helper('eleven thousand') == '11000'
    assert parser_helper('one hundred') == '100'
    assert parser_helper('one hundred and one') == '101'
    assert parser_helper('one hundred one') == '101'
    assert parser_helper('one hundred twenty one') == '121'
    assert parser_helper('five hundred ninety four') == '594'
    assert parser_helper('five two twenty four') == '5224'
    assert parser_helper('fifty two two four') == '5224'
    assert parser_helper('ninety five') == '95'
    assert parser_helper('one thousand ninety five') == '1095'
    assert parser_helper('one hundred thousand') == '100000'  
    assert parser_helper('one hundred eighteen') == '118'
    assert parser_helper('one hundred and fifty thousand twenty one') == '150021'
    assert parser_helper('one hundred and fifty thousand and twenty one') == '150021'
    assert parser_helper('one hundred one thousand') == '101000'
    assert parser_helper('one hundred and one thousand') == '101000'
    assert parser_helper('one hundred one and thousand') == '101000'
    assert parser_helper('two thousand five hundred twenty') == '2520'
    assert parser_helper('two thousand five hundred') == '2500'
    assert parser_helper('nine hundred ninety nine thousand nine hundred ninety nine') == '999999'

def test_converting_multiple_numbers():
    assert parser_helper('twenty twenty') == '2020'
    assert parser_helper('twenty nineteen') == '2019'
    assert parser_helper('one hundred one eight') == '1018'
    assert parser_helper('one hundred one twenty') == '10120'
    assert parser_helper('eleven twelve thirteen fourteen') == '11121314'
    assert parser_helper('eleven sixty') == '1160'
