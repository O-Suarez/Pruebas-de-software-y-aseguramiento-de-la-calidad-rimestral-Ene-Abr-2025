""" 2. Converter

Req1. The program shall be invoked from a
command line. The program shall receive a
file as parameter. The file will contain a list
of items (presumable numbers).

Req 2. The program shall convert the
numbers to binary and hexadecimal base.
The results shall be print on a screen and on
a file named ConvertionResults.txt.
All computation MUST be calculated using
the basic algorithms, not functions or
libraries.

Req 3. The program shall include the
mechanism to handle invalid data in the file.
Errors should be displayed in the console
and the execution must continue.

Req 4. The name of the program shall be
convertNumbers.py
Req 5. The minimum format to invoke the
program shall be as follows:
python convertNumbers.py fileWithData.txt

Req 6. The program shall manage files
having from hundreds of items to thousands
of items.

Req 7. The program should include at the
end of the execution the time elapsed for
the execution and calculus of the data. This
number shall be included in the results file
and on the screen.

Req 8. Be compliant with PEP8.

"""

import os
import re
import sys
import time


def dec_to_binary(number):
    """
    Convierte un número decimal a su representación binaria.
    """
    if number == 0:
        return "0"

    bits = []
    n = number
    while n > 0:
        remainder = n % 2
        n //= 2
        bits.insert(0, str(remainder))  # Insert at the beginning

    return "".join(bits)


def dec_to_hexadecimal(number):
    """
    Convierte un número decimal a su representación hexadecimal.
    """
    if number == 0:
        return "0"

    hex_digits = "0123456789ABCDEF"
    result = []
    n = number
    while n > 0:
        remainder = n % 16
        n //= 16
        result.insert(0, hex_digits[remainder])  # Insert at the beginning

    return "".join(result)


def guardar_numeros(binary_nums, hexadecimal_nums, elapsed_time):
    """
    Guarda los resultados (binario y hexadecimal) en un archivo e imprime
    los mismos en la pantalla.
    """
    # Construimos línea por línea en el formato:
    # {binario}, {hexadecimal}
    lines = [f"{b}, {h}" for b, h in zip(binary_nums, hexadecimal_nums)]
    for line in lines:
        print(line)
    # Incluimos el tiempo de procesamiento (en ms) al final.
    lines.append(f"Tiempo de procesamiento: {elapsed_time:.3f} ms")

    try:
        with open('ConvertionResults.txt', 'w', encoding='utf-8') as file:
            file.write("\n".join(lines))
        print("Resultados guardados en 'ConvertionResults.txt' con éxito.")
    except (FileNotFoundError, PermissionError, OSError) as err:
        print(f"Error al guardar los resultados: {str(err)}")


def procesar_archivo(filename):
    """
    Procesa un archivo de texto, extrae números y realiza conversiones
    a binario y hexadecimal.
    La función asume que los números estan separados por lineas
    """
    start_time = time.time()  # Inicio del tiempo de ejecución

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            binary_nums = []
            hex_nums = []

            for index, line in enumerate(file, start=1):
                # Eliminamos todos los caracteres no numericos
                # Cualquier numero con valores decimales
                # sera convertido a un entero positivo
                match = re.search(r'[+\-]?(\d+)', line)
                if match:
                    number = int(match.group(1))
                    binary_nums.append(dec_to_binary(number))
                    hex_nums.append(dec_to_hexadecimal(number))
                else:
                    print(f"Error en la línea {index}:",
                          f"Valor inválido -> {line.strip()}")

            if binary_nums:
                # Tiempo de ejecución en milisegundos
                elapsed_time = (time.time() - start_time) * 1000
                guardar_numeros(binary_nums, hex_nums, elapsed_time)
            else:
                print("El archivo no contiene números válidos.")

    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error al abrir el archivo '{filename}': {str(e)}")


def main():
    """
    Funcion principal
    """
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print(f"El archivo no existe: {filename}")
            sys.exit(1)
        # Procesar el archivo si existe
        procesar_archivo(filename)
    else:
        print("No se incluyó ningún nombre de archivo en los argumentos.")
        print("Uso: python convertNumbers.py archivoDeTexto.txt")


if __name__ == "__main__":
    main()
