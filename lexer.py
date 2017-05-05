from tokens import *
class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token = KEYWORDS.get(result, Token(ID, result))
        return token
    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()


        token = Token(INTEGER, int(result))
        return token

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue


            if self.current_char.isalpha():
                return self._id()



            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '{':
                self.advance()
                return Token(OPENCURLY, "{")

            if self.current_char == "}":
                self.advance()
                return Token(CLOSE_CURLY, "}")

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == ",":
                self.advance()
                return Token(COMA, ',')

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '"':
                self.advance()
                return Token(DOUBLE_QUOTE,'"')

            self.error()

        return Token(EOF, None)

    def next_char_token(self):
        """Returns the next char token and advance pointer (for use while lexing and parsing strings)"""
        if self.current_char is None:
            raise Exception("END OF TEXT")

        elif self.current_char == '\\':
            # The escaped characters
            if self.peek() == 'n':
                self.advance()
                self.advance()
                return Token(ESCAPED_CHAR, "n")
            else:
                # Unrecognized escaped character
                self.error()
        else:
            char = self.current_char
            self.advance()
            return Token(CHAR, char)

    def peek_token(self):
        """This function return the next toke without changing the lexers state (without changing the current token)"""
        old_pos, old_char = self.pos, self.current_char
        token = self.get_next_token()
        self.pos, self.current_char = old_pos, old_char
        return token