""" 3. Count Words

Req1. The program shall be invoked from a
command line. The program shall receive a
file as parameter. The file will contain a
words (presumable between spaces).

Req 2. The program shall identify all
distinct words and the frequency of them
(how many times the word “X” appears in
the file). The results shall be print on a
screen and on a file named
WordCountResults.txt.

All computation MUST be calculated using
the basic algorithms, not functions or
libraries.

Req 3. The program shall include the
mechanism to handle invalid data in the
file. Errors should be displayed in the
console and the execution must continue.

Req 4. The name of the program shall be
wordCount.py

Req 5. The minimum format to invoke the
program shall be as follows:

python wordCount.py fileWithData.txt
Req 6. The program shall manage files
having from hundreds of items to
thousands of items.

Req 7. The program should include at the
end of the execution the time elapsed for
the execution and calculus of the data.
This number shall be included in the
results file and on the screen.

Req 8. Be compliant with PEP8.

"""

import os
import re
import sys
import time


def procesar_palabras(words):
    """
    Construye una lista de palabras únicas (unique_words).
    Construye una lista paralela con las frecuencias (frequency).
    """

    unique_words = []
    frequency = []

    # Recorremos la lista "words" para contar ocurrencias manualmente
    for w in words:
        if w in unique_words:
            index_w = unique_words.index(w)
            frequency[index_w] += 1
        else:
            unique_words.append(w)
            frequency.append(1)

    return unique_words, frequency


def guardar_palabras(unique_words, frequency, elapsed_time):
    """
    Recibe las listas de palabras únicas y sus frecuencias,
    junto con el tiempo de ejecución.
    Guarda los resultados en "WordCountResults.txt".
    """

    lines = []
    # Construimos línea por línea en el formato: "palabra: frecuencia"
    for word, freq in zip(unique_words, frequency):
        line = f"{word}: {freq}"
        print(line)
        lines.append(line)

    # Incluimos el tiempo de procesamiento (en milisegundos) al final.
    time_line = f"Tiempo de procesamiento: {elapsed_time:.3f} ms"
    print(time_line)
    lines.append(time_line)

    # Guardamos los resultados en un archivo
    try:
        with open('WordCountResults.txt', 'w', encoding='utf-8') as file:
            file.write("\n".join(lines))
        print("Resultados guardados en 'WordCountResults.txt' con éxito.")
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error al guardar los resultados: {str(e)}")


def procesar_archivo(filename):
    """
    Lee un archivo de texto línea a línea y extrae las palabras. Cada
    palabra se valida y se almacena en una lista "words". Después,
    se procesan las palabras para contar la frecuencia de cada una.
    """
    start_time = time.time()  # Inicio del tiempo de ejecución

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = []
            for index, line in enumerate(file, start=1):
                # Dividimos la línea en trozos separados por espacio.
                raw_tokens = line.split()

                for token in raw_tokens:
                    # Marcamos tokens que
                    # tengan caracteres no alfabéticos como inválidos.
                    if re.match(r'^[A-Za-z]+$', token):
                        words.append(token)
                    else:
                        print(f"Error en la línea {index}:",
                              f"dato inválido -> {token}")

            if words:
                unique_words, frequency = procesar_palabras(words)
                elapsed_time = (time.time() - start_time) * 1000
                guardar_palabras(unique_words, frequency, elapsed_time)
            else:
                print("Ninguna palabra válida encontrada.")
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error al abrir el archivo '{filename}': {str(e)}")


def main():
    """
    Función principal
    """
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print(f"El archivo no existe: {filename}")
            sys.exit(1)
        procesar_archivo(filename)
    else:
        print("No se incluyó ningún nombre de archivo en los argumentos.")
        print("Uso: python wordCount.py archivoDeTexto.txt")


if __name__ == "__main__":
    main()
