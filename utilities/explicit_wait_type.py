# -------------------------- DOCUMENTACIÓN ---------------------------------
# <copyright file="ATCS_GR_Log_Inicio_Sesion" company="GLOUU TECHNOLOGIES">
#     Copyright (c) Glouu Technologies. All rights reserved.
# </copyright>
# <author>Orlando Pulido</author>
# <rastreo>GR_LOG_Caso_de_Prueba_INICIO_SESION</rastreo>
# -------------------------------------------------------------------------
from utilities.handy_wrappers import HandyWrappers
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *

# <ExplicitWaitType>
# Clase Principal
# </ExplicitWaitType>
# <param driver> el manejador que se va a manejar en toda la clase</param>
# <returns></returns>
class ExplicitWaitType():
    def __init__(self, driver):
        self.driver= driver
        self.hw = HandyWrappers
    # <waitForElement>
    # metodo que nos ayuda a encontrar un elemento pero de otro tipo, es decir,
    # esos elementos que no cargan al instante y que tardan en aparecer.
    # </waitForElement>
    # <param locator='', byType='id',timeout=10> byType es el tipo de localizador que se usara
    # y locator es el parametro de la busqueda, y timeout es el tiempo maximo de espera en segundos
    # </param>
    # <returns>nos retorna el elemento en caso de aprecer, de lo contario nos devuelve None</returns>
    def waitForElement(self, locator, locatorType="id", timeout=10):
        element= None
        try:
            hw = HandyWrappers(self.driver)
            locatorType=hw.getByType(locatorType)
            print("Espera maxima de:: "+str(timeout)+
                  ":: segundos para que el elemento sea usable")
            element = WebDriverWait(self.driver, timeout, poll_frequency=1,
                                   ignored_exceptions=[NoSuchElementException]).until(lambda driver:
                                   self.driver.find_element(locatorType,locator))
            print("Elemento aparecio en la pagina web")
        except:
            print("Elemento aparecio no en la pagina web")

        return  element