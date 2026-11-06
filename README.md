# Proyecto final:   

## Alcance implementado

- Implementación propia en Python y biblioteca estándar, sin PLY, ANTLR ni
  dependencias de terceros.
- Palabras reservadas: `if`, `else`, `while`, `return`, `int`, `float`, `void`,
  `char`, `double`, `for`, `do`, `break` y `continue`.
- Identificadores ASCII: comienzan con una letra o `_` y continúan con letras,
  dígitos o `_`.
- Literales enteros, flotantes con dígitos a ambos lados del punto y cadenas
  entre comillas dobles. Las cadenas aceptan escapes con barra inversa; no
  pueden cruzar una línea.
- Operadores `+`, `-`, `*`, `/`, `=`, `==`, `!=`, `<`, `>`, `<=` y `>=`.
- Delimitadores `(`, `)`, `{`, `}`, `,` y `;`.
- Espacios y comentarios `//` y `/* ... */` ignorados, conservando el conteo de
  líneas y columnas. Una tabulación cuenta como una columna.
- Los errores léxicos se muestran en la salida y el scanner continúa. Los
  números como `12abc`, las cadenas sin cerrar, los comentarios multilínea sin
  cerrar y los caracteres no reconocidos se reportan como errores.
- El proceso termina con código `0` si no hubo errores léxicos, `1` si encontró
  errores y `2` si faltó la ruta o no se pudo leer el archivo.

## Estructura prevista

```text
.
├── main.py
├── lexer.py
├── README.md
└── tests/
    ├── caso_valido.txt
    └── caso_error.txt
```

## Cómo probarlo

Python es un lenguaje interpretado; no hace falta compilar estos archivos a un
ejecutable. Se necesita Python 3 instalado. Abre una terminal en la carpeta
del proyecto y ejecuta:

Desde la carpeta del proyecto:

```text
python main.py tests/caso_valido.txt
python main.py tests/caso_error.txt
```

En Windows, si `python` no está disponible, utiliza el lanzador `py`:

```text
py main.py tests/caso_valido.txt
py main.py tests/caso_error.txt
```

El primer caso debe imprimir tokens sin errores y terminar con código `0`. El
segundo incluye intencionalmente tres errores léxicos; deben aparecer los
mensajes y el análisis debe continuar hasta el final. Que ese comando termine
con código `1` es lo esperado.

Para analizar otro programa, guárdalo en un archivo de texto (por ejemplo,
`mi_programa.txt`) y pasa su ruta como argumento:

```text
python main.py mi_programa.txt
```

## Flujo del análisis

1. La terminal inicia `main.py` y le entrega la ruta del archivo.
2. `main.py` lee el archivo como UTF-8 y crea el analizador definido en
   `lexer.py`.
3. El scanner recorre el texto de izquierda a derecha, actualizando línea y
   columna; reconoce tokens y omite espacios y comentarios.
4. Si encuentra un carácter o lexema inválido, informa el error en su posición
   e intenta seguir con el resto del archivo.
5. Se imprimen tokens y errores en el orden en que se encontraron. El código de
   salida permite distinguir un análisis limpio de uno con errores.

## Estructura del proyecto

```text
.
├── main.py
├── lexer.py
├── README.md
└── tests/
    ├── caso_valido.txt
    └── caso_error.txt
```
