import requests
from enum import Enum
import os
from dotenv import load_dotenv 

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
FASTER_MODEL = "gemini-2.0-flash"
MODEL = "gemini-2.5-flash-preview-04-17"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{FASTER_MODEL}:generateContent?key={API_KEY}"


class RESPONSE_FORMAT(Enum):
    HTML = 1
    TEXT = 2

def get_personalized_prompt(industry, format):
    text_format_request = f"""Quiero que actúes como un trabajador de una empresa en la industria de {industry}. Estás enviando un brief de diseño a tu diseñador gráfico (que soy yo).

    Tu respuesta debe ser *únicamente* el brief de diseño, estructurado exactamente en las siguientes secciones:

    1.  Descripción de la compañía: Genera una descripción concisa de una empresa ficticia operando en la industria de {industry}. Incluye su nombre, el tipo de productos/servicios/enfoque específico dentro de esa industria (ej: si es moda, ¿es alta costura, streetwear, sostenible?; si es tecnología, ¿es B2B, software, hardware, IA?), y su visión o propuesta de valor principal. La descripción debe sonar auténtica para esa industria.
    2.  Descripción del trabajo a realizar: Detalla el proyecto de diseño específico que necesito realizar. Este trabajo debe ser relevante y típico para una empresa en la industria de {industry}. Sé muy claro y proporciona toda la información necesaria para que yo, como diseñador, entienda completamente el alcance. Esto puede incluir:
        * Tipo de activo de diseño requerido (ej: si es un restaurante, podría ser el diseño del menú o branding; si es tecnología, la UI/UX de una app o una presentación; si es moda, el diseño de un lookbook o la etiqueta de un producto; si es videojuegos, un logo o arte conceptual - *asegúrate de que el tipo de diseño sea apropiado para la industria elegida*).
        * Nombre del producto, servicio, evento o proyecto específico al que pertenece el diseño (inventa uno que suene bien dentro de esa industria).
        * Estilo visual y tono deseado (describe un estilo apropiado para la industria, la marca y el proyecto específico).
        * Objetivo principal del diseño (qué se espera lograr con este diseño en el contexto de esa industria y empresa).
        * Elementos o información específica que *deben* incluirse en el diseño.
        * Cualquier especificación técnica, de formato o medio relevante (ej: para impresión, digital, web, móvil, etc. - *relevante para el tipo de diseño y la industria*).
    3.  Deadline: Indica la fecha límite para la entrega del trabajo. Este deadline debe ser expresado *solamente* en un número de días a partir de hoy.

    Consideraciones importantes para tu respuesta:

    * Mantén un tono estrictamente formal, profesional y directo en todo momento, como si fueras un cliente enviando un brief.
    * No incluyas saludos iniciales ni finales, ni cualquier otra conversación que no sea el brief directamente.
    * Presenta la información de forma clara y concisa bajo los títulos de sección especificados.
    * Asegúrate de que *toda* la información necesaria para que yo pueda empezar el trabajo de diseño esté incluida en la respuesta. No hagas referencia a información que se enviará 'luego' o que está 'pendiente'. El brief debe ser completamente autocontenido.
    * Cada vez que generes una respuesta usando este prompt (variando la industria en {industry}), la 'Descripción de la compañía', la 'Descripción del trabajo a realizar' y el 'Deadline' deben ser diferentes y generar un escenario de brief de diseño único y coherente con la industria especificada.

    Comienza tu respuesta directamente con la sección 'Descripción de la compañía'.
    """

    if format == RESPONSE_FORMAT.HTML:
        html_format_request = """Quiero que tu respuesta la pongas en un html, lindo visualmente, todo lindo formateado, con buen css, estilos y animaciones smooth.
    No escribas nada antes ni después del codigo HTML.
    El diseño que le apliques tiene que tener cierta correlación con la industria pedida."""
    else:
        html_format_request = ""

    final_prompt = text_format_request + html_format_request
    return final_prompt

def clean_html(response_text):
    response_text = response_text.strip()

    if response_text.startswith("```html") and response_text.endswith("```"):
        response_text = response_text[len("```html"):-len("```")].strip()
    return response_text


def get_text_response(prompt):
    prompt_data = {
    "contents": [{
        "parts":[{"text": prompt}]
        }]
    }
    headers = {
        'Content-Type': 'application/json'
    }

    gemini_response = requests.post(url=API_URL,
                                    headers=headers,
                                    json=prompt_data)
    response_text = None
    if gemini_response.status_code == 200:
        gemini_response_data = gemini_response.json()
        response_text = gemini_response_data['candidates'][0]['content']['parts'][0]['text']
    return response_text


def generate_client_order_html(industry):
    prompt = get_personalized_prompt(industry=industry,
                                     format=RESPONSE_FORMAT.HTML)
    response_text = get_text_response(prompt)

    if response_text:
        response_text = clean_html(response_text)
        filename = "templates/brief_request.html"
        with open(filename, "w") as file:
            file.write(response_text)
    else:
        print(f"ERROR.\n")

def generate_client_order_text(industry):
    prompt = get_personalized_prompt(industry=industry,
                                     format=RESPONSE_FORMAT.TEXT)
    response_text = get_text_response(prompt)
    return response_text

""" def call_api(text):
    prompt_data = {
    "contents": [{
        "parts":[{"text": text}]
        }]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    gemini_response = requests.post(url=API_URL,
                                    headers=headers,
                                    json=prompt_data)

    if gemini_response.status_code == 200:
        gemini_response_data = gemini_response.json()
        response_text = gemini_response_data['candidates'][0]['content']['parts'][0]['text']
        print("\n\n-- RESPUESTA GEMINI --\n\n")
        print(response_text)


text = input("\n")
while text!='q':
    call_api(text)
    text = input("\n") """
