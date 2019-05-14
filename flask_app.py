import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
import pdf_reader
import json
from werkzeug.datastructures import FileStorage
from flask import jsonify
from flask import Response

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        path = request.form['path']
        if path == '':
            flash('No path')
            return redirect(request.url)
        else:
            if '.pdf' in path:
                df = pdf_reader.getHistorico(path)
                dfJson = json.dumps(json.loads(df.to_json(orient='records')), indent=2, ensure_ascii=False).encode('utf8')
                return dfJson
    return ''

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= '5000', debug=True)