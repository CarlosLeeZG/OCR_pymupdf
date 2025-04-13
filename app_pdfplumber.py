# import pdfplumber
# import pandas as pd
# import os

# # Initialize an empty dictionary to store DataFrames
# dfs = {}

# def open_pdf(directorty = ".", subfolder = "tables_outputs"):
#   list_pdf = [f for f in os.listdir(os.path.join(directory, 'pdf_files')) if f.endswith(".pdf")]
#   if not os.path.exists(subfolder):
#     os.makedirs(subfolder)
  
#   for file in list_pdf:
#     with pdfplumber.open(file_name) as pdf:
#       for page_number, page in enumerate(pdf.pages, start = 1):
#         print(page_number)
#         tables = page.extract_tables()
#         for table_index, table in enumerate(tables):
#           df = pd.DataFrame(table)
#           df.columns = df.iloc[0]
#           df = df[1:]
#           df.to_excel(f"{file}_{table_index}_{page_number}.xlsx", index = False)

          
          
          
          
  # app.py
from flask import Flask, request, render_template, send_file, session
import pdfplumber
from PIL import Image
import pytesseract
import pandas as pd
import io
import os
from flask import Flask, request, render_template, render_template_string

app = Flask(__name__)
app.secret_key = 'secret'  # Needed for session

# Temporary store for tables
table_store = []

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/upload', methods=['POST'])
def upload():
    global table_store
    file = request.files['file']
    table_store = []  # Clear previous

    if file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    table_store.append(table)
    else:
        image = Image.open(file.stream)
        text = pytesseract.image_to_string(image)
        table_store.append([[text]])

    return render_template('tables.html', tables=table_store)

@app.route('/download')
def download_excel():
    global table_store

    if not table_store:
        return "No table data available", 400

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for idx, table in enumerate(table_store):
            df = pd.DataFrame(table)
            df.to_excel(writer, sheet_name=f'Table_{idx+1}', index=False)
    output.seek(0)

    return send_file(output,
                     download_name="extracted_tables.xlsx",
                     as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(debug=True)
