from flask_restful import Resource,reqparse,request
from models.propriedadesModel import propriedadesModel
from models.produtorModel import produtorModel



class propriedades(Resource):
    @staticmethod
    def normalize_path_params(propriedade_id = None,
                              produtor_id = None,
                              cidade_Propriedade = None,
                              estado_Propriedade = None,
                              area_total_min = 0,
                              area_total_max = 10000000,
                              area_agriculturavel_min = 0,
                              area_agriculturavel_max = 10000000,  
                              limit = 50,
                              offset = 0, **dados):
        dados = {
            "propriedade_id" : propriedade_id,
            "produtor_id" : produtor_id,
            "cidade_Propriedade" : cidade_Propriedade,
            "estado_Propriedade" : estado_Propriedade,
            "area_total_min" : area_total_min,
            "area_total_max" : area_total_max,
            "area_agriculturavel_min" : area_agriculturavel_min,
            "area_agriculturavel_max" : area_agriculturavel_max,  
            "limit" : limit,
            "offset" : offset}
        return {chave:dados[chave] for chave in dados if dados[chave] is not None}
    
    @staticmethod
    def parser_params(path_params):
        path_params.add_argument('propriedade_id', type=int, required=False, location='args')
        path_params.add_argument('produtor_id', type=int, required=False, location='args')
        path_params.add_argument('cidade_Propriedade', type=str, required=False, location='args')
        path_params.add_argument('estado_Propriedade', type=str, required=False, location='args')
        path_params.add_argument('area_total_min', type=float, required=False, location='args')
        path_params.add_argument('area_total_max', type=float, required=False, location='args')
        path_params.add_argument('area_agriculturavel_min', type=float, required=False, location='args')
        path_params.add_argument('area_agriculturavel_max', type=float, required=False, location='args')
        path_params.add_argument('limit', type=int, required=False, location='args')
        path_params.add_argument('offset', type=int, required=False, location='args')
        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        return propriedades.normalize_path_params(**dados_validos)
    
    def get(self):
        try:
            argumentos = propriedades.parser_params(reqparse.RequestParser())
            print(argumentos)
            propriedadesFiltradas = propriedadesModel.filtra_propriedades(argumentos)
            return {"message": propriedadesFiltradas}, 200
        except Exception as e:
            print(f"Error retrieving propriedades: {str(e)}")
            return {"message": [propriedade.json() for propriedade in propriedadesModel.findPropriedades()]}, 200
        
    def put(self):
        parser_propriedade = reqparse.RequestParser()
        parser_propriedade.add_argument('produtor_id', type=int, required=True, help="Id do produtor é obrigatório")
        parser_propriedade.add_argument('nome_Propriedade', type=str, required=True, help="Nome da propriedade é obrigatório")
        parser_propriedade.add_argument('cidade_Propriedade', type=str, required=True, help="Cidade da propriedade é obrigatório")
        parser_propriedade.add_argument('estado_Propriedade', type=str, required=True, help="Estado da propriedade é obrigatório")
        parser_propriedade.add_argument('area_total_Propriedade', type=float, required=True, help="Area total da propriedade é obrigatório")
        parser_propriedade.add_argument('area_vegetacao_Propriedade', type=float, required=True, help="Area de vegetação da propriedade é obrigatório")
        parser_propriedade.add_argument('area_agriculturavel_Propriedade', type=float, required=True, help="Area agricultável da propriedade é obrigatório")
        dados = parser_propriedade.parse_args()
        propriedade = propriedadesModel.findPropriedade(dados["nome_Propriedade"])
        if not propriedade:
            return {"message": f'Propriedade {dados["nome_Propriedade"]} não existe'}, 400
        
        produtor = produtorModel.findProdutorByID(dados["produtor_id"])
        if not produtor:
            return {"message": f'Produtor {dados["produtor_id"]} não existe'}, 400
        
        try:
            print(dados)
            if dados["area_vegetacao_Propriedade"] + dados["area_agriculturavel_Propriedade"] > dados["area_total_Propriedade"]:
                return {"message": "A soma das áreas de vegetação e agricultável não pode ser menor que a área total"}, 400
            propriedade.updatePropriedade(dados)
            return {"message": propriedadesModel.findPropriedade(dados["nome_Propriedade"]).json()}, 201
        except Exception as e:
            return {"message": f"Error Saving Propriedade: {str(e)}"}, 500
        
    def post(self):
        parser_propriedade = reqparse.RequestParser()
        parser_propriedade.add_argument('produtor_id', type=int, required=True, help="Id do produtor é obrigatório")
        parser_propriedade.add_argument('nome_Propriedade', type=str, required=True, help="Nome da propriedade é obrigatório")
        parser_propriedade.add_argument('cidade_Propriedade', type=str, required=True, help="Cidade da propriedade é obrigatório")
        parser_propriedade.add_argument('estado_Propriedade', type=str, required=True, help="Estado da propriedade é obrigatório")
        parser_propriedade.add_argument('area_total_Propriedade', type=float, required=True, help="Area total da propriedade é obrigatório")
        parser_propriedade.add_argument('area_vegetacao_Propriedade', type=float, required=True, help="Area de vegetação da propriedade é obrigatório")
        parser_propriedade.add_argument('area_agriculturavel_Propriedade', type=float, required=True, help="Area agricultável da propriedade é obrigatório")
        dados = parser_propriedade.parse_args()
        propriedade = propriedadesModel.findPropriedade(dados["nome_Propriedade"])

        if propriedade:
            return {"message": f"Propriedade {dados['nome_Propriedade']} já existe"}, 400
        
        produtor = produtorModel.findProdutorByID(dados["produtor_id"])
        if not produtor:
            return {"message": f'Produtor {dados["produtor_id"]} não existe'}, 400
        
        try:
            if dados["area_vegetacao_Propriedade"] + dados["area_agriculturavel_Propriedade"] > dados["area_total_Propriedade"]:
                return {"message": "A soma das áreas de vegetação e agricultável não pode ser menor que a área total"}, 400
            propriedadeParsed = propriedadesModel(dados["produtor_id"], dados["nome_Propriedade"], dados["cidade_Propriedade"], dados["estado_Propriedade"], dados["area_total_Propriedade"], dados["area_vegetacao_Propriedade"], dados["area_agriculturavel_Propriedade"])
            propriedadeParsed.savePropriedade()
            return {"message": propriedadeParsed.json()}, 201
        except Exception as e:
            return {"message": f"Error Saving Propriedade: {str(e)}"}, 500 

    def delete(self):
        parser_propriedade = reqparse.RequestParser()
        parser_propriedade.add_argument('nome_Propriedade', type=str, required=True, help="Nome da propriedade é obrigatório")
        dados = parser_propriedade.parse_args()
        propriedade = propriedadesModel.findPropriedade(dados["nome_Propriedade"])
        if not propriedade:
            return {"message": f"Propriedade {dados['nome_Propriedade']} não existe"}, 400
        try:
            propriedade.deletePropriedade()
            return {"message": f"Propriedade Deletada"}, 204
        except Exception as e:
            return {"message": f"Error Deleting Propriedade: {str(e)}"}, 500