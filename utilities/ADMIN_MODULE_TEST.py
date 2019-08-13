from utilities.InicioSesion import SingUp
from utilities.handy_wrappers import HandyWrappers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from sshtunnel import SSHTunnelForwarder
import time
import pymongo
import codecs
import json
import sys
connection = None
server = None

TD_VALIDAR = "//tbody//tr//td[6]//*[text()='{0}']"
class LogAdmin():
    def  __init__(self):
        pass
    def checkInfo(self, modulo='', datos=[]):
        MONGO_DB = "logDB"
        coll='usuarios'
        fieldnames = ["modulo", "resultados"]

        su = SingUp()
        try:
            driver = su.startLogin(use=True)
        except:
            print("process finished, no driver return")
            return
        if driver == None:
            print("process finished, no driver return")
            return None
        print("rediriegiendo a :" + modulo)
        hw = HandyWrappers(driver)
        driver.get(modulo)
        time.sleep(1)

        print("modulo: "+modulo)
        tableExists = hw.isElementPresent(byType="xpath", locator="//table")

        if not tableExists :
            print("no se encontro ninguna estructura de datos valida")
            return None
        encabezadoT = driver.find_element(By.XPATH, "//thead")
        for dato in datos:
            try:
                encabezadoT.find_element(By.XPATH, "//*[text()='" + dato + "']")
            except:
                results = "el dato :" + dato + " no se encontró"
                print(results)
                data = [{"modulo": modulo, "resultados": results}]
                su.createCVS(fieldnames=fieldnames, data=data, name="Fallo" )
                return None
        self.conectionDB()
        db = self.connection[MONGO_DB]
        collection = db[coll]
        sizeofData = collection.find().count()
        paginas = driver.find_element(By.XPATH, "//div[@id='pagination']//span[2]").text
        numPag = int(paginas)
        print(numPag)

        ultima = driver.find_element(By.XPATH, "//a//img[@src='./assets/img/last.png']")
        driver.execute_script("arguments[0].click();", ultima)
        time.sleep(1)
        filas = driver.find_elements(By.XPATH, "//table//tbody//tr")
        sizeF = len(filas)
        dataInFront = (10 * (numPag - 1)) + sizeF


        if dataInFront == sizeofData:
            results = ("Son " + str(dataInFront) + " datos en el modulo que tambien estan en la BD")
            print(results)
            su.takescreenshot(driver=driver, namescren="TestInfoSuccessful", directory="TestModuleAdmin/")
            name = "TestInfoSuccessful"
        else:
            results = ("Los " + str(sizeofData) + " datos de ls BD no coinciden con los " + str(
                dataInFront) + " datos en la pagina")
            print(results)
            su.takescreenshot(driver=driver, namescren="TestInfoFail", directory="TestModuleAdmin/")
            name = "TestInfoFail"
        time.sleep(1)

        data = [{"modulo": modulo, "resultados": results}]
        su.createCVS(fieldnames=fieldnames, data=data, name=name)
        print("EVUALACION!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        first = driver.find_element(By.XPATH, "//img[@src='./assets/img/first.png']")
        driver.execute_script("arguments[0].click();", first)
        time.sleep(1)

        self.closeSshandConection()
        return driver
    def authModal(self, nombre, apellido, correo, area, rol, usuario, contraseña, check):

        try:
            driver = self.checkInfo(
                    modulo="http://ec2-34-210-56-229.us-west-2.compute.amazonaws.com:3001/#/administracion/:modulo",
                    datos=["Nombre", "Apellidos", "Tipo", "Email", "Área", "Usuario", "Estatus"]
            )
            if driver == None:
                print("ocurrio un problema el driver no se retorno, proceso finalizado")
                return
        except:
            print("Error inesperado en el driver:", sys.exc_info()[0])
            try:
                driver.quit()
            except:
                pass
            return


        su = SingUp()
        driver.find_element(By.XPATH,"//button[text()='Agregar usuario']").click()
        time.sleep(1)
        try:
            modal = driver.find_element(By.XPATH,"//div[@class='modal-dialog']//div[@class='modal-content']")
        except:
            print("element modal not found")
            su.takescreenshot(driver, namescren="FailModal", directory="TestModuleAdmin/")
            driver.quit()
            return
        try:
            modal.find_element(By.XPATH,"//div[@class='modal-header']")
            modal.find_element(By.XPATH,"//div[@class='modal-body']")
            modal.find_element(By.XPATH,"//div[@class='modal-footer']")
        except:
            su.takescreenshot(driver, namescren="FailModal", directory="TestModuleAdmin/")
            print("El modal no contiene una estructura valida")
            driver.quit()
            return
        try:
            su.takescreenshot(driver, namescren="Modal", directory="TestModuleAdmin/")
            driver.find_element(By.XPATH, "//input[@name='nombre']").send_keys(nombre)
            driver.find_element(By.XPATH, "//input[@name='apellido']").send_keys(apellido)
            driver.find_element(By.XPATH, "//input[@name='correo']").send_keys(correo)
            driver.find_element(By.XPATH, "//input[@name='area']").send_keys(area)
            sel= Select(driver.find_element(By.XPATH, "//select[@name='rol']"))#select
            sel.select_by_value(rol)
            driver.find_element(By.XPATH, "//input[@name='usuario']").send_keys(usuario)
            driver.find_element(By.XPATH, "//input[@type='password']").send_keys(contraseña)
            if check:
                checking = driver.find_element(By.XPATH, "//input[@name='activo']")
                driver.execute_script("arguments[0].click();", checking)
            su.takescreenshot(driver, namescren="CamposLlenos", directory="TestModuleAdmin/")
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
        except:
            print("Error inesperado al registrar usaurio :", sys.exc_info()[0])
            driver.quit()
            return


        hw = HandyWrappers(driver)
        if hw.elementPresenceCheck(locator="//*[text()='¡El usuario ya existe!']",byType="xpath"):
            res = self.VerificarusrBD(usuario)
            if res > 0:
                print("Usuario existente, denegado con exito")
            else:
                print("El sistema denego un usuario valido")
            su.takescreenshot(driver, namescren="UsuarioExiste", directory="TestModuleAdmin/")
            driver.find_element(By.XPATH, "//button[contains(text(),'Aceptar')]").click()
            self.closeSshandConection()
            if not self.encuentraUsrFront(driver, 6, usuario):
                print("El usuario denegado no se muestra en el front(esto no es correcto)")
            driver.quit()
            return
        su.takescreenshot(driver, namescren="UsuarioAgregado", directory="TestModuleAdmin/")
        driver.find_element(By.XPATH, "//button[contains(text(),'Aceptar')]").click()
        last = driver.find_element(By.XPATH, "//img[@src='./assets/img/last.png']")
        driver.execute_script("arguments[0].click();", last)
        res = self.VerificarusrBD(usuario)
        if res > 0:
            print("Usuario agregado correctamente a la BD")
        else:
            print("Ocurrio un problema al encontrar el usuario en la BD")
            driver.quit()
            return
        find_td = TD_VALIDAR.format(usuario)
        find = hw.getElement(locator=find_td, locatorType="XPATH")
        if not find:
            print("La pagina NO muestra correctamente el usuario")
            driver.quit()
            return
        down = driver.find_element(By.XPATH,"//img[contains(@src,'sort-down.png')]")
        driver.execute_script("arguments[0].click();", down)
        closesession = driver.find_element(By.XPATH, "// button[contains(text(), 'Cerrar sesión')]")
        driver.execute_script("arguments[0].click();", closesession)

        self.closeSshandConection()
        su.Login(driver=driver, user=usuario, passwd=contraseña, element={"locator": "XPATH",
                                                                          "valueL": "//input[@type='text']"})

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

    def closeSshandConection(self):
        self.connection.close()
        self.server.stop()

    def VerificarusrBD(self,USUARIO):
        MONGO_DB = "logDB"
        self.conectionDB()
        db = self.connection[MONGO_DB]
        BD_coll = db["usuarios"]
        Finder = BD_coll.find({"usuario":USUARIO}).count()
        self.closeSshandConection()
        return Finder

    def encuentraUsrFront(self, driver, indice, dato2):
        while True:
            next = driver.find_element(By.XPATH, "//div[@id='pagination']//a[3]")
            filas = driver.find_elements(By.XPATH, "//tbody/tr/td[" + str(indice) + "]//*")
            for campo in filas:
                texto = campo.text
                notfind = -1
                if not texto.find(dato2) == notfind:
                    print("El usuario denegado se encuentra en la pagina(esto es correcto)")
                    return True
            paginas = driver.find_elements(By.XPATH, "//div[@id='pagination']//span")
            print("pagina " + paginas[0].text + " de " + paginas[1].text)
            if paginas[0].text == paginas[1].text:
                break
            else:
                driver.execute_script("arguments[0].click();", next)
                time.sleep(1)
        return False

    def verificarUsuarioAdmin(self):
        try:
            file = codecs.open("/utilities/data.txt", 'r', 'utf-8')
            content = file.read()

        except:
            file = codecs.open("../utilities/data.txt", 'r', 'utf-8')
            content = file.read()
        else:
            print("Archivo data2.txt no enconrado, verifique:\n"
                  "-Que la paqueteria utilities este dentro de su proyecto.\n"
                  "-Y que esta no se encuentr dentro de otra carpeta o paqueteria.\n"
                  "-A su vez que dentro de ella se encuentre el archivo.")

        index = content.find("#-comments-#")
        content = content[:index]
        print(content)
        objetos = json.loads(content)
        User = objetos["login"]
        self.conectionDB()
        db = self.connection["logDB"]
        collection = db["usuarios"]
        exist = collection.find({"usuario": User }).count()
        if exist <= 0:
            print("Usuario inexistente")
            self.closeSshandConection()
            return False
        types =collection.find({"usuario": User })
        for cursor in types:
            if not (cursor['tipo']) == 'admin':
                print("Se necesita un usuario Admin valido")
                self.closeSshandConection()
                return False
            else:
                self.closeSshandConection()
                return True

    def startTest(self, nombre, apellido, correo, area, rol, usuario, contraseña, check):
        if self.verificarUsuarioAdmin():
            la = LogAdmin()
            la.authModal(
                nombre=nombre, apellido= apellido, correo=correo, area=area, rol=rol, usuario=usuario,
                contraseña=contraseña, check=check
            )
        else:
            print("termino")
