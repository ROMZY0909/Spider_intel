from weasyprint import HTML
import os
from jinja2 import Template

def generate_pdf(report_data: dict, output_path: str = "rapport.pdf"):
    html_template = """
    <html>
    <head>
        <style>
            body { font-family: sans-serif; margin: 40px; }
            h1 { color: #222; }
            .block { margin-bottom: 20px; }
            .section-title { font-weight: bold; font-size: 18px; margin-top: 15px; }
            ul { padding-left: 20px; }
        </style>
    </head>
    <body>
        <h1>🕷️ Rapport SPIDER INTEL</h1>
        <div class="block"><strong>Email analysé :</strong> {{ email }}</div>
        <div class="block"><strong>Valide :</strong> {{ valid }}</div>
        <div class="block"><strong>Sensibilité :</strong> {{ sensitive }}</div>
        <div class="block"><strong>Résumé :</strong><br>{{ summary }}</div>

        {% for source in sources %}
            <div class="section-title">{{ source.source }}</div>
            <ul>
            {% for item in source.data %}
                <li>{{ item }}</li>
            {% endfor %}
            </ul>
        {% endfor %}
    </body>
    </html>
    """

    # Rendu HTML avec les données
    template = Template(html_template)
    rendered_html = template.render(**report_data)

    # Générer le PDF
    HTML(string=rendered_html).write_pdf(output_path)

    return output_path
