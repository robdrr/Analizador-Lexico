# Importamos la librería 're' para trabajar con expresiones regulares
import re  

# Importamos 'defaultdict' de la librería 'collections'
# Nos permite crear un diccionario que devuelve un valor por defecto si una clave no existe
from collections import defaultdict        

# Definimos la clase 'Lexer', que será nuestro analizador léxico
class Lexer:
    def __init__(self):
        """
        Constructor de la clase Lexer.
        Define los tokens a reconocer y crea estructuras para almacenar los resultados.
        """

        # Lista de tokens con sus respectivas expresiones regulares
        # Cada token tiene un número asociado para identificar su tipo
        self.tokens = [
            (0, r'\b(int|float|char|void|string)\b'),  # Tipos de datos
            (10, r'\bif\b'),  # Palabra clave "if"
            (11, r'\bwhile\b'),  # Palabra clave "while"
            (12, r'\breturn\b'),  # Palabra clave "return"
            (13, r'\belse\b'),  # Palabra clave "else"
            (14, r'\bfor\b'),  # Palabra clave "for"
            (2, r'\b\d+(\.\d+)?\b|\bpi\b|#'),  # Constantes numéricas y la constante 'pi'
            (1, r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),  # Identificadores (variables, nombres de funciones)
            (3, r';'),  # Punto y coma (;)
            (4, r','),  # Coma (,)
            (5, r'\('),  # Paréntesis izquierdo '('
            (6, r'\)'),  # Paréntesis derecho ')'
            (7, r'\{'),  # Llave izquierda '{'
            (8, r'\}'),  # Llave derecha '}'
            (9, r'='),  # Operador de asignación '='
            (15, r'[\+\-]'),  # Operadores aritméticos de suma/resta ('+', '-')
            (16, r'[\*/<>]{1,2}'),  # Operadores multiplicativos y relacionales ('*', '/', '<', '>')
            (17, r'&&|\|\|'),  # Operadores lógicos ('&&', '||')
            (18, r'[<>]=?|==|!='),  # Operadores relacionales ('<', '>', '>=', '<=', '==', '!=')
            (19, r'\$'),  # Símbolo especial ('$')
        ]

        # Diccionario para contar cuántas veces aparece cada tipo de token
        self.token_counts = defaultdict(int)

        # Lista para almacenar los errores léxicos encontrados
        self.errors = []

        # Lista donde almacenaremos los tokens reconocidos junto con su tipo
        self.matches = []

    def analyze(self, input_string):
        """
        Analiza una cadena de entrada y extrae los tokens.
        
        """
        pos = 0  

        # Recorremos toda la cadena mientras queden caracteres por analizar
        while pos < len(input_string):
            # Ignoramos los espacios en blanco y tabulaciones 
            if input_string[pos].isspace():
                pos += 1  
                continue  

            match_found = False  # Variable para saber si encontramos un token válido en esta posición

            # Recorremos la lista de tokens definidos para intentar hacer una coincidencia
            for token_type, patron in self.tokens:
                regex = re.compile(patron)  # Compilamos la expresión regular
                match = regex.match(input_string, pos)  # Intentamos encontrar un match en la posición actual

                # Si encontramos un token válido
                if match:
                    lexeme = match.group(0)  # Extraemos el texto del token
                    self.matches.append((lexeme, token_type))  # Guardamos el token en la lista de coincidencias
                    self.token_counts[token_type] += 1  # Incrementamos el contador de este tipo de token
                    pos += len(lexeme)  # Movemos la posición hacia adelante según el tamaño del token encontrado
                    match_found = True  # Marcamos que encontramos un token
                    break  # Salimos del bucle porque ya encontramos un token en esta posición

            # Si no encontramos ningún token válido en la posición actual, lo consideramos un error léxico
            if not match_found:
                self.errors.append(f"Error léxico en posición {pos}: '{input_string[pos]}'")
                pos += 1  # Avanzamos al siguiente carácter para seguir analizando

    def display_results(self):
        """
        Muestra los resultados del análisis léxico: tokens encontrados, conteo por categoría y errores.
        """
        print("\nTokens encontrados:")
        # Mostramos todos los tokens encontrados junto con su tipo
        for lexeme, token_type in self.matches:
            print(f"{lexeme} -> {token_type}")

        print("\nCantidad de tokens por categoría:")
        # Mostramos cuántos tokens de cada tipo fueron encontrados
        for token_type, count in sorted(self.token_counts.items()):
            print(f"Categoría {token_type}: {count}")

        # Si hubo errores léxicos, los mostramos
        if self.errors:
            print("\nErrores encontrados:")
            for error in self.errors:
                print(error)

# Bloque principal: solo se ejecuta si el script es ejecutado directamente
if __name__ == "__main__":
    input_string = input("Ingrese el código a analizar: ")  # Pedimos al usuario que ingrese código fuente
    lexer = Lexer()  # Creamos una instancia del analizador léxico
    lexer.analyze(input_string)  # Analizamos la entrada del usuario
    lexer.display_results()  # Mostramos los resultados del análisis
