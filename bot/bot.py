import os
import json
from datetime import datetime

def procesar_respuesta(input):
    # Aquí va todo el proceso de WS & LLM processing
    return input+' test'

def procesar_jsons():
    input_dir = 'data/input_jsons'
    output_dir = 'data/output_jsons'

    # Asegurarnos de que la carpeta de salida exista
    os.makedirs(output_dir, exist_ok=True)

    # Iterar sobre todos los archivos .json en la carpeta de entrada
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            input_path = os.path.join(input_dir, file_name)

            # Leer el contenido del archivo JSON
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Se asume que 'data' es una lista de diccionarios

            output_data = []
            for item in data:
                # Extraer campos originales
                destinatario = item.get('destinatario', '')
                asunto = item.get('asunto', '')
                fecha = item.get('fecha', '')
                cuerpo = item.get('cuerpo', '')

                # Construir campos de salida
                fecha_output = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                asunto_output = f"{asunto} (respuesta)"
                cuerpo_output = procesar_respuesta(cuerpo)

                # Crear el nuevo registro
                nuevo_registro = {
                    "destinatario": destinatario,
                    "asunto": asunto,
                    "fecha": fecha,
                    "cuerpo": cuerpo,
                    "fecha_output": fecha_output,
                    "asunto_output": asunto_output,
                    "cuerpo_output": cuerpo_output
                }

                output_data.append(nuevo_registro)

            # Guardar el nuevo archivo JSON en la carpeta de salida
            output_file_name = f"output_{file_name}"
            output_path = os.path.join(output_dir, output_file_name)

            with open(output_path, 'w', encoding='utf-8') as out_f:
                json.dump(output_data, out_f, ensure_ascii=False, indent=4)

    print("Archivos procesados y guardados en la carpeta 'data/output_jsons'.")

if __name__ == '__main__':
    procesar_jsons()
