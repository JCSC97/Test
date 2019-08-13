# ------------------------ DOCUMENTACIÓN --------------------------------
# <copyright file="InicioSesion" company="GLOUU TECHNOLOGIES">
#     Copyright (c) Glouu Technologies. All rights reserved.
# </copyright>
# <author>Julio C. Saldivar</author>
# <rastreo>GR_LOG_Caso_de_Prueba_INICIO_SESION</rastreo>
# -----------------------------------------------------------------------
from selenium import webdriver
import selenium.common.exceptions as ES
from selenium.webdriver.common.by import By
import time, json
from utilities.handy_wrappers import HandyWrappers
from utilities.CSV_read_and_write import CSVclass
import os
InLogin = 'user'
InPass = 'password'
ElmentAccess = 'Iniciar Sesión'
observations = ''
results = ''
locator = ''
valueL = ''
takeS = 0

# <SingUp>
# Clase Principal, contiene el metodo para iniciar sesion y su vez otros metodos que pueden ser usados en otro programa
# </SingUp>
# <param></param>
# <returns></returns>
class SingUp():
    def  __init__(self):
        pass

    # <Login>
    # El método Login se encarga de manejar el inicio de sesión después de haber abierto el navegador,
    # a su vez este mismo valida si la autenticación es valida.
    # </Login>
    # <param driver= None, user ='', passwd='', element=[]>
    # Necesita un driver con una sesión abierta del navegador, y apuntando al enlace donde se encuentra el Login,
    # tambien requiere el usuario y password para poder llenar los campos
    # el ultimo parametro es un diccionario para poder hacer la busqueda de el elemento para ingresar el usuario.
    # </param>
    # <returns>
    # El metodo como tal no retorna nada pero a su paso,toma capturas de pantalla en el proceso y los resultados
    # se ven refeljados en un archivo .csv, ambas partes son guardadas en el equipo.
    # </returns>
    def Login(self, driver=None,user='', passwd="", element={}):
        self.takeS = 0
        self.observations = 'without observations'
        self.results = ''
        self.valueL=''
        self.locator=''
        fieldnames = ['user', 'password', 'results', 'Number of screenshots', 'observations']
        driver.maximize_window()
        hw = HandyWrappers(driver)
        if len(element) < 0:
            self.locator = By.XPATH
            self.valueL = "//input[@type='text']"
        else:
            self.locator = hw.getByType(element['locator'])
            self.valueL = element['valueL']

        driver.implicitly_wait(3)
        self.takescreenshot(driver, namescren='TestStartLogin', directory="ScreenshotsPruebaLogin/")
        self.takeS += 1
        # ---------------------------------------------------------------------------------------------------------------
        A = driver.find_elements(self.locator, self.valueL )

        if len(A) > 1:
            for element in A:
                try:
                    element.send_keys(user)
                except:
                    pass
        elif len(A) == 1:
            A[0].send_keys(user)
        else:
            print("element "+self.valueL+" not found, process finished")
            self.results= "AuthenticationFail"
            self.observations= "element "+self.valueL+" not found, process finished"
            data = [{'user': user, 'password': passwd, 'results': self.results,
                     'Number of screenshots': self.takeS, 'observations': self.observations}]
            self.createCVS(fieldnames, data, name = self.results)
            return
        B = driver.find_elements(By.XPATH, "//input[@type='password']")
        if len(B) > 1:
            for element in B:
                try:
                    element.send_keys(passwd)
                except:
                    pass
        elif len(B) == 1:
            B[0].send_keys(passwd)
        else:
            print("element for put password not found, process finished")
            self.results = "AuthenticationFail"
            self.observations = "element for put password not found, process finished"
            data = [{'user': user, 'password': passwd, 'results': self.results,
                     'Number of screenshots': self.takeS, 'observations': self.observations}]
            self.createCVS(fieldnames, data, name = self.results)
            return
        self.takescreenshot(driver, namescren="FillFields", directory="ScreenshotsPruebaLogin/")
        self.takeS += 1
        C = driver.find_elements(By.XPATH, "//*[@type='submit']")
        if len(C) > 1:
            for element in C:
                try:
                    element.click()
                except:
                    pass

        elif len(C) == 1:
            C[0].click()
        else:
            print("button to start session up not found, process finished")
            self.results = "AuthenticationFail"
            self.observations = "Button to start session not found, process finished"
            data = [{'user': user, 'password': passwd, 'results': self.results,
                     'Number of screenshots': self.takeS, 'observations': self.observations}]
            self.createCVS(fieldnames, data, name = self.results)
            return

        time.sleep(3)
        print("validating authentication")
        V1 = hw.elementPresenceCheck(locator=self.valueL, byType=self.locator)
        V2 = hw.elementPresenceCheck(locator="//input[@type='password']", byType=By.XPATH)
        V3 = hw.elementPresenceCheck(locator="//*[@type='password']", byType=By.XPATH)
        if V1 and V2 and V3:
            self.takescreenshot(driver, namescren="AuthenticationFail", directory="ScreenshotsPruebaLogin/")
            self.takeS += 1
            self.results= "AuthenticationFail"

        else:
            self.takescreenshot(driver, namescren="AuthenticationSuccessful", directory="ScreenshotsPruebaLogin/")
            self.takeS += 1
            self.results = "AuthenticationSuccessful"
        data = [{'user': user, 'password': passwd, 'results': self.results,
                 'Number of screenshots': self.takeS, 'observations': self.observations}]
        self.createCVS(fieldnames, data, name = self.results)

    # <takescreenshot>
    # El método takescreenshot se crea para facilitar una captura de pantalla, ya que para tener una evidencia completa
    # son necesarias varias capturas de pantalla
    # </takescreenshot>
    # <param driver, namescren ='', directory=''>
    # Por obviedad es necesario un driver, asi la captura de pantalla se realizará en el estado actual de ese driver
    # el nombre con el que se desea guardar y el directorio son los datos necesarios para hacer una screenshot
    # </param>
    # <returns>
    #
    # </returns>
    def takescreenshot(self, driver, namescren='', directory='TestScreenshots/'):
        if not namescren == '':
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)
            fileName = str(round(time.time() * 1000)) + namescren + ".png"
            screenshotDirectory = directory
            destinationfile = screenshotDirectory + fileName
            try:
                driver.save_screenshot(destinationfile)
                print("Captura de paantalla salvada en--> :: " + destinationfile)
            except NotADirectoryError:
                print("Error de directorio")
        else:
            print("envia un nombre del archivo")
    # <createCSV>
    # El método createCSV tiene la simple finalidad de reducir esfuerzo al crear el archivo
    # </createCSV>
    # <param namescren ='', directory='', name>
    # son necesarios los nombres de los datos y la informacion a guardar
    # , fieldnames debe ser un arreglo de cadena y data debe ser un arreglo de diccionarios,
    # es muy necesario que los fieldnames y los inideces del diccionario sean los mismos.
    # por ultimo el nombre que tendrá el archivo.
    # </param>
    # <returns>
    #
    # </returns>
    def createCVS(self, fieldnames, data, name):
        csv = CSVclass()
        csv.writeCSV(fieldnames=fieldnames, data=data, name=name)

    # <StartLogin>
    # El método StartLogin inicia un driver de selenium de Google Chrome.
    # los datos del inicio de sesión que requiere el metodo SingUp son tomados de
    # un archivo de configuración llamado data.txt, despues envia esos datos al metodo
    # SingUp.
    # </startLogin>
    # <param use=False>
    # Al usar metodo en otro programa, el parametro use nos ayuda a decirdir si despues de un login, la sesión seguira
    # abierta o no, esto para poder seguir usandola.
    # </param>
    # <returns>
    # Si decidimos usar la sesión al finalizar el inicio de sesión nos
    # devuelve el driver de lo contrario retorna None.
    # </returns>
    def startLogin(self,use = False):
        su = SingUp()
        try:
            file = open("/utilities/data.txt", 'r')
            content = file.read()

        except:
            file = open("../utilities/data.txt", 'r')
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
        user = objetos['login']
        passwd = objetos['passwd']
        url = objetos['url']
        locator = objetos['locatorLogin']
        valueL = objetos['valueLocatorI']
        element = {'locator': locator, 'valueL': valueL}
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            try:
                su.Login(driver= driver,user=user, passwd=passwd, element=element)
            except:
                self.takescrrenshot(driver, namescren="Exeption",directory="ScreenshotsPruebaLogin/")

                self.createCVS(fieldnames=["Exception"],data=[{"Excepciion":"una excepcion inesperada ocurrio"}],name="Exception")
                driver.quit()
                return None
            if not use:
                driver.quit()
                return None
            else:
                return driver
        except ES.WebDriverException:
            print("Un error fuera del alcance del script se generó.\n"
                  "Asegurese de no manipular la ventana en ejecucion.\n"
                  "Y que el url que introdujo es correcto")
            driver.quit()
            return None
