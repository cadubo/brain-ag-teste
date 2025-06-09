from models import banco

class propriedadesModel(banco.Model):
    __tablename__ = "propriedades"

    propriedade_id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    produtor_id = banco.Column(banco.Integer, nullable=False)
    nome_Propriedade = banco.Column(banco.String(80), nullable=False)
    cidade_Propriedade = banco.Column(banco.String(80), nullable=False)
    estado_Propriedade = banco.Column(banco.String(80), nullable=False)
    area_total_Propriedade = banco.Column(banco.Float, nullable=False)
    area_vegetacao_Propriedade = banco.Column(banco.Float, nullable=False)
    area_agriculturavel_Propriedade = banco.Column(banco.Float, nullable=False)
    criado_em = banco.Column(banco.DateTime, nullable=False, default=banco.func.now())
    atualizado_em = banco.Column(banco.DateTime, nullable=False, default=banco.func.now(), onupdate=banco.func.now())

    def __init__(self, produtor_id, nome_Propriedade, cidade_Propriedade, estado_Propriedade, area_total_Propriedade, area_vegetacao_Propriedade, area_agriculturavel_Propriedade):
        self.produtor_id = produtor_id 
        self.nome_Propriedade = nome_Propriedade 
        self.cidade_Propriedade = cidade_Propriedade 
        self.estado_Propriedade = estado_Propriedade 
        self.area_total_Propriedade = area_total_Propriedade 
        self.area_vegetacao_Propriedade = area_vegetacao_Propriedade 
        self.area_agriculturavel_Propriedade = area_agriculturavel_Propriedade 
    
    def json(self):
        return {
            "propriedade_id": self.propriedade_id,
            "produtor_id": self.produtor_id,
            "nome_Propriedade": self.nome_Propriedade,
            "cidade_Propriedade": self.cidade_Propriedade,
            "estado_Propriedade": self.estado_Propriedade,
            "area_total_Propriedade": self.area_total_Propriedade,
            "area_vegetacao_Propriedade": self.area_vegetacao_Propriedade,
            "area_agriculturavel_Propriedade": self.area_agriculturavel_Propriedade,
            "criado_em": str(self.criado_em),
            "atualizado_em": str(self.atualizado_em)
        }
    
    def updatePropriedade(self, propriedade):
        self.produtor_id = propriedade["produtor_id"]
        self.nome_Propriedade = propriedade["nome_Propriedade"]
        self.cidade_Propriedade = propriedade["cidade_Propriedade"]
        self.estado_Propriedade = propriedade["estado_Propriedade"]
        self.area_total_Propriedade = propriedade["area_total_Propriedade"]
        self.area_vegetacao_Propriedade = propriedade["area_vegetacao_Propriedade"]
        self.area_agriculturavel_Propriedade = propriedade["area_agriculturavel_Propriedade"]
        banco.session.commit()
        

    def deletePropriedade(self):
        banco.session.delete(self)
        banco.session.commit()

    @classmethod        
    def findPropriedade(cls, nome_Propriedade):
        propriedade = cls.query.filter_by(nome_Propriedade=nome_Propriedade).first()
        if propriedade:
            return propriedade
        return None
    
    @classmethod
    def findPropriedades(cls):
        propriedades = cls.query.all()
        if propriedades:
            return propriedades
        return None
    
    def savePropriedade(self):
        banco.session.add(self)
        banco.session.commit()

    def filtra_propriedades(argumentos):
        query = banco.session.query(propriedadesModel)
        
        if argumentos.get("propriedade_id"):
            query = query.filter(propriedadesModel.propriedade_id == argumentos["propriedade_id"])
        if argumentos.get("produtor_id"):
            query = query.filter(propriedadesModel.produtor_id == argumentos["produtor_id"])
        if argumentos.get("cidade_Propriedade"):
            query = query.filter(propriedadesModel.cidade_Propriedade == argumentos["cidade_Propriedade"])
        if argumentos.get("estado_Propriedade"):
            query = query.filter(propriedadesModel.estado_Propriedade == argumentos["estado_Propriedade"])
        if argumentos.get("area_total_min"):
            query = query.filter(propriedadesModel.area_total_Propriedade >= argumentos["area_total_min"])
        if argumentos.get("area_total_max"):
            query = query.filter(propriedadesModel.area_total_Propriedade <= argumentos["area_total_max"])
        if argumentos.get("area_agriculturavel_min"):
            query = query.filter(propriedadesModel.area_agriculturavel_Propriedade >= argumentos["area_agriculturavel_min"])
        if argumentos.get("area_agriculturavel_max"):
            query = query.filter(propriedadesModel.area_agriculturavel_Propriedade <= argumentos["area_agriculturavel_max"])
        if argumentos.get("limit"):
            query = query.limit(argumentos["limit"])
        if argumentos.get("offset"):
            query = query.offset(argumentos["offset"])

        return [propriedade.json() for propriedade in query.all()]
    
    @classmethod
    def findPropriedadeByID(cls, propriedade_id):
        propriedade = cls.query.filter_by(propriedade_id=propriedade_id).first()
        if propriedade:
            return propriedade
        return None