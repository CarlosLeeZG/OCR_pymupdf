import pymupdf
import fitz
import pandas as pd
import os

def open_pdf(directorty = ".", subfolder = "tables_outputs"):
  list_pdf = [f for f in os.listdir(os.path.join(directory, 'pdf_files')) if f.endswith(".pdf")]
  if not os.path.exists(subfolder):
    os.makedirs(subfolder)
    
  for file in list_pdf:
    fitz.open(file)
    pagenum=0
    targetlist = []
    pagelist =[]
    
    for page in doc:
      tabs = page.find_tables()
      if tabs.tables:
        print(tabs[0].extract())
        pagenum +=1
        l=len(tabs.tables)
        
        for i in range(l):
          if tabs[i].extract()[0]: 
              #print(pagenum)
              #print(tabs[i].extract()[0])
              for item in tabs[i].extract()[0]:
                  #if item != None and len(re.findall('(sqm|Emissions Intensity|CO)',item))>0:
                  if item != None:
                      #print(tabs[i].extract())
                      targetlist.append(tabs[i].extract())
                      pagelist.append(tabs[i].extract())
pagelist
targetlist

tab_1 = pd.DataFrame(targetlist[-11])

tab_1.columns = tab_1.iloc[0]
tab_1 = tab_1[1:]
tab_1

tab_1.to_csv("bottom 2 table for CHina.csv", index = False)
