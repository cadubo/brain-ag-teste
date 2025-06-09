from flask_restful import Resource,reqparse,request
from models.produtosModel import produtosModel



class produtos(Resource):

    def get(self):
        try:
            parser_produto = reqparse.RequestParser()
            parser_produto.add_argument('nome_produto', type=str)
            dados = parser_produto.parse_args()
            produto = produtosModel.findProduto(dados["nome_produto"])
            if produto:
                return {"message": produto.json()}, 200
            return {"message": "Produto Não Encontrado"}, 400

        except:
            produtos = produtosModel.findProdutos()
            return {"message": [produto.json() for produto in produtos]}, 200
         
    def put(self):
        parser_produto = reqparse.RequestParser()
        parser_produto.add_argument('nome_produto', type=str, required=True, help="Nome do produto é obrigatório")
        parser_produto.add_argument('descricao', type=str, required=True, help="Descrição do produto é obrigatório")
        parser_produto.add_argument('categoria', type=str, required=True, help="Categoria do produto é obrigatório")
        dados = parser_produto.parse_args()
        produto = produtosModel.findProduto(dados["nome_produto"])
        if not produto:
            return {"message": f'Produto {dados["nome_produto"]} não existe'}, 400
        try:
            produto.updateProduto(dados)
            return {"message": produtosModel.findProduto(dados["nome_produto"]).json()}, 201
        except Exception as e:
            return {"message": f"Error Saving Produto: {str(e)}"}, 500
        
    def post(self):
        parser_produtor = reqparse.RequestParser()
        parser_produtor.add_argument('nome_produto', type=str, required=True, help="Nome do produto é obrigatório")
        parser_produtor.add_argument('descricao', type=str, required=True, help="Descrição do produto é obrigatório")
        parser_produtor.add_argument('categoria', type=str, required=True, help="Categoria do produto é obrigatório")
        dados = parser_produtor.parse_args()
        produto = produtosModel.findProduto(dados["nome_produto"])

        if produto:
            return {"message": f"Produto {dados['nome_produto']} já existe"}, 400
        try:
            produtoParsed = produtosModel(dados["nome_produto"], dados["descricao"], dados["categoria"])
            produtoParsed.saveProduto()
            return {"message": produtoParsed.json()}, 201
        except Exception as e:
            return {"message": f"Error Saving Produtor: {str(e)}"}, 500 

    def delete(self):
        parser_produtor = reqparse.RequestParser()
        parser_produtor.add_argument('nome_produto', type=str, required=True, help="Nome do produto é obrigatório")
        dados = parser_produtor.parse_args()
        produto = produtosModel.findProduto(dados["nome_produto"])
        if not produto:
            return {"message": f"Produto {dados['nome_produto']} não existe"}, 400
        try:
            produto.deleteProduto()
            return {"message": f"Produto Deletado"}, 204
        except Exception as e:
            return {"message": f"Error Deleting Produto: {str(e)}"}, 500