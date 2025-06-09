from models import banco

class produtosModel(banco.Model):
    __tablename__ = "produtos"

    produto_id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    nome_produto = banco.Column(banco.String, nullable=False, unique=True)
    descricao = banco.Column(banco.String, nullable=False)
    categoria = banco.Column(banco.String, nullable=False)
    criado_em = banco.Column(banco.DateTime, nullable=False, default=banco.func.now())
    atualizado_em = banco.Column(banco.DateTime, nullable=False, default=banco.func.now(), onupdate=banco.func.now())

    def __init__(self, nome_produto, descricao, categoria):
        self.nome_produto = nome_produto
        self.descricao = descricao
        self.categoria = categoria

    def json(self):
        return {
            "id_produto": self.produto_id,
            "nome_produto": self.nome_produto,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "criado_em": str(self.criado_em),
            "atualizado_em": str(self.atualizado_em)
        }
    
    
          
    def updateProduto(self, produto):
        self.nome_produto = produto["nome_produto"]
        self.descricao = produto["descricao"]
        self.categoria = produto["categoria"]
        banco.session.commit()

    def deleteProduto(self):
        banco.session.delete(self)
        banco.session.commit()

    @classmethod        
    def findProduto(cls, nome_produto):
        produto = cls.query.filter_by(nome_produto=nome_produto).first()
        if produto:
            return produto
        return None
    
    @classmethod
    def findProdutos(cls):
        produtos = cls.query.all()
        if produtos:
            return produtos
        return None
    
    def saveProduto(self):
        banco.session.add(self)
        banco.session.commit()

    @classmethod
    def findProdutoByID(cls, produto_id):
        produto = cls.query.filter_by(produto_id=produto_id).first()
        if produto:
            return produto
        return None