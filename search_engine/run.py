from nar_supervised import create_NAR_model, recommend
from searchengine import app

if __name__ == "__main__":
    model = create_NAR_model()
    app.config['MODEL'] = model
    app.config['REC_FUNCTION'] = recommend
    app.run(debug=True)