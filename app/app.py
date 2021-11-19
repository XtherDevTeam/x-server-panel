import flask

app = flask.app.Flask(__name__,
    static_url_path='/static/',
    static_folder='static',
    template_folder='template'
)

@app.route('/',methods = ['GET'])
def indexOfRoot():
    return flask.render_template('index.html')

app.run('0.0.0.0',11453,None)