from utilities.InicioSesion import SingUp
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import selenium.common.exceptions as ES
import time, json
from utilities.handy_wrappers import HandyWrappers
from utilities.CSV_read_and_write import CSVclass
import os
from selenium.webdriver.common.keys import Keys
import unittest
import sys
import pymongo
from sshtunnel import SSHTunnelForwarder
connection = None
server = None
#--------------------------------------------------------------------
IN_NOMBRE ="//input[@placeholder='Nombre']"
IN_APELLIDO ="//input[@placeholder='Apellido']"
IN_EMAIL = "//input[@placeholder='ejemplo@correo.com']"
IN_AREA = "//input[@placeholder='Área']"
IN_ROL = "//select[@value='Rol']"
IN_USUARIO ="//input[@placeholder='Usuario']"
IN_CONTRASEÑA = "//input[@placeholder='Contraseña']"
BTN_ACTIVO = "//label[@class='checkbox-inline']"
BTN_GUARDAR = "//*[@type='submit']"
BTN_ACEPTAR = "//button[text()=' Aceptar']"
BTN_ROWDOWN = "//a[@class='down dropdown-toggle']"
BTN_LOGOUT = "//button[text()='Cerrar sesión']"
TD_VALIDAR = "//tbody//tr//td[6]//*[text()='{0}']"
Usuaio_Actual=""
#---------------------------------------------------------------------
class Edit_Usuer():
    def __init__(self):
        pass

    def EditarUsuario(self, search, nombre="", apellido="", correo="", area="", rol="", usuario="", contraseña="", check=""):
        SU = SingUp()
        driver = SU.startLogin(use=True)
        driver.find_element_by_xpath("//a[@href='#/administracion/:modulo']").click()
        datosTabla = self.BuscarDato(driver, search, "Usuario")
        edit = driver.find_elements(By.XPATH, "//tbody//td[8]//*")
        if not datosTabla == None:
            fila = datosTabla['fila']
            edit[fila-1].click()
        else:
            return
        time.sleep(1)
        self.authModal(driver, nombre, apellido, correo, area, rol, usuario, contraseña, check, search)
        #---------------------------------------------------------------

    def BuscarDato(self,driver,dato,campo):
        try:
            driver.find_element_by_xpath("//table")
            print("Tabla Encontrada")
        except:
            print("Tabla no encontrada")
            return None
        try:
            titulo = driver.find_elements_by_xpath('//thead//th//*')
        except:
            print("Parece que la tabla no cuenta con un 'head'")
            return None
        size = len(titulo)
        count1 = 1
        for camp in titulo:
            Ncampo = camp.text
            if Ncampo == campo:
                print("Campo: " + campo +" encontrado")
                break
            count1 += 1
            if count1 > size:
                print("Campo no encotrado")
                return None

        find = False
        while True:
            next = driver.find_element(By.XPATH, "//div[@id='pagination']//a[3]")
            campos = driver.find_elements(By.XPATH, "//tbody//td["+str(count1)+"]")
            count2 = 1
            for camp in campos:
                Ncampo = camp.text
                print("El dato en la tabla: "+Ncampo)
                if Ncampo == dato:
                    print("Campo: " + dato +" encontrado")
                    find = True
                    break
                count2 += 1
            paginas = driver.find_elements(By.XPATH, "//div[@id='pagination']//span")
            print("pagina " + paginas[0].text + " de " + paginas[1].text)
            if paginas[0].text == paginas[1].text and not find:
                print("dato no encontrado :(")
                return None
            elif find:
                break
            else:
                driver.execute_script("arguments[0].click();", next)
                time.sleep(1)

        print("El dato se encuantra en la columna " + str(count1) + " y la fila " + str(count2))
        datos = {'campo': count1, 'fila': count2}
        return datos

    def authModal(self, driver, nombre, apellido, correo, area, rol, usuario, contraseña, check, search):
        su = SingUp()
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
        su.takescreenshot(driver, namescren="Modal", directory="TestModuleAdmin/")

        try:
            element = driver.find_element(By.XPATH, "//input[@name='nombre']")
            element1 = driver.find_element(By.XPATH, "//input[@name='apellido']")
            element2 = driver.find_element(By.XPATH, "//input[@name='correo']")
            element3 = driver.find_element(By.XPATH, "//input[@name='area']")
            select = driver.find_element(By.XPATH, "//select[@name='rol']")
            element4 = driver.find_element(By.XPATH, "//input[@name='usuario']")
            element5 = driver.find_element(By.XPATH, "//input[@type='password']")
            checking = driver.find_element(By.XPATH, "//input[@type='checkbox']")
            if not nombre == "":
                driver.execute_script('arguments[0].value = "";',element)
                element.send_keys(nombre)
            if not apellido == "":
                driver.execute_script('arguments[0].value = "";', element1)
                element1.send_keys(apellido)
            if not correo == "":
                driver.execute_script('arguments[0].value = "";', element2)
                element2.send_keys(correo)
            if not area == "":
                driver.execute_script('arguments[0].value = "";', element3)
                element3.send_keys(area)
            if not rol == "":
                sel = Select(select)#select
                sel.select_by_value(rol)
            if not usuario == "":
                driver.execute_script('arguments[0].value = "";', element4)
                element4.send_keys(usuario)
            if not contraseña == "":
                driver.execute_script('arguments[0].value = "";', element5)
                element5.send_keys(contraseña)
            if not check == "":
                if not checking.is_selected():
                    if check:
                        driver.execute_script("arguments[0].click();", checking)
                else:
                    if not check:
                        driver.execute_script("arguments[0].click();", checking)
            su.takescreenshot(driver, namescren="CamposLlenos", directory="TestModuleAdmin/")
            # -----------------------------obtener datos---------------------------------

            nombre = element.get_property("value")
            apellido = element1.get_property("value")
            correo = element2.get_property("value")
            area = element3.get_property("value")
            rol = select.get_property("value")
            usuario = element4.get_property("value")
            if checking.is_selected():
                check = True
            else:
                check = False

            datos = {"usuario": usuario, "nombre": nombre, "tipo": rol, "activo": check, "area": area, "email": correo
                , "apellidos": apellido}
            # ---------------------------------------------------------------------------
            save = driver.find_element(By.XPATH, "//input[contains(@type,'submit') and contains(@value,'Guardar')]")
            driver.execute_script("arguments[0].click();", save)

            time.sleep(2)
        except:
            print("Error inesperado al registrar usuario :", sys.exc_info()[0])
            driver.quit()
            return

        hw = HandyWrappers(driver)
        if hw.elementPresenceCheck(locator="//*[text()='¡El usuario ya existe!']",byType="xpath"):
            if search == usuario:
                print("El sistema denego su mismo usuario")
                su.takescreenshot(driver, namescren="UsuarioExiste", directory="TestModuleAdmin/")
                driver.find_element(By.XPATH, "//button[contains(text(),'Aceptar')]").click()
            else:
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
        res = self.validarUsrBD(datos)
        if res > 0:
            print("Usuario modificado correctamente a la BD")
        else:
            print("Ocurrio un problema al encontrar el usuario en la BD")
            driver.quit()
            return

        usuarioModificado = self.BuscarDato(driver,dato= usuario, campo='Usuario')
        if usuarioModificado is not None:
            fila = usuarioModificado['fila']
            datos=[nombre, apellido, rol, correo, area, usuario, check]
            correcto = self.verificarDatoUsr(driver, fila, datos)
            if correcto:
                print("los datos del usuario se muestran de manera correcta")
            else:
                print("un dato del usuario modificado no coincidio")
                driver.quit()
                return
        else:
            print("el usuario modificado no se muestra en el front")
            driver.quit()
            return

        down = driver.find_element(By.XPATH,"//img[contains(@src,'sort-down.png')]")
        driver.execute_script("arguments[0].click();", down)
        closesession = driver.find_element(By.XPATH, "// button[contains(text(), 'Cerrar sesión')]")
        driver.execute_script("arguments[0].click();", closesession)

        self.closeSshandConection()
        #su.Login(driver=driver, user=usuario, passwd=contraseña, element={"locator": "XPATH","valueL": "//input[@type='text']"})

    def encuentraUsrFront(self, driver, indice, dato2):
        while True:
            next = driver.find_element(By.XPATH, "//div[@id='pagination']//a[3]")
            filas = driver.find_elements(By.XPATH, "//tbody/tr/td[" + str(indice) + "]//*")
            for campo in filas:
                texto = campo.text
                notfind = -1
                if not texto.find(dato2) == notfind:
                    return True
            paginas = driver.find_elements(By.XPATH, "//div[@id='pagination']//span")
            print("pagina " + paginas[0].text + " de " + paginas[1].text)
            if paginas[0].text == paginas[1].text:
                break
            else:
                driver.execute_script("arguments[0].click();", next)
                time.sleep(1)
        return False

    def closeSshandConection(self):
        self.connection.close()
        self.server.stop()

    def VerificarusrBD(self, USUARIO):
        MONGO_DB = "logDB"
        self.conectionDB()
        db = self.connection[MONGO_DB]
        BD_coll = db["usuarios"]
        Finder = BD_coll.find({"usuario": USUARIO}).count()
        self.closeSshandConection()
        return Finder

    def verificarDatoUsr(self, driver, fila, datos):
        xpath = "//tbody//tr[{0}]/td/*"
        xpath = xpath.format(fila)
        campos = driver.find_elements(By.XPATH, xpath)
        count = 0
        for dato in datos:
            print("dato en Front: "+str(campos[count].text)+", dato enviado:"+str(dato))
            if count == 6:
                estilo =str(campos[count].get_attribute("style"))
                print("estilo para verde: "+ str(estilo.find("green")))
                print("estilo para rojo: "+ str(estilo.find("red")))
                if estilo.find("green") > -1 and dato:
                    print("entro 1")
                    pass
                elif estilo.find("red") > -1 and not dato:
                    pass
                else:
                    self.closeSshandConection()
                    return False
            elif not count == 6:
                if not dato == campos[count].text:
                    self.closeSshandConection()
                    return False
                count += 1
        return True

    def validarUsrBD(self,datos):
        MONGO_DB = "logDB"
        self.conectionDB()
        db = self.connection[MONGO_DB]
        collection = db["usuarios"]
        cursor = collection.find({"usuario": datos["usuario"]})
        obj = cursor[0]
        for key in datos:
            print("base de datos: "+str(obj[key])+", dato enviado: " +str(datos[key]))
            if not obj[key] == datos[key]:
                print("El dato: "+str(key+" no coincide"))
                self.closeSshandConection()
                return 0
        return 1

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