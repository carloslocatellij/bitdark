from flask import Flask, jsonify, json 
from os.path import join
from Tabuleiro import Tabuleiro as Tab

app = Flask(__name__)


tab = Tab('m')

@app.route('/', methods=['GET'])
def home():
    
    t = tab
    
    return f'<table>{t}</table>' 

if __name__ == '__main__':
    app.run( debug=True)
