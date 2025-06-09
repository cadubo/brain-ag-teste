from flask_restful import Resource,reqparse,request
from models.produtorModel import produtorModel



class produtor(Resource):

    def get(self):
        try:
            parser_produtor = reqparse.RequestParser()
            parser_produtor.add_argument('cpf_cnpj14', type=str)
            parser_produtor.add_argument('tipo_Produtor', type=str)
            dados = parser_produtor.parse_args()
            print(dados)
            validador = produtorModel.validaCpfCnpj(dados["cpf_cnpj14"], dados["tipo_Produtor"])
            if validador == False:
                return {"message": "CPF ou CNPJ inválido"}, 400
        
            Produtor = produtorModel.findProdutor(dados["cpf_cnpj14"])
            if Produtor:
                return {"message": Produtor.json()}, 200
            return {"message": "Produtores Não Encontrado"}, 400

        except:
            try:
                Produtores = produtorModel.findProdutores()
                return {"message": [produtor.json() for produtor in Produtores]}, 200
            except:
                return {"message": "Nenhum Produtor Encontrado"}, 400
        
    def put(self):
        parser_produtor = reqparse.RequestParser()
        parser_produtor.add_argument('cpf_cnpj14', type=str, required=True, help="CPF ou CNPJ do produtor é obrigatório", location='json')
        parser_produtor.add_argument('nome_Produtor', type=str, required=True, help="Nome do produtor é obrigatório", location='json')
        parser_produtor.add_argument('tipo_Produtor', type=str, required=True, help="Produtor 'PF' ou 'PJ' é obrigatório", location='json')
        dados = parser_produtor.parse_args()
        print(parser_produtor)
        validador = produtorModel.validaCpfCnpj(dados["cpf_cnpj14"], dados["tipo_Produtor"])

        if validador == False:
            return {"message": "CPF ou CNPJ inválido"}, 400
        
        produtor = produtorModel.findProdutor(dados["cpf_cnpj14"])
        if not produtor:
            return {"message": f"Produtor {dados['cpf_cnpj14']} não existe"}, 400
        try:
            produtorUpdateParsed = dados
            produtor.updateProdutor(produtorUpdateParsed)
            return {"message": produtorModel.findProdutor(dados["cpf_cnpj14"]).json()}, 201
        except Exception as e:
            return {"message": f"Error Saving Produtor: {str(e)}"}, 500 

    def post(self):
        parser_produtor = reqparse.RequestParser()
        parser_produtor.add_argument('cpf_cnpj14', type=str, required=True, help="CPF ou CNPJ do produtor é obrigatório")
        parser_produtor.add_argument('nome_Produtor', type=str, required=True, help="Nome do produtor é obrigatório")
        parser_produtor.add_argument('tipo_Produtor', type=str, required=True, help="Produtor 'PF' ou 'PJ' é obrigatório")
        dados = parser_produtor.parse_args()
        validador = produtorModel.validaCpfCnpj(dados["cpf_cnpj14"], dados["tipo_Produtor"])

        if validador == False:
            return {"message": "CPF ou CNPJ inválido"}, 400
        
        produtor = produtorModel.findProdutor(dados["cpf_cnpj14"])
        if produtor:
            return {"message": f"Produtor {dados['cpf_cnpj14']} já existe"}, 400
        try:
            produtorParsed = produtorModel(dados["cpf_cnpj14"], dados["nome_Produtor"], dados["tipo_Produtor"])
            produtorParsed.saveProdutor()
            return {"message": produtorParsed.json()}, 201
        except Exception as e:
            return {"message": f"Error Saving Produtor: {str(e)}"}, 500 

    def delete(self):
        parser_produtor = reqparse.RequestParser()
        parser_produtor.add_argument('cpf_cnpj14', type=str, required=True, help="CPF ou CNPJ do produtor é obrigatório")
        parser_produtor.add_argument('tipo_Produtor', type=str, required=True, help="Produtor 'PF' ou 'PJ' é obrigatório")
        dados = parser_produtor.parse_args()
        validador = produtorModel.validaCpfCnpj(dados["cpf_cnpj14"], dados["tipo_Produtor"])

        if validador == False:
            return {"message": "CPF ou CNPJ inválido"}, 400
        
        produtor = produtorModel.findProdutor(dados["cpf_cnpj14"])
        if produtor:
            try:
                produtor.deleteProdutor()
                return {"message": f"Produtor {produtor.nome_Produtor} deleted"}, 204
            except Exception as e:
                return {"message": f"Error deleting Produtor: {str(e)}"}, 500
        else: 
            return {"message": f"Produtor não existe"}, 304