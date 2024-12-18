from math import pi

#densidad lineal de carga de explosivos
def linear_density(diameter: float | int, density: float, english = False):
    """
    Densidad lineal de carga

    Esta funcion calcula la subida lineal o
    densidad lineal de carga de un explosivo
    para un diámetro y densidad determinados.

    Entradas:
    * diameter: Diametro de carga [mm]
    * density: Densidad del explosivo [g/cm3]

    Salidas:
    * ql: Densidad lineal de carga [kg/m]
    """
    if english == False:
        diameter = diameter/1000
        density = density*1000
        return pi/4*diameter**2*density
    elif english == True:
        diameter = diameter/0.00328084
        density = density/62.428
        return pi/4*diameter**2*density

print(linear_density(64, 0.9))
