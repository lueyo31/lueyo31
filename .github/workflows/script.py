import requests
from bs4 import BeautifulSoup
import time
import os
from PIL import Image
import io

def update_quote():
    # Obtener la página web
    response = requests.get('https://proverbia.net/frase-del-dia')

    # Parsear la página web
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar la frase del día
    quote = soup.find('blockquote').text.strip()

    # Dividir la cita en sus componentes
    h4, rest = quote.split('\n', 1)
    author, kursiva = rest.split('(', 1)
    author = author.strip()
    kursiva = '(' + kursiva.split('.\n')[0] + '.'

    # Leer el archivo README.md
    with open('README.md', 'r') as file:
        lines = file.readlines()

    # Borrar la frase del día anterior
    start_marker = '<!-- START QUOTE -->\n'
    end_marker = '<!-- END QUOTE -->\n'
    if start_marker in lines and end_marker in lines:
        start_index = lines.index(start_marker) + 1
        end_index = lines.index(end_marker)
        del lines[start_index:end_index]

    # Insertar la nueva frase con los marcadores y el formato deseado
    lines.insert(start_index, f'#### {h4}\n')
    lines.insert(start_index + 1, f'**{author}** *{kursiva}*\n')

    # Escribir el contenido actualizado en el archivo README.md
    with open('README.md', 'w') as file:
        file.writelines(lines)

def update_weather():
    # Obtener la página web
    response = requests.get('https://www.tiempo.com/valencia.htm')

    # Parsear la página web
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar el elemento del estado del tiempo
    weather_element = soup.find('span', class_='descripcion')
    temperature_element = soup.find('span', class_='dato-temperatura changeUnitT')

    # Comprobar si se encontraron los elementos de la temperatura y el estado del tiempo
    if temperature_element is None:
        temperature = 'Desconocido'
    else:
        temperature = temperature_element.text

    if weather_element is None:
        weather = 'Desconocido'
    else:
        weather = weather_element.text.strip()  # Asegurarse de que no haya espacios en blanco alrededor de la descripción

    # Mapear el estado del tiempo a un emoji
    weather_emoji_map = {
        'Despejado': '☀️',
        'Intervalos nubosos': '🌤️',
        'Cielos Nubosos': '🌥️',
        'Cielos Cubiertos': '☁️',
        'Lluvia ligera': '🌦️',
        'Lluvia moderada': '🌧️',
        'Tormentas': '⛈️',
        'Nieve': '🌨️',
        'Niebla': '🌫️'
    }
    weather_emoji = weather_emoji_map[weather]  # Esto lanzará una excepción si la descripción no está en el diccionario

    # Crear la línea del clima
    weather_line = f'### Valencia: {temperature} {weather_emoji}\n'

    # Leer el archivo README.md
    with open('README.md', 'r') as file:
        lines = file.readlines()

    # Eliminar la línea del clima anterior, si existe
    lines = [line for line in lines if 'Valencia:' not in line]

    # Insertar la nueva línea del clima en la línea 2
    lines.insert(2, weather_line)

    # Escribir el contenido actualizado en el archivo README.md
    with open('README.md', 'w') as file:
        file.writelines(lines)



def update_images():
    # Crear la carpeta src si no existe
    if not os.path.exists('src'):
        os.makedirs('src')

    # Leer el archivo README.md
    with open('README.md', 'r') as file:
        lines = file.readlines()

    # Encontrar la línea que contiene "Esta persona no existe"
    index = next((i for i, line in enumerate(lines) if 'Esta persona no existe' in line.lower()), -1)

    for i in range(6):
    # Descargar la imagen
        time.sleep(0.8)
        image_url = 'https://thispersondoesnotexist.com/'
        image_path = f'src/image_{i}.png'
        response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'})

    # Abrir la imagen desde la respuesta y redimensionarla
        img = Image.open(io.BytesIO(response.content))
        img = img.resize((200, 200))

    # Guardar la imagen redimensionada
        img.save(image_path)

        

# Llamar a las funciones

update_quote()
update_images()
update_weather()
