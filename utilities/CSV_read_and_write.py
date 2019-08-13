# ------------------------ DOCUMENTACIÓN --------------------------------
# <copyright file="CSV_read_and_write" company="GLOUU TECHNOLOGIES">
#     Copyright (c) Glouu Technologies. All rights reserved.
# </copyright>
# <author>Julio C. Saldivar</author>
# <rastreo></rastreo>
# -----------------------------------------------------------------------
import csv
import time
import codecs
# <CSVclass>
# Clase Principal, contiene metodos que nos ayuda a escribir y leer archivos .csv
# </CSVclass>
# <param></param>
# <returns></returns>
class CSVclass():
    def __init__(self):
        pass

    # <writeCSV>
    # metodo de escritura de archivo .csv
    # </writeCSV>
    # <param namescren ='', directory='', name>
    # son necesarios los nombres de los datos y la informacion a guardar
    # , fieldnames debe ser un arreglo de cadena y data debe ser un arreglo de diccionarios,
    # es muy necesario que los fieldnames y los inideces del diccionario sean los mismos.
    # por ultimo el nombre que tendrá el archivo.
    # </param>
    # <returns></returns>
    def writeCSV(self, fieldnames =None, data=None, name='CSVfile'):
        if fieldnames and data:
            namefile = str(round(time.time() * 1000)) +name+'.csv'
            with codecs.open(namefile, 'w', "utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
                print("CSV guardado como: "+namefile)
            self.readCSV(namefile=namefile)
        else:
            print("Fallo escritura  CSV debes enviar los parametros 'fieldnames' y 'data'\n"
                  "Field names: los nombres de los campos en un arreglo \n"
                  "data: la informacion para guardar en un arreglo de dicccionarios.")
            return

    # <readCSV>
    # metodo de escritura de archivo .csv
    # </readCSV>
    # <param namefile=''>
    # El nombre del archivo es lo unico necesario, este deberá tener la ruta completa o parcial en caso
    # de no encontrarse en la carpeta donde del proyecto.
    # </param>
    # <returns></returns>
    def readCSV(self, namefile=''):
        if not namefile == '':
            with codecs.open(namefile, encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                print("")
                print("--------------------------------Inicia lectura de CSV------------------------------------")
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Las columnas son: {", ".join(row)}')
                        line_count += 1
                    else:
                        for r in row:
                            print(r, end=", ")
                        print()
                        line_count += 1
                if not line_count==0:
                    print(f'--------------------------------{line_count} lineas procesadas.---------------------------------------')
                    print("--------------------------------Termina lectura de CSV------------------------------------")
                    print("")
                else:
                    print("El archivo CSV esta vacio")
                    return
        else:
            print("Envia un nombre del archivo")
