import requests
import base64
import json
import sys
import os

def compile_tex(tex_content, bib_content):
    url = "http://127.0.0.1:8080/compile"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "tex": tex_content,
        "bib": bib_content
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_data = response.json()
        pdf_base64 = response_data.get("pdf")
        if pdf_base64:
            pdf_data = pdf_base64.encode('latin1')
            with open("output.pdf", "wb") as pdf_file:
                pdf_file.write(pdf_data)
            print("PDF successfully generated and saved as output.pdf")
        else:
            print("No PDF data found in the response")
    else:
        print(f"Failed to compile. Status code: {response.status_code}")
        print(response.json())

def read_file_content(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compile_tex.py <tex_file> <bib_file>")
        sys.exit(1)
    
    tex_file = sys.argv[1]
    bib_file = sys.argv[2]
    
    tex_content = read_file_content(tex_file)
    bib_content = read_file_content(bib_file)
    
    compile_tex(tex_content, bib_content)
