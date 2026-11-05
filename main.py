"""Command-line entry point for the lexical analyzer."""

import sys

from lexer import LexicalError, Lexer, Token


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python main.py <ruta_archivo>", file=sys.stderr)
        return 2

    file_path = sys.argv[1]
    try:
        with open(file_path, "r", encoding="utf-8") as source_file:
            source = source_file.read()
    except (OSError, UnicodeError) as error:
        print("Error al leer {!r}: {}".format(file_path, error), file=sys.stderr)
        return 2

    items = Lexer(source).tokenize()
    error_count = 0
    for item in items:
        if isinstance(item, Token):
            print(
                "[TOKEN] Tipo: {:<14} | Lexema: {!r} | "
                "Posición: [Línea {}, Col {}]".format(
                    item.type, item.lexeme, item.line, item.column
                )
            )
        elif isinstance(item, LexicalError):
            error_count += 1
            print(
                "[ERROR LÉXICO] {} en Posición: [Línea {}, Col {}]".format(
                    item.message, item.line, item.column
                )
            )

    return 1 if error_count else 0


if __name__ == "__main__":
    sys.exit(main())
