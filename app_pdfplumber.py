import pdfplumber
import pandas as pd
import os

# Initialize an empty dictionary to store DataFrames
dfs = {}

def open_pdf(directorty = ".", subfolder = "tables_outputs"):
  list_pdf = [f for f in os.listdir(os.path.join(directory, 'pdf_files')) if f.endswith(".pdf")]
  if not os.path.exists(subfolder):
    os.makedirs(subfolder)
  
  for file in list_pdf:
    with pdfplumber.open(file_name) as pdf:
      for page_number, page in enumerate(pdf.pages, start = 1):
        print(page_number)
        tables = page.extract_tables()
        for table_index, table in enumerate(tables):
          df = pd.DataFrame(table)
          df.columns = df.iloc[0]
          df = df[1:]
          df.to_excel(f"{file}_{table_index}_{page_number}.xlsx", index = False)
          
          
          
          
          
      
