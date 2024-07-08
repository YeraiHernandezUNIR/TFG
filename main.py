import os

def print_centered(text, width):
    return text.center(width)

def print_header():
    width = 80
    print("=" * width)
    print(print_centered("TFG: Análisis de WEBS para la valoración de su contenido", width))
    print(print_centered("Realizado por: Yerai Miguel Hernández Fariña", width))
    print("=" * width)
    print("\n")

def print_menu():
    width = 80
    print("=" * width)
    print(print_centered("SELECCIONE UNA OPCIÓN", width))
    print("=" * width)
    print("1 - Pulse 1 para acceder al analizar de páginas WEB".ljust(width))
    print("2 - Pulse 2 para acceder a la base de datos de las páginas WEB".ljust(width))
    print("3 - Pulse 3 para salir del programa".ljust(width))
    print("=" * width)

def main():
    print_header()
    while True:
        print_menu()
        choice = input("\nIndique que opción desea usar: ")
        
        if choice == '1':
            os.system('python crawler.py')
        elif choice == '2':
            os.system('python consultar_mongodb.py')
        elif choice == '3':
            width = 80
            print("=" * width)
            print(print_centered("Gracias por utilizar Análisis de WEBS para la valoración de su contenido", width))
            print("=" * width)
            break
        else:
            print("La opción indicada no es existe, por favor introduzca una opción válida.")

if __name__ == "__main__":
    main()
