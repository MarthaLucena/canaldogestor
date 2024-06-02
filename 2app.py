from flask import Flask, request, redirect, url_for, render_template, send_file
import os
import pandas as pd

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')


# Diretório de upload e compilação
UPLOAD_FOLDER = 'uploads'
COMPILED_FOLDER = 'compiled'

# Configurações do Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPILED_FOLDER'] = COMPILED_FOLDER

# Criação dos diretórios, se não existirem
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPILED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files[]')
    dataframes = []

    for file in uploaded_files:
        if file.filename.endswith('.csv'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            df = pd.read_csv(file_path)
            dataframes.append(df)

    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        compiled_csv_path = os.path.join(app.config['COMPILED_FOLDER'], 'combined.csv')
        compiled_xlsx_path = os.path.join(app.config['COMPILED_FOLDER'], 'combined.xlsx')
        
        # Salvar como CSV
        combined_df.to_csv(compiled_csv_path, index=False)
        
        # Salvar como Excel
        with pd.ExcelWriter(compiled_xlsx_path, engine='xlsxwriter') as writer:
            combined_df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        # Opções de download
        download_option = request.form.get('download_option')
        if download_option == 'csv':
            return send_file(compiled_csv_path, as_attachment=True, download_name='combined.csv')
        elif download_option == 'excel':
            return send_file(compiled_xlsx_path, as_attachment=True, download_name='combined.xlsx')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
