from flask_restful import Resource,reqparse,request
from models.hotelModel import HotelModel
import sys



class Hoteis(Resource):
    @staticmethod
    def normalize_path_params(cidade=None,
                          estrelas_min = 0,
                          estrelas_max = 6,
                          diaria_min = 0,
                          diaria_max = 10000000,
                          limit = 50,
                          offset = 0, **dados):
        if cidade:
            return {
                'estrelas_min': estrelas_min,
                'estrelas_max': estrelas_max,
                'diaria_min': diaria_min,
                'diaria_max': diaria_max,
                'cidade': cidade,
                'limit': limit,
                'offset': offset}
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset}
    

    def parser_params(path_params):
        path_params.add_argument('cidade', type=str, required=False, location='args')
        path_params.add_argument('estrelas_min', type=float, required=False, location='args')
        path_params.add_argument('estrelas_max', type=float, required=False, location='args')
        path_params.add_argument('diaria_min', type=float, required=False, location='args')
        path_params.add_argument('diaria_max', type=float, required=False, location='args')
        path_params.add_argument('limit', type=int, required=False, location='args')
        path_params.add_argument('offset', type=int, required=False, location='args')
        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        print(dados)
        return Hoteis.normalize_path_params(**dados_validos)
    
    def get(self):
        argumentos = Hoteis.parser_params(reqparse.RequestParser())
        filtra_hoteis = HotelModel.filtra_hotel(argumentos)
        print(filtra_hoteis)
        return {"message": filtra_hoteis}, 200
        
    
    def put(self, hotel_id):
        return {"message": f"Hotel {hotel_id} updated"}, 200

    def post(self, hotel_id):
        return {"message": f"Hotel {hotel_id} updated"}, 200

    def delete(self, hotel_id):
        return {"message": f"Hotel {hotel_id} deleted"}, 204
    
class Hotel(Resource):
    
    def parser_hotel(hotel_id, argumentos):
        argumentos.add_argument("nome", type=str, required=True, help="Nome do hotel é obrigatório")
        argumentos.add_argument("estrelas", type=float, required=True, help="Estrelas do hotel é obrigatório")
        argumentos.add_argument("diaria", type=float, required=True, help="Diária do hotel é obrigatório")
        argumentos.add_argument("cidade", type=str, required=True, help="Cidade do hotel é obrigatório")
        dados = argumentos.parse_args()
        Hotel_Obj = HotelModel(hotel_id, dados["nome"], dados["estrelas"], dados["diaria"], dados["cidade"])
        return Hotel_Obj
                
    def get(self, hotel_id):
        hotel = HotelModel.findhotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {"message": "Hotel not found"}, 404
    
    def put(self, hotel_id):
        hotel_parsed = Hotel.parser_hotel(hotel_id, reqparse.RequestParser())
        hotel = HotelModel.findhotel(hotel_id)
        if hotel:
            hotel.update_hotel(hotel_parsed)
            return {"message": f"Hotel {hotel_id} updated"}, 200
        else:  
            try:
                hotel_parsed.save_hotel()
                return {"message": f"Hotel Criado\n {hotel_parsed}"}, 201
            except Exception as e:
                return {"message": f"Error saving hotel: {str(e)}"}, 500
        
    def post(self, hotel_id):
        hotel = HotelModel.findhotel(hotel_id)
        if hotel:
            return {"message": f"Hotel {hotel_id} already exists"}, 400
        hotel_parsed = Hotel.parser_hotel(hotel_id, reqparse.RequestParser())
        try:
            hotel_parsed.save_hotel()
            return {"message": hotel_parsed.json()}, 201
        except Exception as e:
            return {"message": f"Error saving hotel: {str(e)}"}, 500

    def delete(self, hotel_id):
        hotel = HotelModel.findhotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {"message": f"Hotel {hotel_id} deleted"}, 204
            except Exception as e:
                return {"message": f"Error saving hotel: {str(e)}"}, 500
        else: 
            return {"message": f"Hotel not exists"}, 304