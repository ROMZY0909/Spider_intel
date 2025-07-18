# utils/generator.py

from weasyprint import HTML
from jinja2 import Template
import os

def generate_pdf(report_data: dict, output_path: str = "rapport.pdf"):
    html_template = """
    <html>
    <head>
        <meta charset="UTF-8">
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

        {% for key, value in report_data.items() %}
            <div class="block">
                <span class="section-title">{{ key | capitalize }} :</span><br>
                {% if value is iterable and value is not string %}
                    <ul>
                        {% for item in value %}
                            <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                {% else %}
                    {{ value }}
                {% endif %}
            </div>
        {% endfor %}

    </body>
    </html>
    """

    # Rendu HTML avec Jinja2
    template = Template(html_template)
    rendered_html = template.render(report_data=report_data)

    # Génération du PDF avec WeasyPrint
    HTML(string=rendered_html).write_pdf(output_path)

    print(f"✅ PDF généré avec succès : {output_path}")
