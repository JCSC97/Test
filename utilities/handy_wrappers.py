#  --------------------------- DOCUMENTACIÓN ------------------------------
# <copyright file="handy_wrappers" company="GLOUU TECHNOLOGIES">
#     Copyright (c) Glouu Technologies. All rights reserved.
# </copyright>
# <author>Julio C. Saldivar</author>
# <rastreo></rastreo>
# -------------------------------------------------------------------------
from selenium.webdriver.common.by import By
# <HandyWrappers>
# Clase Principal, contine metodos que ayuda a facilitar el manejo de elementos
# </HandyWrappers>
# <param driver> el manejador que se va a manejar en toda la clase</param>
# <returns></returns>
class HandyWrappers():
    results = ''
    def __init__(self, driver):
        self.driver = driver

    # <getByType>
    # Obtiene tipo de localizador que maneja selenium a traves de la libreria By
    # </getByType>
    # <param locatorType> este parametro recibe una cadena con el nombre de in tipo de localizador </param>
    # <returns> retorna el tipo de localizador valido o un False en caso de haber encontrado el localizador</returns>
    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "classname":
            return By.CLASS_NAME
        elif locatorType == "linktext":
            return By.LINK_TEXT
        else:
            print("Localizador de tipo " + locatorType + " no es correcto/soportado")
        return False

    # <getELement>
    # este método nos ayuda encontrar un elemento de forma mas dinamica
    # </getElement>
    # <param locator='', locatorType='id'> locatorType es el tipo de localizador que se usara
    # y locator es el parametro de la busqueda
    # </param>
    # <returns> regresa el elemento en caso de encontrarlo o None en caso de no encontrarlo</returns>
    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.results= "Elemento "+str(locator)+" Encontrado"
            print("Elemento "+str(locator)+" encontrado")
        except:
            self.results = "Elemento " + str(locator) + " no encontrado"
            print("Elemento "+str(locator)+" no encontrado")
        return element

    # <isElementPresent>
    # metodo que nos ayuda a saber si un elemento se encuentra o no
    # </isElementPresent>
    # <param locator='', byType='id'> byType es el tipo de localizador que se usara
    # y locator es el parametro de la busqueda
    # </param>
    # <returns></returns>
    def isElementPresent(self, locator, byType):
        try:
            element = self.driver.find_element(byType, locator)
            if element is not None:
                self.results = "Elemento " + str(locator) + " encontrado"
                print("Elemento "+str(locator)+" encontrado")
                return True
            else:
                self.results = "Elemento " + str(locator) + " no encontrado"
                print("Elemento "+str(locator)+" no encontrado")
                return False

        except:
            self.results="Elemento " + str(locator) + " no encontrado"
            print("Elemento "+str(locator)+" no encontrado")
            return False

    # <elementPresenceCheck>
    # metodo que nos ayuda a saber si un elemento se encuentra o no, de una manera diferente al otro
    # esta podria ser una alernatica en caso de que no funcione la anterior
    # </elementPresenceCheck>
    # <param locator='', byType='id'> byType es el tipo de localizador que se usara
    # y locator es el parametro de la busqueda
    # </param>
    # <returns></returns>
    def elementPresenceCheck(self,locator, byType):
        try:
            element = self.driver.find_elements(byType, locator)
            if len(element) > 0:
                self.results = "Elemento " + str(locator) + " encontrado"
                print("Elemento " + str(locator) + " encontrado")
                return True
            else:
                self.results = "Elemento " + str(locator) + " no encontrado"
                print("Elemento "+str(locator)+" no encontrado")
                return False

        except:
            self.results = "Elemento " + str(locator) + " no encontrado"
            print("Elemento "+str(locator)+" no encontrado")
            return False
    def returnResults(self):
        return self.results
