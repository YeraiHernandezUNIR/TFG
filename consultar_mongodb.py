import subprocess
import pymongo

# Configuración de MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["web-analysis"]
collection = db["pages"]

def print_centered(text, width):
    return text.center(width)

def print_header():
    width = 80
    print("=" * width)
    print(print_centered("CONSULTAR RESULTADOS", width))
    print("=" * width)

def print_menu():
    width = 80
    print("1 - Listar todos los resultados de la base de datos.".ljust(width))
    print("2 - Ver el resultado de una página WEB específica.".ljust(width))
    print("3 - Volver al menú principal.".ljust(width))
    print("=" * width)

def print_result(page_data):
    width = 80
    print("=" * width)
    print(print_centered(f"RESULTADO PARA: {page_data['url']}", width))
    print("=" * width)
    print(f"- El contenido es para: {page_data['audience']}.".ljust(width))
    print(" ")
    print(f"- El contenido se asocia a: {page_data['content_type']}.".ljust(width))
    print(" ")
    print(f"- Breve resumen de la WEB indicada: {page_data['summary']}.".ljust(width))
    print("=" * width)
    print(" ")

def list_all_results():
    width = 80
    results = collection.find()
    if collection.count_documents({}) == 0:
        print("=" * width)
        print(print_centered("No se han encontrado resultados en la base de datos.", width))
        print("=" * width)
    else:
        for page_data in results:
            print_result(page_data)

def view_specific_result():
    url = input("Introduzca la dirección de la página WEB que desea consultar: ")
    results = list(collection.find({"url": url}))  # Convertir a lista para contar fácilmente
    width = 80
    if len(results) > 0:
        for page_data in results:
            print_result(page_data)
    else:
        print("=" * width)
        print(print_centered("La página WEB indicada aún no ha sido analizada.", width))
        print("=" * width)

def main():
    while True:
        print_header()
        print_menu()
        choice = input("\nIndique que opción desea usar: ")
        
        if choice == '1':
            list_all_results()
            input("Pulse enter para continuar")
        elif choice == '2':
            view_specific_result()
            input("Pulsa enter para continuar")
        elif choice == '3':
            subprocess.run(['python', 'main.py'])
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
