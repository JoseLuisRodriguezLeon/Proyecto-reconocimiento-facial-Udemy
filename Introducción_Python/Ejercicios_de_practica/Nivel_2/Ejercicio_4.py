#// Ejercicios de práctica Python

#Ejercicio 4

print("Crea un programa que simule un cajero automaticocon un saldo inicial de 2000€. Debe tener las siguientes funciones: \n")
print("1. Ingresar dinero en la cuenta\n2. Retirar dinero de la cuenta\n3. Mostrar saldo\n4. Salir\n")

saldo = 2000  # Variable global

def menu():
    print("\nSeleccione una opción:")
    print("1. Ingresar dinero")
    print("2. Retirar dinero")
    print("3. Mostrar saldo")
    print("4. Salir")
    
    seleccion = input("Opción: ")
    
    if seleccion == "1":
        ingreso = float(input("Ingrese la cantidad a depositar: "))
        ingresar_dinero(ingreso)
    elif seleccion == "2":
        retiro = float(input("Ingrese la cantidad a retirar: "))
        retirar_dinero(retiro)
    elif seleccion == "3":
        mostrar_saldo()
    elif seleccion == "4":
        print("Gracias por usar el cajero. ¡Hasta pronto!")
        return
    else:
        print("Opción no válida")
        menu()

def ingresar_dinero(ingreso):
    global saldo
    saldo += ingreso
    print(f"Has ingresado {ingreso}€. Tu nuevo saldo es {saldo}€.")
    menu()
    
def retirar_dinero(retiro):
    global saldo
    if retiro > saldo:
        print("Fondos insuficientes para realizar el retiro.")
    else:
        saldo -= retiro
        print(f"Has retirado {retiro}€. Tu nuevo saldo es {saldo}€.")
    menu()
    
def mostrar_saldo():
    global saldo
    print(f"Tu saldo actual es de: {saldo}€")
    menu()

# Iniciar el programa
menu()