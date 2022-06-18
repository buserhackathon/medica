import json
from flask import Flask, render_template
import map_support
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           ufs=map_support.getUFs(),
                           municipios=map_support.getMunicipios('AC'))


@app.route('/callback/<endpoint>')
def callbacks(endpoint):
    args = request.args
    if endpoint == 'getMap':
        return json.dumps({'Map': map_support.getFigUBSs(args.get('uf'),
                                                         args.get('municipio_id'))})

if __name__ == '__main__':
        app.run(debug=True)
