from flask_restful import Resource,reqparse,request
from models.produtorModel import produtorModel
from models.produtosModel import produtosModel
from models.propriedadesModel import propriedadesModel
from models.safrasModel import safrasModel


class safras(Resource):
    @staticmethod
    def normalize_path_params(safra_id = None,
                              propriedade_id = None,
                              produtor_id = None,
                              safra_produto_id = None,
                              safra_ano_min = 0,
                              safra_ano_max = 3000,
                              safra_area_min = 0,
                              safra_area_max = 10000000,  
                              safra_producao_min = 0,
                              safra_producao_max = 10000000,
                              safra_rendimento_min = 0,
                              safra_rendimento_max = 10000000,
                              limit = 50,
                              offset = 0, **dados):
        dados = {
            "safra_id" : safra_id,
            "propriedade_id" : propriedade_id,
            "produtor_id" : produtor_id,
            "safra_produto_id" : safra_produto_id,
            "safra_ano_min" : safra_ano_min,
            "safra_ano_max" : safra_ano_max,
            "safra_area_min" : safra_area_min,
            "safra_area_max" : safra_area_max,  
            "safra_producao_min" : safra_producao_min,
            "safra_producao_max" : safra_producao_max,
            "safra_rendimento_min" : safra_rendimento_min,  
            "safra_rendimento_max" : safra_rendimento_max,  
            "limit" : limit,
            "offset" : offset}
        return {chave:dados[chave] for chave in dados if dados[chave] is not None}
    
    @staticmethod
    def parser_params(path_params):
        path_params.add_argument('safra_id', type=int, required=False, location='args')
        path_params.add_argument('propriedade_id', type=int, required=False, location='args')
        path_params.add_argument('produtor_id', type=int, required=False, location='args')
        path_params.add_argument('safra_ano_min', type=int, required=False, location='args')
        path_params.add_argument('safra_ano_max', type=int, required=False, location='args')
        path_params.add_argument('safra_area_min', type=float, required=False, location='args')
        path_params.add_argument('safra_area_max', type=float, required=False, location='args')
        path_params.add_argument('safra_producao_min', type=float, required=False, location='args')
        path_params.add_argument('safra_producao_max', type=float, required=False, location='args')
        path_params.add_argument('safra_rendimento_min', type=float, required=False, location='args')
        path_params.add_argument('safra_rendimento_max', type=float, required=False, location='args')
        path_params.add_argument('limit', type=int, required=False, location='args')
        path_params.add_argument('offset', type=int, required=False, location='args')
        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        return safras.normalize_path_params(**dados_validos)
    
    def get(self):
        try:
            argumentos = safras.parser_params(reqparse.RequestParser())
            print(argumentos)
            safrasFiltradas = safrasModel.filtraSafras(argumentos)
            return {"message": safrasFiltradas}, 200
        except:
            return {"message": [safra.json() for safra in safrasModel.findSafras()]}, 200
        
    def put(self):
        parser_safra = reqparse.RequestParser()
        parser_safra.add_argument('safra_id', type=int, required=True, help="Id da Safra é obrigatório")
        parser_safra.add_argument('propriedade_id', type=int, required=True, help="Id da propriedade é obrigatório")
        parser_safra.add_argument('produtor_id', type=int, required=True, help="Id do produtor é obrigatório")
        parser_safra.add_argument('safra_produto_id', type=int, required=True, help="Id do produto é obrigatório")
        parser_safra.add_argument('safra_ano', type=int, required=True, help="Ano da safra é obrigatório")
        parser_safra.add_argument('safra_area', type=float, required=True, help="Area total da safra é obrigatório")
        parser_safra.add_argument('safra_producao', type=float, required=True, help="Produção da safra é obrigatório")
        parser_safra.add_argument('safra_rendimento', type=float, required=True, help="Rendimento da safra é obrigatório")
        dados = parser_safra.parse_args()
        propriedade = propriedadesModel.findPropriedadeByID(dados["propriedade_id"])
        if not propriedade:
            return {"message": f'Propriedade {dados["propriedade_id"]} não existe'}, 400
        
        produtor = produtorModel.findProdutorByID(dados["produtor_id"])
        if not produtor:
            return {"message": f'Produtor {dados["produtor_id"]} não existe'}, 400
        
        produto = produtosModel.findProdutoByID(dados["safra_produto_id"])
        if not produto:
            return {"message": f'Produto {dados["safra_produto_id"]} não existe'}, 400
        
        safra = safrasModel.findSafra(dados["safra_id"])
        if not safra:
            return {"message": f'Safra {dados["safra_id"]} não existe'}, 400

        try:
            safra.updateSafra(dados)
            return {"message": safrasModel.findSafra(dados["safra_id"]).json()}, 201
        except Exception as e:
            return {"message": f"Error Saving Safra: {str(e)}"}, 500
        
    def post(self):
        parser_safra = reqparse.RequestParser()
        parser_safra.add_argument('propriedade_id', type=int, required=True, help="Id da propriedade é obrigatório")
        parser_safra.add_argument('produtor_id', type=int, required=True, help="Id do produtor é obrigatório")
        parser_safra.add_argument('safra_produto_id', type=int, required=True, help="Id do produto é obrigatório")
        parser_safra.add_argument('safra_ano', type=int, required=True, help="Ano da safra é obrigatório")
        parser_safra.add_argument('safra_area', type=float, required=True, help="Area total da safra é obrigatório")
        parser_safra.add_argument('safra_producao', type=float, required=True, help="Produção da safra é obrigatório")
        parser_safra.add_argument('safra_rendimento', type=float, required=True, help="Rendimento da safra é obrigatório")
        dados = parser_safra.parse_args()
        argumentos = safras.parser_params(reqparse.RequestParser())
        print(argumentos)
        safrasFiltradas = safrasModel.filtraSafras(argumentos)
        if safrasFiltradas:
            return {"message": f'Safra {safrasFiltradas} já existe'}, 400
       
        propriedade = propriedadesModel.findPropriedadeByID(dados["propriedade_id"])
        if not propriedade:
            return {"message": f'Propriedade {dados["propriedade_id"]} não existe'}, 400
        
        produtor = produtorModel.findProdutorByID(dados["produtor_id"])
        if not produtor:
            return {"message": f'Produtor {dados["produtor_id"]} não existe'}, 400
        
        produto = produtosModel.findProdutoByID(dados["safra_produto_id"])
        if not produto:
            return {"message": f'Produto {dados["safra_produto_id"]} não existe'}, 400

        try:
            safraParsed = safrasModel(dados["propriedade_id"], dados["produtor_id"], dados["safra_produto_id"], dados["safra_ano"], dados["safra_area"], dados["safra_producao"], dados["safra_rendimento"])
            safraParsed.saveSafra()
            return {"message": safraParsed.json()}, 201
        except Exception as e:
            return {"message": f"Error Saving Propriedade: {str(e)}"}, 500 

    def delete(self):
        parser_safra = reqparse.RequestParser()
        parser_safra.add_argument('safra_id', type=str, required=True, help="Id da safra é obrigatório")
        dados = parser_safra.parse_args()
        safra = safrasModel.findSafra(dados["safra_id"])
        if not safra:
            return {"message": f"Safra {dados['safra_id']} não existe"}, 400
        try:
            safra.deleteSafra()
            return {"message": f"Safra Deletada"}, 204
        except Exception as e:
            return {"message": f"Error Deleting Safra: {str(e)}"}, 500