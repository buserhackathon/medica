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
        # TODO: remover parâmetro uf da função abaixo
        return json.dumps({'Map': map_support.getFigUBSs(args.get('uf'),
                                                         args.get('municipio_id')),
                           'municipios': json.dumps(map_support.getMunicipios(args.get('uf')))})

if __name__ == '__main__':
        app.run(debug=True)
