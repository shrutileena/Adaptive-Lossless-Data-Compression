from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Files'
CORS(app)

if __name__ == "__main__":
    from api import *
    app.run(debug=True,use_reloader=True)