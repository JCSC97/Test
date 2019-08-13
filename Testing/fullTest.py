from utilities.InicioSesionLog import SingUp
from utilities.INFO_SEARCH_TEST import Logs
from utilities.ADMIN_MODULE_TEST import LogAdmin
import codecs
import sys
# su = SingUp()
# driver= su.startLoginLog(use=True)

# try:
#     buildjson = "{\n\"modulo\"       : \"" +"Solicitudes"+"\"," \
#                  "\n\"filtro\"       : \"" +"busqueda"+"\"," \
#                  "\n\"buscarPor\"    : \"" +"Document"+"\"," \
#                  "\n\"busca\"        : \"" +"16520"+"\","\
#                  "\n\"fechaInicio\"  : \"" +"30/05/2014"+"\"," \
#                  "\n\"fechaFinal\"   : \"" +"23/06/2019"+"\"\n}"
#
#     f = codecs.open("../utilities/data2.txt", 'w', "utf-8")
#     f.write(str(buildjson)+"\n#-comments-#")
#     f.close()
#     l = Logs()
#     l.startTest(use=False)
# except:
#     print("Busqueda no finalizada, no se encontraron solicitudes con esos parametros", sys.exc_info())


# try:
#     buildjson = "{\n\"modulo\"       : \"" +"Usuarios"+"\"," \
#                  "\n\"filtro\"       : \"" +"busqueda"+"\"," \
#                  "\n\"buscarPor\"    : \"" +"Responsable"+"\"," \
#                  "\n\"busca\"        : \"" +"CARLOS"+"\","\
#                  "\n\"fechaInicio\"  : \"" +"30/05/2014"+"\"," \
#                  "\n\"fechaFinal\"   : \"" +"23/06/2019"+"\"\n}"
#
#     f = codecs.open("../utilities/data2.txt", 'w', "utf-8")
#     f.write(str(buildjson)+"\n#-comments-#")
#     f.close()
#     l = Logs()
#     l.startTest(use=False)
# except:
#     print("Busqueda no finalizada, no se encontraron responsables con esos parametros.",sys.exc_info())



# try:
#     l = Logs()
#     l.startTest(use=False)
#     buildjson = "{\n\"modulo\"       : \"" +"Sociedades"+"\"," \
#                  "\n\"filtro\"       : \"" +"busqueda"+"\"," \
#                  "\n\"buscarPor\"    : \"" +"Acción"+"\"," \
#                  "\n\"busca\"        : \"" +"Eliminación"+"\","\
#                  "\n\"fechaInicio\"  : \"" +"30/05/2014"+"\"," \
#                  "\n\"fechaFinal\"   : \"" +"23/06/2019"+"\"\n}"
#
#     f = codecs.open("../utilities/data2.txt", 'w', "utf-8")
#     f.write(str(buildjson)+"\n#-comments-#")
#     f.close()
#     l = Logs()
#     l.startTest(use=False)
# except:
#     print("Busqueda no finalizada, no se encontraron sociedades eliminadas con esos parametros",sys.exc_info())
# print("--------------------------------------------------------------------------------")
#
# try:
#
#     la = LogAdmin()
#     la.startTest(
#         nombre="Yadira",
#         apellido="Vargas",
#         correo="yadii1113@gmail.com",
#         rol="user",
#         area="Testing",
#         usuario="miamor",
#         contraseña="123tamarindo",
#         check=False
#     )
# except:
#     print("Error Inesperado",sys.exc_info())
#
try:
    from utilities.Editar_Usuario import Edit_Usuer
    ed = Edit_Usuer()
    ed.EditarUsuario(search="miamor",
                     rol='admin',
                     check=True
    )
except:
    print("Error Inesperado",sys.exc_info())

