""" 1. Compute sales

Req1. The program shall be invoked from a
command line. The program shall receive two
files as parameters. The first file will contain
information in a JSON format about a catalogue
of prices of products. The second file will
contain a record for all sales in a company.

Req 2. The program shall compute the total cost
for all sales included in the second JSON archive.
The results shall be print on a screen and on a
file named SalesResults.txt. The total cost
should include all items in the sale considering
the cost for every item in the first file.
The output must be human readable, so make it
easy to read for the user.

Req 3. The program shall include the mechanism
to handle invalid data in the file. Errors should
be displayed in the console and the execution
must continue.

Req 4. The name of the program shall be
computeSales.py

Req 5. The minimum format to invoke the
program shall be as follows:
python computeSales.py priceCatalogue.json
salesRecord.json

Req 6. The program shall manage files having
from hundreds of items to thousands of items.

Req 7. The program should include at the end of
the execution the time elapsed for the
execution and calculus of the data. This number
shall be included in the results file and on the
screen.
Req 8. Be compliant with PEP8.

"""

import os
import sys
import json
import time


def procesar_archivos(catalogue_file, sales_record_file):
    """
    Abre los archivos json y extrae la información deseada
    """
    with open(catalogue_file, 'r', encoding='utf-8') as f:
        catalogue = json.load(f)
    with open(sales_record_file, 'r', encoding='utf-8') as f:
        sales_record = json.load(f)

    sales = {}
    # Extrae los nombres y precios de cada producto
    for item in catalogue:
        title = item.get('title')
        price = item.get('price')
        sales[title] = [price, 0]

    # Extrae la cantidad de veces que se vendio un producto
    for sale in sales_record:
        product_title = sale.get('Product')
        quantity = sale.get('Quantity', 0)
        if product_title in sales:
            # Suma la cantidad de ventas
            sales[product_title][1] += quantity
        else:
            print(f"Producto no detectado en el catalogo: {product_title}")
    return sales


def calcular_total(sales):
    """
    Calcula las ventas totales
    """
    total = 0
    for item in sales.values():
        # La ganancia es igual a
        # el precio del producto por las veces que se vendio
        ganancia = item[0] * item[1]
        total += ganancia
    return total


def main():
    """
    Función principal
    """
    if len(sys.argv) > 2:
        catalogue_file, sales_record_file = sys.argv[1], sys.argv[2]
        if not os.path.isfile(catalogue_file):
            print(f"El archivo no existe: {catalogue_file}")
            sys.exit(1)
        elif not os.path.isfile(sales_record_file):
            print(f"El archivo no existe: {sales_record_file}")
            sys.exit(1)
        # Empieza la ejecucion
        start_time = time.time()
        ventas = procesar_archivos(catalogue_file, sales_record_file)
        total = calcular_total(ventas)
        # Fin de la ejecucion
        end_time = (time.time() - start_time)*1000

        # Resultados
        output = (f"Resultado:{total:.2f}\n"
                  f"Tiempo de procesamiento: {end_time:.6f} milisegundos\n")
        print(output)
        with open("SalesResults.txt", "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print("No se incluyeron todos los nombres de archivo necesarios")
        print("Uso: python computeSales.py catalogo.json ventas.json")


if __name__ == "__main__":
    main()
