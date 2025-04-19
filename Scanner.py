from functools import reduce
from enum import Enum
import re


class Constants:
    KEYWORDS = ["if", "else", "void", "int", "while", "break", "return"]
    SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<', '==']
    WHITE_SPACES = [' ', '\n', '\r', '\t', '\v', '\f']
    COMMENT_OPEN = '/*'
    COMMENT_CLOSE = '*/'
    EOF = 'EOF'

class States(Enum):
    START = 'Start'
    NUM_R = 'Number Read'
    IKW_R = 'Id/Keyword Read'
    WS_R = 'White Space Read'
    SYM_R = 'Symbol Read'
    COM_R = 'Comment Read'

    NUM_C = 'Number Complete'
    IKW_C = 'ID/Keyword Complete'
    WS_C = 'White Space Complete'
    SYM_C = 'Symbol Complete'
    COM_C = 'Comment Complete'

    ErrII = 'Error: Invalid Input'
    ErrUCC = 'Error: Unclosed Comment'
    ErrUMC = 'Error: Unmatched Comment'


class Transitioner:
    WS_RXP = '[' + ''.join(Constants.WHITE_SPACES) + ']'
    SYM_RXP = '[' + ''.join(Constants.SYMBOLS) + ']'
    TRANSITIONS = {
        States.START: [
            (f'^\d({WS_RXP}|{''.join(Constants.SYMBOLS)}{Constants.EOF}]$', States.NUM_C)
            ('^\d.$', States.NUM_R),
            (f'^[A-Za-z]({WS_RXP}|{SYM_RXP}|{Constants.EOF})$', States.IKW_C),
            ('^[A-Za-z].$', States.IKW_R),
            (f'^{WS_RXP}{{2}}$', States.WS_R),
            (f'^{WS_RXP}.$', States.WS_C)
            ('^\/\*$', States.SYM_R),
            ('^\*\/$', States.ErrUMC),
            ('^==$', States.SYM_R),
            (f'^[{SYM_RXP}]$', States.SYM_C),

        ]
    }
    
    def __init__(self):
        self.cur_state = States.START


    def get_next_state(sefl, two_char):



class Matcher:
    cur_state = States.START


class Scanner:

    def __init__(self, source_location: str ="input.txt"):
        self.initialize_symbol_table()
        self.code
        self.pointer = 0
        self.matchers = self.initialize_matchers()

    def get_next_char(self):
        pass

    def get_look_ahead(self):
        pass
    
    def token_matcher(self, token, lookahead):
        token_plus_lookahead = token + lookahead
        lookahead_matchers = [
            self.match_NUM(token_plus_lookahead),
            self.match_ID(token_plus_lookahead),
            self.match_KEYWORD(token_plus_lookahead),
            self.match_SYMBOL(token_plus_lookahead),
            self.match_COMMENT(token_plus_lookahead),
            self.match_WHITESPACE(token_plus_lookahead)
            ]
        any_match = reduce(lambda x, y: x or y, lookahead_matchers)
        
        if any_match:
            return None
        
        token_matchers = [
            (self.match_NUM(token), "TOKEN"),
            (self.match_ID(token), "ID"),
            (self.match_KEYWORD(token), "KEYWORD"),
            (self.match_SYMBOL(token), "SYMBOL"),
            (self.match_COMMENT(token), "COMMENT"),
            (self.match_WHITESPACE(token), "WHITESPACE")
        ]
        match = next(filter(lambda x: x[0], token_matchers), None)
        return match
    
    def get_lookahead(self):
        pass

    def get_next_token(self):
        token = self.get_next_char()
        lookahead = self.get_look_ahead()
        match = self.token_matcher(token, lookahead)
        while not match:
            token += self.get_next_char()
            match = self.token_matcher(token, lookahead)
        self.update_parameters(match)
        return token

    def match_NUM(self, token):
        pattern = re.compile("^[0-9]+$")
        match = pattern.match(token)
        return match and (token, "NUM")

    def match_ID(self, token):
        pattern = re.compile("^([A-Z]|[a-z])([A-Z]|[a-z]|[0-9])*")
        match = pattern.match(token)
        return match and (token, "ID")

    def match_KEYWORD(self, token):
        match = token in self.KEYWORDS
        return match and (token, "KEYWORD")

    def match_SYMBOL(self, token):
        match = token in self.SYMBOLS
        return match and (token, "SYMBOL")

    def match_COMMENT(self):
        pattern_1 = re.compile("^/*[^(\/*)]*\*/$")

    def match_WHITESPACE(self):
        pass

