from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from utilities.InicioSesionLog import SingUp
from utilities.handy_wrappers import HandyWrappers
from sshtunnel import SSHTunnelForwarder
import pymongo
import time
import codecs
import json
from datetime import datetime
import sys
connection=None
server=None

class Logs():
    def  __init__(self):
        pass
    def checkInfo(self, modulo='', filtro='', dato1='',dato2=''):
        MONGO_DB= "logDB"
        fieldnames = ["modulo", "filtro", "parametros", "resultados"]
        su = SingUp()
        try:
            driver = su.startLoginLog(use=True)
        except:
            results = "Proceso finalizado. No se retorno el driver de inicio sesión"
            print(results)
            data = [{"modulo": modulo, "resultados": results}]
            su.createCVS(fieldnames=fieldnames, data=data, name="Fail" + modulo)
            return
        if driver == None:
            results = "Proceso finalizado. No se retorno el driver de inicio sesión"
            print(results)
            data = [{"modulo": modulo, "resultados": results}]
            su.createCVS(fieldnames=fieldnames, data=data, name="Fail" + modulo)
            return
        hw = HandyWrappers(driver)
        if modulo == "solicitudes":
            driver.find_element(By.XPATH, "//*[@href='#/log-solicitudes']").click()
            columns = ['Cliente', 'Usuario', 'Acción', 'Documento', 'Fecha']
            details = ['Responsable:', 'Servicio Consumido:', 'Id del documento:']
            coll ="solicituds"
        elif modulo == "usuarios":
            driver.find_element(By.XPATH, "//*[@href='#/reporte-acciones']").click()
            columns = ['Sistema', 'Responsable', 'Acción', 'Usuario afectado', 'Fecha']
            details = ['Responsable:', 'Servicio Consumido:', 'Id del documento:']
            coll= "usuarioslogs"
        elif modulo == "sociedades":
            driver.find_element(By.XPATH, "//*[@href='#/log-sociedades']").click()
            columns = ['Sistema', 'Responsable', 'Acción', 'Sociedad', 'Fecha']
            details = ['Responsable:', 'Servicio Consumido:', 'Id del documento:']
            coll= "sociedadschemas"
        else:
            print("modulo invalido")
            return

        # button = driver.find_element(By.XPATH, "//button[@class='btn btn-link collapsed']")
        # driver.execute_script("arguments[0].click();", button)
        for colum in columns:
            value = hw.isElementPresent(byType=By.XPATH, locator="//table//thead//*[text()='" + colum + "']")
            if not value:
                print("falta dato " + colum + " en la tabla")

        print("datos de la tabla analizados")
        print("Analizando los detalles")
        btnDetails=driver.find_element(By.XPATH,"//table//tr//td[6]//span[1]")
        driver.execute_script("arguments[0].click();", btnDetails)
        for d in details:
            value = hw.isElementPresent(locator="//table//tr//td//p[text()='"+d+"']",byType=By.XPATH)
            if value:
                text =driver.find_element(By.XPATH,"//table//tr//td//p[text()='"+d+"']//code").text
                if text == "":
                    print("no hay informacion en:" + d)
        driver.execute_script("arguments[0].click();", btnDetails)



        #------------------------------------- FILTROS POR BUSQUEDA ----------------------------------------------------
        if filtro== 'busqueda':
            indice=0
            try:
                 indice = columns.index(dato1)+1
            except:
                results = "campo de busqueda " + dato1 +" no valido"
                print(results)
                name = "TestInfoFail"
                data = [
                    {"modulo": modulo, "filtro": filtro, "parametros": dato1 + " a " + dato2, "resultados": results}]
                su.createCVS(fieldnames=fieldnames, data=data, name=name)
                return

            print("buscando por "+dato1+": "+dato2)
            driver.find_element(By.XPATH,
                                "//input[contains (@type,'text')and contains (@placeholder,'Búsqueda')]").send_keys(dato2)
            driver.find_element(By.XPATH, "//button[text()='Buscar']").click()

            time.sleep(2)
            filas = driver.find_elements(By.XPATH, "//tbody/tr/td["+str(indice)+"]/div")

            if len(filas) == 0:
                print("sin resultados")
            else:
                while True :
                    next = driver.find_element(By.XPATH, "//div[@id='pagination']//a[3]")
                    filas = driver.find_elements(By.XPATH, "//tbody/tr/td[" + str(indice) + "]/div")
                    for campo in filas:
                        texto = campo.text
                        notfind = -1
                        if texto.find(dato2) == notfind :
                            print("se encontro un dato no valido")

                    paginas = driver.find_elements(By.XPATH, "//div[@id='pagination']//span")
                    print("pagina "+paginas[0].text+" de "+paginas[1].text)
                    if paginas[0].text == paginas[1].text:
                        break
                    else:
                        driver.execute_script("arguments[0].click();",next)
                        time.sleep(1)


                print("todos los datos coinciden con la busqueda")
            print("comparando contra la base de datos")
            dataInFront = self.infoFront(driver)
            self.conectionDB()
            db = self.connection[MONGO_DB]
            collection = db[coll]
            campo = self.buscaCampoDB(dato1)
            print("la busqueda se reliza por :"+campo+" y se busca "+dato2)
            sizeofData = collection.find({campo: {"$regex":dato2}}).count()
            if dataInFront == sizeofData:
                results = ("Al filtrar son " + str(dataInFront) + " datos en el modulo que tambien estan en la BD")
                print(results)
                su.takescreenshot(driver=driver, namescren="TestInfoSuccessful", directory="TestModules/")
                name = "TestInfoSuccessful"
            else:
                results = ("Los " + str(sizeofData) + " datos de ls BD no coinciden con los " + str(
                    dataInFront) + " datos en la pagina, al realizar el filtrado")
                print(results)
                su.takescreenshot(driver=driver, namescren="TestInfoFail", directory="TestModules/")
                name = "TestInfoFail"
            data = [{"modulo": modulo,"filtro":filtro, "parametros": dato1+":"+dato2, "resultados": results}]
            su.createCVS(fieldnames=fieldnames, data=data, name=name)
            time.sleep(1)
            self.closeSshandConection()
            driver.quit()
            time.sleep(2)

        #------------------------------------- FILTROS POR FECHA ----------------------------------------------------
        elif filtro == 'fecha':
            dia = dato1[:dato1.index("/")]
            sliceD = dato1[dato1.index("/") + 1:]
            mes = sliceD[:sliceD.index("/")]
            año = sliceD[sliceD.index("/") + 1:]

            dia2 = dato2[:dato2.index("/")]
            sliceD = dato2[dato2.index("/") + 1:]
            mes2 = sliceD[:sliceD.index("/")]
            año2 = sliceD[sliceD.index("/") + 1:]

            if int(dia) > 0 and int(dia) < 32:
                if int(mes) > 0 and int(mes) < 13:
                    if int(año) > 2008 and int(año) < 2030:
                        pass
                    else:
                        print("fecha invalida de inicio, año fuera de rango")
                else:
                    print("fecha de inicio invalida, mes incorrecto")
            else:
                print("fecha de inicio invalida, dia incorrecto")
            if int(dia2) > 0 and int(dia2) < 32:
                if int(mes2) > 0 and int(mes2) < 13:
                    if int(año2) > 2008 and int(año2) < 2030:
                        pass
                    else:
                        print("fecha final invalida, año fuera de rango")
                else:
                    print("fecha final invalida, mes incorrecto")
            else:
                print("fecha final invalida, dia incorrecto")
            #INSERTA LA PRIMER FECHA
            date = driver.find_element(By.XPATH, "//button[@class='btn btn-outline-secondary btn-sm'][1]")
            driver.execute_script("arguments[0].click();", date)
            time.sleep(1)
            element = driver.find_elements(By.XPATH,"//select[@class='custom-select']")

            sel = Select(element[1])
            sel.select_by_value(año)

            sel2 = Select(element[0])
            mes = str(int(mes))
            sel2.select_by_value(mes)
            try:
                dias = driver.find_elements(By.XPATH,"//div[@class='btn-light']")
            except:
                print("al perecer el mes "+mes+" solo tiene 30 o menos dias")
                return
            dias[int(dia)-1].click()

            #INSERTA LA SEGUNDA FECHA
            date = driver.find_element(By.XPATH, "//button[@class='btn btn-outline-secondary btn-sm'][2]")
            driver.execute_script("arguments[0].click();", date)
            time.sleep(1)
            element = driver.find_elements(By.XPATH,"//select[@class='custom-select']")

            sel = Select(element[1])
            sel.select_by_value(año2)

            sel2 = Select(element[0])
            mes2 = str(int(mes2))
            sel2.select_by_value(mes2)
            try:
                dias = driver.find_elements(By.XPATH,"//div[@class='btn-light']")
            except:
                print("al perecer el mes "+mes2+" solo tiene 30 o menos dias")
                return
            dias[int(dia2)-1].click()

            time.sleep(2)
            driver.find_element(By.XPATH, "//button[text()='Buscar']").click()
            time.sleep(2)
            #-------------------
            dataInFront = self.infoFront(driver)
            self.conectionDB()
            db = self.connection[MONGO_DB]
            collection = db[coll]
            date1=[int(dia), int(mes), int(año)]
            date2 = [int(dia2), int(mes2), int(año2)]
            sizeofData = self.DateinDataB(collection=collection, date1Int=date1, date2Int=date2)


            if dataInFront == sizeofData:
                results = ("Al filtrar son " + str(dataInFront) + " datos en el modulo que tambien estan en la BD")
                print(results)
                su.takescreenshot(driver=driver, namescren="TestInfoSuccessful", directory="TestModules/")
                name = "TestInfoSuccessful"
            else:
                results = ("Los " + str(sizeofData) + " datos de ls BD no coinciden con los " + str(
                    dataInFront) + " datos en la pagina al realizar el filtrado")
                print(results)
                su.takescreenshot(driver=driver, namescren="TestInfoFail", directory="TestModules/")
                name = "TestInfoFail"
            data = [{"modulo": modulo, "filtro": filtro, "parametros": dato1+" a "+dato2, "resultados": results}]
            su.createCVS(fieldnames=fieldnames, data=data, name=name)
            time.sleep(1)
            self.closeSshandConection()
            driver.quit()
            time.sleep(2)

        time.sleep(1)
        driver.quit()
    def infoFront(self,driver):
        paginas = driver.find_element(By.XPATH, "//div[@id='pagination']//span[2]").text
        numPag = int(paginas)
        print("numero total de paginas: "+str(numPag))
        ultima = driver.find_element(By.XPATH, "//a//img[@src='./assets/img/last.png']")
        driver.execute_script("arguments[0].click();", ultima)
        time.sleep(1)
        filas = driver.find_elements(By.XPATH, "//table//tbody//tr")
        sizeF = len(filas)
        dataInFront = (10 * (numPag - 1)) + sizeF
        return dataInFront

    def conectionDB(self):
        MONGO_HOST = "ec2-34-210-56-229.us-west-2.compute.amazonaws.com"
        MONGO_USER = "ubuntu"
        MONGO_PASS = "~/Desktop/testing/Testing/GRP-Key-Testing.pem"

        # define ssh tunnel
        self.server = SSHTunnelForwarder(
            MONGO_HOST,
            ssh_username=MONGO_USER,
            ssh_pkey=MONGO_PASS,
            remote_bind_address=('127.0.0.1', 27017)
        )
        # start ssh tunnel
        self.server.start()
        self.connection = pymongo.MongoClient('127.0.0.1', self.server.local_bind_port)
    def DateinDataB(self, collection, date1Int=[], date2Int=[]):
        size = collection.find({})
        datos = []
        count = 0
        for cursor in size:
            datos.append(cursor['fecha'][:10])
            count += 1

        año = date1Int[2]
        mes = date1Int[1]
        dia = date1Int[0]
        año1 = date2Int[2]
        mes1 = date2Int[1]
        dia1 = date2Int[0]
        datosC = 0
        for dato1 in datos:
            añob = int(dato1[:dato1.index("-")])
            dato1 = dato1[dato1.index("-") + 1:]
            mesb = int(dato1[:dato1.index("-")])
            diab = int(dato1[dato1.index("-") + 1:])
            fechabd = datetime(añob, mesb, diab)
            fechaInicio = datetime(año, mes, dia)
            fechaFin = datetime(año1, mes1, dia1)
            if str(fechabd) >= str(fechaInicio) and str(fechabd) <= str(fechaFin):
                datosC += 1
        return datosC
    def buscaCampoDB(self, campo):
        if campo == "Acción":
            campo = "accion"
        elif campo =="Usuario":
            campo = "usuario"
        elif campo =="Documento":
            campo = "solicitud"
        elif campo =="Responsable":
            campo = "responsable"
        elif campo =="Usuario afectado":
            campo = "afectado"
        elif campo =="Sociedad":
            campo = "sociedad"
        return campo
    def closeSshandConection(self):
        self.connection.close()
        self.server.stop()
    def startTest (self,use = False):
        dato1=''
        dato2=''
        try:
            file = codecs.open("/utilities/data2.txt", 'r', 'utf-8')
            content = file.read()

        except:
            file = codecs.open("../utilities/data2.txt", 'r', 'utf-8')
            content = file.read()
        else:
            print("Archivo data2.txt no enconrado, verifique:\n"
                  "-Que la paqueteria utilities este dentro de su proyecto.\n"
                  "-Y que esta no se encuentr dentro de otra carpeta o paqueteria.\n"
                  "-A su vez que dentro de ella se encuentre el archivo.")
        try:
            index = content.find("#-comments-#")
            content = content[:index]
            print(content)
            objetos = json.loads(content)
            modulo = objetos['modulo'].lower()
            filtro = objetos['filtro']
            filtro= filtro.lower()
            if filtro == "busqueda":
                dato1= objetos['buscarPor'].capitalize()
                dato2= objetos['busca']
            elif filtro == "fecha":
                dato1 = objetos['fechaInicio']
                dato2 = objetos['fechaFinal']
            else:
                print("filtro invalido")

            l = Logs()
            l.checkInfo(modulo= modulo, filtro=filtro, dato1=dato1, dato2=dato2)
        except:
            print("Error al ejecutar busqueda y lectura de datos",sys.exc_info())