from flask import Flask, request, render_template
from gemini_api import generate_client_order_html, generate_client_order_text
import markdown

# --- Configuración de Flask ---
app = Flask(__name__)

# --- Ruta para la página inicial con el formulario ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Ruta para manejar la petición POST del formulario ---
@app.route('/generate_brief', methods=['POST'])
def generate_brief():
    industry = request.form.get('industry')
    design_type = request.form.get('design_type')
    if not industry:
        return "Error: Por favor, especifica una industria.", 400


    try:
        if design_type == "personalized":
            generate_client_order_html(industry)
            return render_template("brief_request.html")
        else:
            response_text = generate_client_order_text(industry)
            company_title = 'Descripción de la compañía:'
            job_title = 'Descripción del trabajo a realizar:'
            deadline_title = 'Deadline:'

            company_content = ""
            job_content = ""
            deadline_content = ""

            # Ver luego gestión de errores
            parts = response_text.split(company_title)
            remaining_text = parts[1].strip()
            parts = remaining_text.split(job_title)
            company_content = parts[0].strip()
            remaining_text = parts[1].strip()
            parts = remaining_text.split(deadline_title)
            job_content = parts[0].strip()
            deadline_content = parts[1].strip()

            company_content_html = markdown.markdown(company_content)
            job_content_html = markdown.markdown(job_content)
            deadline_content_html = markdown.markdown(deadline_content)

            return render_template(
                'brief_standard.html',
                company_content=company_content_html,
                job_content=job_content_html,
                deadline_content=deadline_content_html
            )
    except:
        return "Error al contactar con la IA", 400

if __name__ == '__main__':
    app.run(debug=True)

