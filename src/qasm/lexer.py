import string


class Lexer:
    word_chars = string.ascii_letters + "." + string.digits
    whitespace = string.whitespace
    single_punctuation_chars = "():;,{}[]'\""
    multi_punctuation_chars = "!=<>-"

    def __init__(self, text):
        self.text = text
        self.tokens = None
        self.lex()

    def lex(self):
        tokens = []
        chars = self.text

        single_line_comment = False
        is_string = False

        buff = []

        punctuation = False
        word = False
        for index, char in enumerate(chars):
            if single_line_comment:
                if char == "\n":
                    single_line_comment = False
                continue

            if char == '"':
                print(f"... {buff}")
                tokens.append(''.join(buff))
                buff = []
                is_string = not is_string
                continue

            if is_string:
                buff.append(char)
                continue

            if char == "#":
                single_line_comment = True

            if char == "/" and chars[index + 1] == "/":
                single_line_comment = True

            if char in Lexer.word_chars:
                if punctuation:
                    tokens.append(''.join(buff))
                    punctuation = False
                    buff = []
                word = True
                buff.append(char)

            if char in Lexer.whitespace:
                word = False
                punctuation = False
                tokens.append(''.join(buff))
                buff = []

            if char in Lexer.single_punctuation_chars:
                punctuation = False
                word = False
                tokens.append(''.join(buff))
                buff = []
                tokens.append(char)

            if char in Lexer.multi_punctuation_chars:
                if word:
                    tokens.append(''.join(buff))
                    word = False
                    buff = []
                punctuation = True
                buff.append(char)
        self.tokens = tokens
