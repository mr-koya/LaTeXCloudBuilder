from flask import Flask, request, jsonify, send_file
import os
import subprocess
import tempfile
import shutil

app = Flask(__name__)

@app.route('/compile', methods=['POST'])
def compile_tex():
    data = request.get_json()
    tex_content = data.get('tex')
    bib_content = data.get('bib')

    if not tex_content:
        return jsonify({"error": "TeX content missing"}), 400

    # Create a temporary directory to work in
    temp_dir = tempfile.mkdtemp()
    try:
        # Write the TeX and Bib files to the temp directory
        tex_path = os.path.join(temp_dir, 'document.tex')
        with open(tex_path, 'w') as tex_file:
            tex_file.write(tex_content)

        if bib_content:
            bib_path = os.path.join(temp_dir, 'references.bib')
            with open(bib_path, 'w') as bib_file:
                bib_file.write(bib_content)

        # Run LaTeX to compile the document
        subprocess.run(['pdflatex', 'document.tex'], cwd=temp_dir, check=True)
        if bib_content:
            subprocess.run(['bibtex', 'document.aux'], cwd=temp_dir, check=True)
            subprocess.run(['pdflatex', 'document.tex'], cwd=temp_dir, check=True)
            subprocess.run(['pdflatex', 'document.tex'], cwd=temp_dir, check=True)

        # Read the generated PDF
        pdf_path = os.path.join(temp_dir, 'document.pdf')
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        return jsonify({"pdf": pdf_data.decode('latin1')}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "LaTeX compilation failed", "details": str(e)}), 500

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

