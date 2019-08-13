from selenium import webdriver
from selenium.webdriver.common.by import By
import time, json
from utilities.CSV_read_and_write import CSVclass
from utilities.handy_wrappers import HandyWrappers
from utilities.CSV_read_and_write import CSVclass
import selenium.common.exceptions as ES
import os
#version 2 del script de automatizacion
#En esta version se le agrego un metodo (takescreenshot), para optimizacion de codigo, ahora por cada accion realizada
#se toma una screenshot para llevar un mejor seguimiento del proceso, ademas se creo un pequeño framework para poder
#guardar los datos de salida en archivos .CSV, esto nos permite tener la informacion de la prueba mas a la mano y de
#manera que la podamos manipular facilmente.
#Por ultimo se agrego una funcionalidad que nos permite tomar los datos de entrada desde un archivo que contiene
#formato Json

InLogin = 'user'
InPass = 'password'
ElmentAccess = 'Iniciar Sesión'
observations = ''
results =''
takeS=0
class SingUp():
    def  __init__(self):
        pass

    def Login(self, driver, user='', passwd="", typeU=""):
        self.takeS=0
        self.observations = ''
        self.results = ''
        fielnames=['usuario', 'contraseña', 'tipoUsuario', 'resultados','No. de capturas', 'observaciones']
        typeU = typeU.lower()

        hw = HandyWrappers(driver)
        driver.implicitly_wait(3)
        self.takescreenshot(driver, namescren='IniciaPruebaLogin',
                            directory="ScreenshotsPruebaLogin/")
        self.takeS += 1
        locator = By.XPATH
        driver.find_element(locator, "//input[@formcontrolname='"+InLogin+"']").send_keys(user)
        driver.find_element(By.XPATH, "//input[@type='"+InPass+"']").send_keys(passwd)
        self.takescreenshot(driver, namescren='LlenadoDeDatos',
                            directory="ScreenshotsPruebaLogin/")
        self.takeS += 1
        driver.find_element(By.XPATH, "//input[@value='"+ElmentAccess+"']").click()
        buttonAceptar = hw.isElementPresent(locator="//button[text()='Aceptar']", byType=By.XPATH)
        self.observations = hw.returnResults()
        if buttonAceptar:
            time.sleep(1)
            #-----------------------------screenshot-------------------------------------------------
            driver.find_element(By.XPATH, "//button[text()='Aceptar']").click()
            time.sleep(2)
            print("Ocurrio un problema de autenticacion(datos incorrectos o informacion faltante)")

            self.takescreenshot(driver, namescren='FalloAutenticacion',
                                directory="ScreenshotsPruebaLogin/")
            self.takeS += 1
            self.results='Ocurrio un problema de autenticacion(datos incorrectos o informacion faltante)'
            data = [{'usuario': user, 'contraseña': passwd, 'tipoUsuario': typeU, 'resultados': self.results,
                     'No. de capturas': self.takeS, 'observaciones': self.observations}]
            csv = CSVclass()
            csv.writeCSV(fieldnames=fielnames, data=data, name='resultadosTC1_INICIO_SESION')

            return False

        elements = driver.find_elements(By.XPATH,"//li//a")
        if typeU == 'simple':
            if len(elements) == 3 :
                self.results='Autenticacion de usuario simple exitosa'
                print(self.results)

                self.takescreenshot(driver, namescren='AtenticacionExitosaParaUsuario'+typeU,
                                    directory="ScreenshotsPruebaLogin/")
                self.takeS += 1
            else:
                self.takescreenshot(driver, namescren='AtenticacionFallidaParaUsuario'+typeU,
                                    directory="ScreenshotsPruebaLogin/")
                self.takeS += 1
                self.results=("Autenticacion de usuario simple fallida")
                print(self.results)
        elif typeU == 'administrador':
            if len(elements) == 4 :
                self.results=("Autenticacion de usuario administrador exitosa")
                print(self.results)
                self.takescreenshot(driver, namescren='AtenticacionExitosaParaUsuario'+typeU,
                                    directory="ScreenshotsPruebaLogin/")
                self.takeS += 1
            else:
                self.takescreenshot(driver, namescren='AtenticacionFallidaParaUsuario'+typeU,
                                    directory="ScreenshotsPruebaLogin/")
                self.takeS += 1
                self.results=("Autenticacion de usuario administrador fallida")
                print(self.results)
        data= [{'usuario': user, 'contraseña': passwd, 'tipoUsuario': typeU,'resultados': self.results, 'No. de capturas': self.takeS, 'observaciones': self.observations}]
        csv = CSVclass()
        csv.writeCSV(fieldnames=fielnames,data=data,name='resultadosTC1_INICIO_SESION')
        time.sleep(2)
        return True

    def takescreenshot(self, driver, namescren='', directory=''):
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)
        fileName = str(round(time.time() * 1000)) + namescren + ".png"
        screenshotDirectory = directory
        destinationfile = screenshotDirectory + fileName
        try:
            driver.save_screenshot(destinationfile)
            print("Captura de pantalla salvada en--> :: " + destinationfile)

        except NotADirectoryError:
            print("Ocurrio un problema en el directorio ")

    def createCVS(self, fieldnames, data, name):
        csv = CSVclass()
        csv.writeCSV(fieldnames=fieldnames, data=data, name=name)
    def startLoginLog(self, use=False):
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
        passwd= objetos['passwd']
        typeU = objetos['typeUser']
        url= objetos['url']
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            driver.maximize_window()
            try:
                val=su.Login(driver, user=user, passwd=passwd, typeU=typeU)
                if not val:
                    return None
            except:
                self.takescrrenshot(driver, namescren="Excepcion", directory="ScreenshotsPruebaLogin/")

                self.createCVS(fieldnames=["Excepcion"], data=[{"Excepcion": "Una excepcion inesperada ocurrio"}],
                               name="Exception")
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