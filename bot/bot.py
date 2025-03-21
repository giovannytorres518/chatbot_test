import os
import json
from datetime import datetime
import logging

# Configuración del logging para que se muestre información detallada.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def procesar_respuesta(input):
    logging.debug(f"Iniciando procesamiento de respuesta para input: {input}")
    # Aquí va todo el proceso de WS & LLM processing
    resultado = input + ' test'
    logging.debug(f"Resultado del procesamiento: {resultado}")
    return resultado

def procesar_jsons():
    input_dir = 'data/input_jsons'
    output_dir = 'data/output_jsons'
    logging.info("Iniciando el procesamiento de archivos JSON.")
    logging.debug(f"Directorio de entrada: {input_dir}")
    logging.debug(f"Directorio de salida: {output_dir}")

    # Asegurarnos de que la carpeta de salida exista
    os.makedirs(output_dir, exist_ok=True)
    logging.info("Directorio de salida verificado/creado.")

    # Iterar sobre todos los archivos .json en la carpeta de entrada
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            input_path = os.path.join(input_dir, file_name)
            logging.info(f"Procesando archivo: {input_path}")

            try:
                # Leer el contenido del archivo JSON
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)  # Se asume que 'data' es una lista de diccionarios
                logging.debug(f"Archivo {file_name} cargado correctamente. Registros encontrados: {len(data)}")
            except Exception as e:
                logging.error(f"Error al leer el archivo {input_path}: {e}")
                continue

            output_data = []
            for index, item in enumerate(data):
                logging.debug(f"Procesando registro {index + 1}/{len(data)}: {item}")

                # Extraer campos originales
                destinatario = item.get('destinatario', '')
                asunto = item.get('asunto', '')
                fecha = item.get('fecha', '')
                cuerpo = item.get('cuerpo', '')
                logging.debug(f"Datos extraídos - Destinatario: {destinatario}, Asunto: {asunto}, Fecha: {fecha}, Cuerpo: {cuerpo}")

                # Construir campos de salida
                fecha_output = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                asunto_output = f"{asunto} (respuesta)"
                logging.debug(f"Generando respuesta para el registro {index + 1}")
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
                logging.debug(f"Nuevo registro generado: {nuevo_registro}")

                output_data.append(nuevo_registro)

            # Guardar el nuevo archivo JSON en la carpeta de salida
            output_file_name = f"output_{file_name}"
            output_path = os.path.join(output_dir, output_file_name)
            try:
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    json.dump(output_data, out_f, ensure_ascii=False, indent=4)
                logging.info(f"Archivo procesado guardado correctamente: {output_path}")
            except Exception as e:
                logging.error(f"Error al guardar el archivo {output_path}: {e}")

    logging.info("Todos los archivos han sido procesados y guardados en la carpeta 'data/output_jsons'.")

if __name__ == '__main__':
    logging.info("Inicio de la ejecución del script bot.py")
    procesar_jsons()
    logging.info("Fin de la ejecución del script bot.py")
