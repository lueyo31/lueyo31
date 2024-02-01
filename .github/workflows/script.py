import requests
from bs4 import BeautifulSoup
import time
import os
import wget

def update_quote():
    # Obtener la página web
    response = requests.get('https://proverbia.net/frase-del-dia')

    # Parsear la página web
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar la frase del día
    quote = soup.find('blockquote').text.strip()

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

    # Insertar la nueva frase con los marcadores
    lines.insert(start_index, quote + '\n')

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
        'Nubes dispersas': '🌤️',
        'Nublado': '🌥️',
        'Lluvia ligera': '🌦️',
        'Lluvia': '🌧️',
        'Tormenta': '⛈️',
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
    # Crear la carpeta images si no existe
    if not os.path.exists('images'):
        os.makedirs('images')

    # Leer el archivo README.md
    with open('README.md', 'r') as file:
        lines = file.readlines()

    # Encontrar la línea que contiene "Esta persona no existe"
    index = next((i for i, line in enumerate(lines) if 'Esta persona no existe' in line.lower()), -1)

    for i in range(6):
        # Descargar la imagen
        image_url = 'https://thispersondoesnotexist.com/image'
        image_path = f'images/image_{i}.png'
        wget.download(image_url, image_path)

        # Crear el código Markdown para la imagen con el tamaño deseado
        image_line = f'<img src="{image_path}" width="200" height="200">\n'

        if index != -1:
            # Si se encontró la línea, insertar la línea de la imagen después de ella
            lines.insert(index + 1, image_line)
            index += 1  # Incrementar el índice para la próxima inserción
        else:
            # Si no se encontró la línea, agregar la línea de la imagen al final
            lines.append(image_line)

    # Escribir el contenido actualizado en el archivo README.md
    with open('README.md', 'w') as file:
        file.writelines(lines)

# Llamar a las funciones
update_quote()
update_weather()
update_images()