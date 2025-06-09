from models import banco
from pycpfcnpj import cpfcnpj

class produtorModel(banco.Model):
    __tablename__ = "produtores"

    produtor_id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    cpf_cnpj14 = banco.Column(banco.String, nullable=False, unique=True)
    nome_Produtor = banco.Column(banco.String(80), nullable=False)
    tipo_Produtor = banco.Column(banco.String(80), nullable=False)
    criado_em = banco.Column(banco.DateTime, nullable=False, default=banco.func.now())
    atualizado_em = banco.Column(banco.DateTime, nullable=False, default=banco.func.now(), onupdate=banco.func.now())

    def __init__(self, cpf_cnpj14, nome_Produtor, tipo_Produtor):
        self.cpf_cnpj14 = cpf_cnpj14
        self.nome_Produtor = nome_Produtor
        self.tipo_Produtor = tipo_Produtor

    def json(self):
        return {
            "id_Produtor": self.produtor_id,
            "cpf_cnpj14": self.cpf_cnpj14,
            "nome_Produtor": self.nome_Produtor,
            "tipo_Produtor": self.tipo_Produtor,
            "criado_em": str(self.criado_em),
            "atualizado_em": str(self.atualizado_em)
        }   
    
    @classmethod
    def findProdutor(cls, cpf_cnpj14):
        produtor = cls.query.filter_by(cpf_cnpj14=cpf_cnpj14).first()
        if produtor:
            return produtor
        return None
    
    @classmethod
    def findProdutorByID(cls, produtor_id):
        produtor = cls.query.filter_by(produtor_id=produtor_id).first()
        if produtor:
            return produtor
        return None
    
    @classmethod
    def findProdutores(cls):
        produtores = cls.query.all()
        if produtores:
            return produtores
        return None
    
    def saveProdutor(self):
        banco.session.add(self)
        banco.session.commit()
        
    @staticmethod
    def validaCpfCnpj(cpf_cnpj14, tipo_Produtor):
        if tipo_Produtor == "PF":
            return cpfcnpj.validate(cpf_cnpj14.zfill(11))
        elif tipo_Produtor == "PJ":
            return cpfcnpj.validate(cpf_cnpj14.zfill(14))
        else:
            return False
        
    def updateProdutor(self, produtor):
        self.cpf_cnpj14 = produtor["cpf_cnpj14"]
        self.nome_Produtor = produtor["nome_Produtor"]
        self.tipo_Produtor = produtor["tipo_Produtor"]
        banco.session.commit()

    def deleteProdutor(self):
        banco.session.delete(self)
        banco.session.commit()

            
