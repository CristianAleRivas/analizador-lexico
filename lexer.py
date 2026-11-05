
from dataclasses import dataclass
from typing import List, Union


@dataclass
class Token:
    type: str
    lexeme: str
    line: int
    column: int


@dataclass
class LexicalError:
    message: str
    line: int
    column: int


LexicalItem = Union[Token, LexicalError]


class Lexer:
    RESERVED_WORDS = {
        "if": "PR_IF",
        "else": "PR_ELSE",
        "while": "PR_WHILE",
        "return": "PR_RETURN",
        "int": "PR_INT",
        "float": "PR_FLOAT",
        "void": "PR_VOID",
        "char": "PR_CHAR",
        "double": "PR_DOUBLE",
        "for": "PR_FOR",
        "do": "PR_DO",
        "break": "PR_BREAK",
        "continue": "PR_CONTINUE",
    }

    TWO_CHARACTER_OPERATORS = {
        "==": "OP_EQ",
        "!=": "OP_NE",
        "<=": "OP_LE",
        ">=": "OP_GE",
    }

    ONE_CHARACTER_TOKENS = {
        "+": "OP_PLUS",
        "-": "OP_MINUS",
        "*": "OP_MULTIPLY",
        "/": "OP_DIVIDE",
        "<": "OP_LT",
        ">": "OP_GT",
        "=": "OP_ASSIGN",
        "(": "LPAREN",
        ")": "RPAREN",
        "{": "LBRACE",
        "}": "RBRACE",
        ",": "COMMA",
        ";": "SEMICOLON",
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.index = 0
        self.line = 1
        self.column = 1
        self.items: List[LexicalItem] = []

    def tokenize(self) -> List[LexicalItem]:
        while not self._at_end():
            char = self._current()

            if char in " \t\f\v":
                self._advance()
            elif char in "\r\n":
                self._advance()
            elif self._starts_with("//"):
                self._skip_line_comment()
            elif self._starts_with("/*"):
                self._skip_block_comment()
            elif self._is_identifier_start(char):
                self._read_identifier()
            elif char.isascii() and char.isdigit():
                self._read_number()
            elif char == '"':
                self._read_string()
            elif self._read_operator_or_delimiter():
                continue
            else:
                self.items.append(
                    LexicalError(
                        "Carácter no reconocido {!r}".format(char),
                        self.line,
                        self.column,
                    )
                )
                self._advance()

        return self.items

    def _at_end(self) -> bool:
        return self.index >= len(self.source)

    def _current(self) -> str:
        return self.source[self.index]

    def _starts_with(self, text: str) -> bool:
        return self.source.startswith(text, self.index)

    def _advance(self) -> str:
        char = self._current()
        if char == "\r":
            self.index += 1
            if not self._at_end() and self._current() == "\n":
                self.index += 1
            self.line += 1
            self.column = 1
        elif char == "\n":
            self.index += 1
            self.line += 1
            self.column = 1
        else:
            self.index += 1
            self.column += 1
        return char

    @staticmethod
    def _is_identifier_start(char: str) -> bool:
        return (
            char == "_"
            or "a" <= char <= "z"
            or "A" <= char <= "Z"
        )

    @classmethod
    def _is_identifier_part(cls, char: str) -> bool:
        return cls._is_identifier_start(char) or (
            char.isascii() and char.isdigit()
        )

    def _read_identifier(self) -> None:
        start_index = self.index
        line, column = self.line, self.column
        while not self._at_end() and self._is_identifier_part(self._current()):
            self._advance()

        lexeme = self.source[start_index:self.index]
        token_type = self.RESERVED_WORDS.get(lexeme, "ID")
        self.items.append(Token(token_type, lexeme, line, column))

    def _read_number(self) -> None:
        start_index = self.index
        line, column = self.line, self.column

        while (
            not self._at_end()
            and self._current().isascii()
            and self._current().isdigit()
        ):
            self._advance()

        token_type = "INT_LITERAL"
        if (
            not self._at_end()
            and self._current() == "."
            and self.index + 1 < len(self.source)
            and self.source[self.index + 1].isascii()
            and self.source[self.index + 1].isdigit()
        ):
            token_type = "FLOAT_LITERAL"
            self._advance()
            while (
                not self._at_end()
                and self._current().isascii()
                and self._current().isdigit()
            ):
                self._advance()

        if not self._at_end() and self._is_identifier_start(self._current()):
            while not self._at_end() and self._is_identifier_part(self._current()):
                self._advance()
            lexeme = self.source[start_index:self.index]
            self.items.append(
                LexicalError(
                    "Número mal formado {!r}".format(lexeme),
                    line,
                    column,
                )
            )
            return

        lexeme = self.source[start_index:self.index]
        self.items.append(Token(token_type, lexeme, line, column))

    def _read_string(self) -> None:
        start_index = self.index
        line, column = self.line, self.column
        self._advance()

        while not self._at_end():
            char = self._current()
            if char == '"':
                self._advance()
                lexeme = self.source[start_index:self.index]
                self.items.append(Token("STRING_LITERAL", lexeme, line, column))
                return
            if char in "\r\n":
                break
            if char == "\\":
                self._advance()
                if not self._at_end() and self._current() not in "\r\n":
                    self._advance()
            else:
                self._advance()

        self.items.append(
            LexicalError("Cadena sin cerrar", line, column)
        )

    def _skip_line_comment(self) -> None:
        self._advance()
        self._advance()
        while not self._at_end() and self._current() not in "\r\n":
            self._advance()

    def _skip_block_comment(self) -> None:
        line, column = self.line, self.column
        self._advance()
        self._advance()

        while not self._at_end():
            if self._starts_with("*/"):
                self._advance()
                self._advance()
                return
            self._advance()

        self.items.append(
            LexicalError("Comentario multilínea sin cerrar", line, column)
        )

    def _read_operator_or_delimiter(self) -> bool:
        line, column = self.line, self.column

        for lexeme, token_type in self.TWO_CHARACTER_OPERATORS.items():
            if self._starts_with(lexeme):
                self._advance()
                self._advance()
                self.items.append(Token(token_type, lexeme, line, column))
                return True

        char = self._current()
        token_type = self.ONE_CHARACTER_TOKENS.get(char)
        if token_type is None:
            return False

        self._advance()
        self.items.append(Token(token_type, char, line, column))
        return True
