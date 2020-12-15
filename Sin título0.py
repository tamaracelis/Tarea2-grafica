# Por: Benja Vera
# Nota: Ya que esto es para una ocasión super puntual y todo el mundo involucrado probablemente sabe programar mejor que yo,
# no me voy a molestar en chequear inputs :)

horasTotales = 240
diaPrimeraEntrega = int(input("¿Qué día de octubre entregaste la tarea 1? (ej: 24)\n"))
horaPrimeraEntrega = int(input("Genial ¿Y a qué hora? (ingrese un solo entero de 0 a 23, ej: 15)\n"))
if diaPrimeraEntrega <= 14:
    horas1 = 0
elif 15 <= diaPrimeraEntrega <= 17:  # primeros días
    horas1 = (diaPrimeraEntrega - 15)*24 + horaPrimeraEntrega
elif 18 <= diaPrimeraEntrega <= 25:  # receso, las 72 horas se congelan
    horas1 = 72
else:
    horas1 = 72 + (diaPrimeraEntrega - 26)*24 + horaPrimeraEntrega  # luego, desde el lunes 26, cuentan a partir de 72

if horas1 > 240:  # si con la T1 sobrepasa el límite...
    raise Exception('F')  # u.u
print("Bacán, usaste " + str(horas1) + " horas del total de 240 en la primera tarea.")

# Nota a mi yo del futuro: Cambiar de aquí en adelante para la tarea 3

horasR = horasTotales - horas1
diasRestantes = horasR//24  # división entera
horasRestantes = horasR%24  # módulo
print("Hagamos un resumen: te quedan " + str(horasR) + " horas en total luego de las que usaste para la T1. Esto se traduce a "\
     + str(diasRestantes) + " días y " + str(horasRestantes) + " horas (no estoy considerando el atraso que ya puedes llevar en la T2)")

if diasRestantes <= 2:  # si no se pasa del domingo, da lo mismo
    print("Esto significa que puedes entregar hasta el día " + str(10 + diasRestantes) + " a las " + str(horasRestantes) + " hrs sin descuento :)")
else: # aquí, tenemos que no considerar el domingo
    print("Teniendo en mente que los domingos no descuentan, esto significa que puedes entregar hasta el día " + str(10 + diasRestantes + 1) \
        + " a las " + str(horasRestantes) + " hrs sin descuento :)")

out = input("Mucho ánimo con lo que queda del semestre! Presiona ENTER para salir: ")