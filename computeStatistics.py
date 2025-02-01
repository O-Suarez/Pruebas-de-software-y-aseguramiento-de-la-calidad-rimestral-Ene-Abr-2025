""" 1. Compute statistics

Req1. The program shall be invoked from a
command line. The program shall receive a
file as parameter. The file will contain a list
of items (presumable numbers).

Req 2. The program shall compute all
descriptive statistics from a file containing
numbers. The results shall be print on a
screen and on a file named
StatisticsResults.txt. All computation MUST
be calculated using the basic algorithms,
not functions or libraries.
The descriptive statistics are mean, median,
mode, standard deviation, and variance.

Req 3. The program shall include the
mechanism to handle invalid data in the file.
Errors should be displayed in the console
and the execution must continue.

Req 4. The name of the program shall be
computeStatistics.py

Req 5. The minimum format to invoke the
program shall be as follows:
python computeStatistics.py
fileWithData.txt

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
from math import sqrt


def calcular_estadisticas(nums):
    """
    Calcula estadísticas: promedio, mediana, moda,
    desviación estándar y varianza.

    """
    # Promedio
    mean = sum(nums) / len(nums)
    # Mediana
    sorted_nums = sorted(nums)
    mid = len(sorted_nums) // 2
    median = (sorted_nums[mid] + sorted_nums[~mid]) / 2.0
    # Moda
    mode = max(set(nums), key=nums.count)
    # Desviación estándar
    std_deviation = sqrt(
        sum((x - mean) ** 2 for x in nums) / len(nums)
    )
    # Varianza
    variance = sum((x - mean) ** 2 for x in nums) / len(nums)

    return mean, median, mode, std_deviation, variance


def guardar_estadisticas(estadisticas, elapsed_time):
    """
    Guarda las estadísticas en un archivo e imprime los resultados.
    """
    mean, median, mode, std_deviation, variance = estadisticas
    output = (
        f"Promedio: {mean}\n"
        f"Mediana: {median}\n"
        f"Moda: {mode}\n"
        f"Desviación estándar: {std_deviation}\n"
        f"Varianza: {variance}\n"
        f"Tiempo de procesamiento: {elapsed_time:.3f} ms\n"
    )

    try:
        with open('StatisticsResults.txt', 'w', encoding='utf-8') as file:
            file.write(output)
        print(output)
        print("Estadísticas guardadas en 'StatisticsResults.txt' con éxito.")
        sys.stdout.flush()
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error al guardar los resultados: {str(e)}")


def procesar_archivo(filename):
    """
    Procesa un archivo de texto, extrae números y calcula estadísticas.
    La función asume que los números estan separados por lineas
    """
    start_time = time.time()  # Inicio del tiempo de ejecución

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            nums = []
            for index, line in enumerate(file, start=1):
                # Eliminamos todos los caracteres no numéricos
                num_line = re.sub(r'\D', '', line)
                if len(num_line) != 0:
                    nums.append(int(num_line))
                else:
                    print(f"Error en la línea {index}:",
                          " Ningún carácter numérico detectado")
                    print(line.strip())

            if nums:
                estadisticas = calcular_estadisticas(nums)
                # Tiempo de ejecución en milisegundos
                elapsed_time = (time.time() - start_time) * 1000
                guardar_estadisticas(estadisticas, elapsed_time)
            else:
                print("Ningún número válido encontrado")
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error al abrir el archivo: {str(e)}")


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
        print("Uso: python computeStatistics.py archivoDeTexto.txt")


if __name__ == "__main__":
    main()
