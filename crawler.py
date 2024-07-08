import subprocess
from bs4 import BeautifulSoup
from openai import OpenAI
import requests
import pymongo


# Configuración de OpenAI
api_key = "TU API AQUÍ"
api = OpenAI(api_key=api_key)

# Configuración de MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["web-analysis"]
collection = db["pages"]

def print_centered(text, width):
    return text.center(width)

def print_header():
    width = 80
    print("=" * width)
    print(print_centered("SELECCIONE UNA OPCIÓN", width))
    print("=" * width)

def print_menu():
    width = 80
    print("1 - Pulse 1 para indicar la página WEB que desea analizar".ljust(width))
    print("2 - Pulse 2 para volver al menú principal".ljust(width))
    print("=" * width)

def print_results(url, audience, content_type, summary):
    width = 80
    print(" ")
    print("=" * width)
    print(print_centered("RESULTADOS", width))
    print("=" * width)
    print(f"- La página WEB consultada es: {url}".ljust(width))
    print(" ")
    print(f"- El contenido es para: {audience}".ljust(width))
    print(" ")
    print(f"- El contenido se asocia a: {content_type}".ljust(width))
    print(" ")
    print(f"- Breve resumen de la WEB indicada: {summary}".ljust(width))
    print("=" * width)

def analyze_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanzar un error si el status code no es 200
    except requests.RequestException:
        width = 80
        print("=" * width)
        print(print_centered("No se ha podido acceder a la WEB indicada", width))
        print("=" * width)
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    text_content = ' '.join(soup.stripped_strings)
    
    analysis_response = api.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "Debes responder en español y no enumerar tus respuestas"},
            {"role": "user", "content": f"Analiza el contenido de la siguiente página WEB:\n{text_content}\n\nResponder solo si el contenido es para 'TODOS LOS PÚBLICOS' o solo para 'ADULTOS'\nIndicar solo el tipo de contenido 'deportes, tecnología, sexo, drogas, etc'?\nRealiza un breve contenido de la página WEB de no más de 30"}
        ],
        max_tokens=150
    )

    analysis_lines = analysis_response.choices[0].message.content.strip().split('\n')

    # Validar y asignar los valores de la respuesta
    audience = "No disponible"
    content_type = "No disponible"
    summary = "No disponible"
    
    if len(analysis_lines) > 0:
        audience = analysis_lines[0].split(': ')[-1] if ': ' in analysis_lines[0] else analysis_lines[0]
    if len(analysis_lines) > 1:
        content_type = analysis_lines[1].split(': ')[-1] if ': ' in analysis_lines[1] else analysis_lines[1]
    if len(analysis_lines) > 2:
        summary = analysis_lines[2].split(': ')[-1] if ': ' in analysis_lines[2] else analysis_lines[2]
    
    print_results(url, audience, content_type, summary)
    
    # Guardar en MongoDB
    page_data = {
        "url": url,
        "audience": audience,
        "content_type": content_type,
        "summary": summary
    }
    collection.insert_one(page_data)

def main():
    while True:
        print_header()
        print_menu()
        choice = input("\nIndique la opción que desee usar: ")
        
        if choice == '1':
            url = input("Introduzca la dirección de la página WEB que desea analizar: ")
            analyze_page(url)
            input("Pulse enter para continuar")
        elif choice == '2':
            subprocess.run(['python', 'main.py'])
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
