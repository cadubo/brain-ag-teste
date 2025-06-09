from models import banco

class safrasModel(banco.Model):
    __tablename__ = "safras"

    safra_id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    propriedade_id = banco.Column(banco.Integer, nullable=False)
    produtor_id = banco.Column(banco.Integer, nullable=False)
    safra_produto_id = banco.Column(banco.Integer, nullable=False)
    safra_ano = banco.Column(banco.Integer, nullable=False)
    safra_area = banco.Column(banco.Float, nullable=False)
    safra_producao = banco.Column(banco.Float, nullable=False)
    safra_rendimento = banco.Column(banco.Float, nullable=False)
    criado_em = banco.Column(banco.DateTime, nullable=False, default=banco.func.now())
    atualizado_em = banco.Column(banco.DateTime, nullable=False, default=banco.func.now(), onupdate=banco.func.now())
    

    def __init__(self, propriedade_id, produtor_id, safra_produto_id, safra_ano, safra_area, safra_producao, safra_rendimento):
        self.propriedade_id = propriedade_id 
        self.produtor_id = produtor_id 
        self.safra_produto_id = safra_produto_id
        self.safra_ano = safra_ano 
        self.safra_area = safra_area 
        self.safra_producao = safra_producao 
        self.safra_rendimento = safra_rendimento 

    def json(self):
        return {
            "safra_id": self.safra_id,
            "propriedade_id": self.propriedade_id,
            "produtor_id": self.produtor_id,
            "safra_produto_id": self.safra_produto_id,
            "safra_ano": self.safra_ano,
            "safra_area": self.safra_area,
            "safra_producao": self.safra_producao,
            "safra_rendimento": self.safra_rendimento,
            "criado_em": str(self.criado_em),
            "atualizado_em": str(self.atualizado_em)
        }
    
    def updateSafra(self, propriedade):
        self.safra_id = propriedade["safra_id"]
        self.propriedade_id = propriedade["propriedade_id"]
        self.produtor_id = propriedade["produtor_id"]
        self.safra_produto_id = propriedade["safra_produto_id"]
        self.safra_ano = propriedade["safra_ano"]
        self.safra_area = propriedade["safra_area"]
        self.safra_producao = propriedade["safra_producao"]
        self.safra_rendimento = propriedade["safra_rendimento"]
        banco.session.commit()
        

    def deleteSafra(self):
        banco.session.delete(self)
        banco.session.commit()

    @classmethod        
    def findSafra(cls, safra_id):
        safra = cls.query.filter_by(safra_id=safra_id).first()
        if safra:
            return safra
        return None
    
    @classmethod
    def findSafras(cls):
        safras = cls.query.all()
        if safras:
            return safras
        return None
    
    def saveSafra(self):
        banco.session.add(self)
        banco.session.commit()

    def filtraSafras(argumentos):
        query = banco.session.query(safrasModel)
        
        if argumentos.get("safra_id"):
            query = query.filter(safrasModel.safra_id == argumentos["safra_id"])
        if argumentos.get("propriedade_id"):
            query = query.filter(safrasModel.propriedade_id == argumentos["propriedade_id"])
        if argumentos.get("produtor_id"):
            query = query.filter(safrasModel.produtor_id == argumentos["produtor_id"])
        if argumentos.get("safra_ano_min"):
            query = query.filter(safrasModel.safra_ano >= argumentos["safra_ano_min"])
        if argumentos.get("safra_ano_max"):
            query = query.filter(safrasModel.safra_ano <= argumentos["safra_ano_max"])
        if argumentos.get("safra_area_min"):
            query = query.filter(safrasModel.safra_area >= argumentos["safra_area_min"])
        if argumentos.get("safra_area_max"):
            query = query.filter(safrasModel.safra_area <= argumentos["safra_area_max"])
        if argumentos.get("safra_producao_min"):
            query = query.filter(safrasModel.safra_producao >= argumentos["safra_producao_max"])
        if argumentos.get("safra_producao_max"):
            query = query.filter(safrasModel.safra_producao <= argumentos["safra_producao_max"])
        if argumentos.get("safra_rendimento_min"):
            query = query.filter(safrasModel.safra_rendimento <= argumentos["safra_rendimento_min"])
        if argumentos.get("safra_rendimento_max"):
            query = query.filter(safrasModel.safra_rendimento <= argumentos["safra_rendimento_max"])
        if argumentos.get("limit"):
            query = query.limit(argumentos["limit"])
        if argumentos.get("offset"):
            query = query.offset(argumentos["offset"])

        return [safra.json() for safra in query.all()]
    