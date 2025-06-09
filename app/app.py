from flask import Flask
from flask_restful import Api
from resources.produtor import produtor
from resources.produtos import produtos
from resources.propriedades import propriedades
from resources.safras import safras
from apitally.flask import ApitallyMiddleware
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
# Configure logging
app.wsgi_app = ApitallyMiddleware(
    app,
    client_id="7f89226f-b492-4b40-a568-b82e9c555942",
    env="dev",  # or "dev"
)


with app.app_context():
    from models import banco
    from models.produtorModel import produtorModel
    from models.produtosModel import produtosModel
    from models.propriedadesModel import propriedadesModel
    from models.safrasModel import safrasModel
    banco.init_app(app)
    banco.create_all()

api.add_resource(produtor, '/produtores')
api.add_resource(produtos, '/produtos')
api.add_resource(propriedades, '/propriedades')
api.add_resource(safras, '/safras')




if __name__ == '__main__':
    app.run(host="0.0.0.0")