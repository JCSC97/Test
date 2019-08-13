from utilities.InicioSesionLog import SingUp
try:
    su = SingUp()
    driver=su.startLoginLog(True)
    driver.quit()
except:
    print("Error")