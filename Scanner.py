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

    ErrII = 'Invalid Input'
    ErrIN = 'Invalid Number'
    ErrUCC = 'Unclosed Comment'
    ErrUMC = 'Unmatched Comment'

    FINISHING_STATES = [NUM_C, IKW_C, WS_C, SYM_C, COM_C, ErrII, ErrIN, ErrUCC, ErrUMC]
    ERROR_STATES = [ErrII, ErrIN, ErrUCC, ErrUMC]
    SUCCESS_FINISH_STATES = [NUM_C, IKW_C, WS_C, SYM_C, COM_C]


class Transitioner:
    WS_RXP = '[' + ''.join(Constants.WHITE_SPACES) + ']'
    SYM_RXP = '[' + ''.join(Constants.SYMBOLS) + ']'
    TRANSITIONS = {
        States.START: [
            (f'^\d({WS_RXP}|{"".join(Constants.SYMBOLS)}|{Constants.EOF}]$', States.NUM_C),
            ('^\d.$', States.NUM_R),
            (f'^[A-Za-z]({WS_RXP}|{SYM_RXP}|{Constants.EOF})$', States.IKW_C),
            ('^[A-Za-z].$', States.IKW_R),
            (f'^{WS_RXP}{{2}}$', States.WS_R),
            (f'^{WS_RXP}.$', States.WS_C),
            ('^\/\*$', States.COM_R),
            ('^\*\/$', States.ErrUMC),
            ('^==$', States.SYM_R),
            (f'^[{SYM_RXP}]$', States.SYM_C),
        ],
        States.NUM_R: [
            (f'^\d({WS_RXP}|{"".join(Constants.SYMBOLS)}|{Constants.EOF}]$', States.NUM_C),
            ('^\d.$', States.NUM_R),
            ('^[A-Za-z].$', States.ErrII),
        ],
        States.NUM_C: [
            (f'^[A-Za-z]({WS_RXP}|{SYM_RXP}|{Constants.EOF})$', States.IKW_C),
            ('^[A-Za-z].$', States.IKW_R),
            (f'^{WS_RXP}{{2}}$', States.WS_R),
            (f'^{WS_RXP}.$', States.WS_C),
            ('^\/\*$', States.COM_R),
            ('^\*\/$', States.ErrUMC),
            ('^==$', States.SYM_R),
            (f'^[{SYM_RXP}]$', States.SYM_C),
        ],
        States.IKW_R: [
            (f'^[A-Za-z]({WS_RXP}|{SYM_RXP}|{Constants.EOF})$', States.IKW_C),
            ('^[A-Za-z].$', States.IKW_R),
            ('^\d.$', States.ErrII),
        ],
        States.IKW_C: [
            (f'^\d({WS_RXP}|{"".join(Constants.SYMBOLS)}|{Constants.EOF}]$', States.NUM_C),
            ('^\d.$', States.NUM_R),
            (f'^{WS_RXP}{{2}}$', States.WS_R),
            (f'^{WS_RXP}.$', States.WS_C),
            ('^\/\*$', States.COM_R),
            ('^\*\/$', States.ErrUMC),
            ('^==$', States.SYM_R),
            (f'^[{SYM_RXP}]$', States.SYM_C),
        ],
        States.WS_R: [
            (f'^{WS_RXP}{{2}}$', States.WS_R),
            (f'^{WS_RXP}.$', States.WS_C),
        ],
        States.WS_C: [
            (f'^\d({WS_RXP}|{"".join(Constants.SYMBOLS)}|{Constants.EOF}]$', States.NUM_C),
            ('^\d.$', States.NUM_R),
            (f'^[A-Za-z]({WS_RXP}|{SYM_RXP}|{Constants.EOF})$', States.IKW_C),
            ('^[A-Za-z].$', States.IKW_R),
            ('^\/\*$', States.COM_R),
            ('^\*\/$', States.ErrUMC),
            ('^==$', States.SYM_R),
            (f'^[{SYM_RXP}]$', States.SYM_C),
        ],
        States.SYM_R: [
            (f'^[{SYM_RXP}].$', States.SYM_C),
        ],
        States.SYM_C: [
            (f'^\d({WS_RXP}|{"".join(Constants.SYMBOLS)}|{Constants.EOF}]$', States.NUM_C),
            ('^\d.$', States.NUM_R),
            (f'^[A-Za-z]({WS_RXP}|{SYM_RXP}|{Constants.EOF})$', States.IKW_C),
            ('^[A-Za-z].$', States.IKW_R),
            (f'^{WS_RXP}{{2}}$', States.WS_R),
            (f'^{WS_RXP}.$', States.WS_C),
            ('^\/\*$', States.COM_R),
            ('^\*\/$', States.ErrUMC),
            ('^==$', States.SYM_R),
            (f'^[{SYM_RXP}]$', States.SYM_C),
        ],
        States.COM_R: [
            ('^\*.$', States.COM_HC),
            ('^..$', States.COM_R),
            (f'^.({Constants.EOF})', States.ErrUCC)
        ],
        States.COM_HC: [
            ('^\/.$', States.COM_C),
            ('^\*.$', States.COM_HC),
            ('^..$', States.COM_R)
        ],
        States.COM_C: [
            (f'^\d({WS_RXP}|{"".join(Constants.SYMBOLS)}|{Constants.EOF}]$', States.NUM_C),
            ('^\d.$', States.NUM_R),
            (f'^[A-Za-z]({WS_RXP}|{SYM_RXP}|{Constants.EOF})$', States.IKW_C),
            ('^[A-Za-z].$', States.IKW_R),
            (f'^{WS_RXP}{{2}}$', States.WS_R),
            (f'^{WS_RXP}.$', States.WS_C),
            ('^\/\*$', States.COM_R),
            ('^\*\/$', States.ErrUMC),
            ('^==$', States.SYM_R),
            (f'^[{SYM_RXP}]$', States.SYM_C),
        ]
    }
    
    def __init__(self):
        self.cur_state = States.START


    def transition(self, last_char, lookahead):
        cur_transitions = Transitioner.TRANSITIONS[self.cur_state]
        matched_transition = filter(lambda t: re.match(t[0], last_char + lookahead), cur_transitions)[0]
        self.cur_state = matched_transition[1]
        return self.cur_state


class Scanner:

    def __read_file(self, loc):
        with open(loc, 'r') as file:
            lines = file.readlines()
            return lines


    def __init__(self, 
                 code_source: str ="input.txt",
                 tokens_dest: str ="tokens.txt",
                 error_dest: str ="lexical_errors.txt",
                 symtable_loc: str = "symbol_table.txt"):
        open(symtable_loc, 'a').close()
        self.code_lines = self.__read_file(loc=code_source)
        self.pointer = 0
        self.line_pointer = 0
        self.transitioner = Transitioner()
        self.token_dest = tokens_dest
        self.error_dest = error_dest
        self.symbol_table_loc = symtable_loc
        self.eof_reached = False

    def __write_error(self, message):
        with open(self.error_dest, 'a') as file:
            file.write(f'\nLineNo.{self.line_pointer + 1}: ' + message)

    def symbol_table_get(self, token):
        with open(self.symbol_table_loc, 'r') as file:
            lines = file.readlines
            return filter(lambda l: l.split()[0] == token, lines)[0]
        
    def symbol_table_append(self, token, type):
        with open(self.symbol_table_loc, 'a') as file:
            file.write(f'\n{token} {type}')
            

    def move_one_char_forward(self):
        line = self.code_lines[self.line_pointer]
        if self.pointer == len(line) - 1:
            if self.line_pointer == len(self.code_lines) - 1:
                self.eof_reached = True
            
            self.line_pointer += 1
            self.pointer = 0
        else:
            self.pointer += 1

    def get_pointing_char(self):
        line = self.code_lines[self.line_pointer]
        char = line[self.pointer]
        return char

    def get_lookahead(self):
        line = self.code_lines[self.line_pointer]
        if self.pointer == len(line) - 1:
            if self.line_pointer == len(self.code_lines) - 1:
                return Constants.EOF
            line = self.code_lines[self.line_pointer + 1]
            lookahead = line[0]
            return lookahead
        lookahead = line[self.pointer + 1]
        return lookahead

    def shorten(self, token):
        message = token if len(token) <= 6 else token[:6] + '...'
        return message

    def get_next_token(self):
        last_char = self.get_pointing_char()
        lookahead = self.get_lookahead()
        token = last_char
        state = self.transitioner.transition(last_char, lookahead)
        while not state in States.FINISHING_STATES and not self.eof_reached:
            self.move_one_char_forward()
            last_char = self.get_pointing_char()
            lookahead = self.get_lookahead()
            token += last_char
            state = self.transitioner.transition(last_char, lookahead)
        
        if self.eof_reached:
            return None
        
        
        if state in States.ERROR_STATES:
            token_message = self.shorten(token) if state == States.ErrUCC else token
            self.__write_error(f'({token_message}, {state.value})')
            return self.get_next_token()
        
        if state == States.IKW_C:
            search_res = self.symbol_table_get(token)
            type = "KEYWORD" if token in Constants.KEYWORDS else "ID"
            if not search_res:
                self.symbol_table_append(token, type)

        