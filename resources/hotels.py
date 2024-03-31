from flask_restful import Resource, reqparse
from models.hotel_model import HotelModel

# --------- EM MEMORIA
# hotels = [
#     {
#     'id': 1, 
#     'name': 'Hotel 1', 
#     'stars': 3.5,
#     'price': 150,
#     'city': "Recife",
#     },
#     {
#     'id': 2, 
#     'name': 'Hotel 2', 
#     'stars': 5,
#     'price': 240,
#     'city': "João Pessoa",
#     },
#      {
#     'id': 3, 
#     'name': 'Hotel 3', 
#     'stars': 1.2,
#     'price': 77.43,
#     'city': "João Pessoa",
#     },
# ]

# class Hotels(Resource):
#    def get(self):
#       return {'hotels': hotels}

# class Hotel(Resource):
#   def create_args(self):
#     args = reqparse.RequestParser()
#     args.add_argument('name')
#     args.add_argument('price')
#     args.add_argument('city')
#     return args.parse_args()
  
#   def find_hotel(self, id):
#     for hotel in hotels:
#       if hotel['id'] == id:
#         return hotel
  
#   def get(self, id):
#     return self.find_hotel(id)
    
#   def post(self, id):
#     body = self.create_args()
#     new_hotel = HotelModel(len(hotels) + 1, stars=0, **body)
#     new_hotel = new_hotel.json()
#     hotels.append(new_hotel)
#     return new_hotel
    
#   def patch(self, id):
#     hotel = self.find_hotel(id)
#     if hotel:
#       body = self.create_args()
#       new_hotel = HotelModel(id, **body)
#       new_hotel = new_hotel.json()
#       hotels.append(new_hotel)
#       return None, 204
      
#   def delete(self, id):
#     hotel = self.find_hotel(id)
#     if hotel:
#       hotels.remove(hotel)
#       return None, 204
    
# --------- BANCO DE DADOS

class Hotels(Resource):
   def get(self):
      return {'hotels': [HotelModel.json() for HotelModel in HotelModel.query.all()]}
    
class NewHotel(Resource):
  def create_args(self):
    args = reqparse.RequestParser()
    args.add_argument('name', type=str, required=True, help="The field 'name' cannot be left blank")
    args.add_argument('price', type=float, required=True, help="The field 'price' cannot be left blank")
    args.add_argument('city', type=str, required=True, help="The field 'city' cannot be left blank")
    return args.parse_args()
  
  def post(self):
    body = self.create_args()
    new_hotel = HotelModel(stars=0, **body)
    try:
      new_hotel.save_hotel()
    except:
      return {'message': 'An internal error ocurred trying to save hotel'}, 500
    return new_hotel.json(), 201

class Hotel(Resource):
  def create_args(self):
    args = reqparse.RequestParser()
    args.add_argument('name', type=str, required=True, help="The field 'name' cannot be left blank")
    args.add_argument('price', type=float, required=True, help="The field 'price' cannot be left blank")
    args.add_argument('city', type=str, required=True, help="The field 'city' cannot be left blank")
    args.add_argument('stars', type=float, required=False)
    return args.parse_args()
  
  def get(self, id):
    hotel = HotelModel.find_hotel(id)
    if hotel:
      return hotel.json()
    return {'message': 'Hotel not found'}, 404
  
  def patch(self, id):
    hotel = HotelModel.find_hotel(id)
    if hotel:
        body = self.create_args()
        hotel.update_hotel(**body)
        try:
          hotel.save_hotel()
          return hotel.json(), 200
        except:
          return {'message': 'An internal error ocurred trying to patch hotel'}, 500
    return {'message': 'Hotel not found'}, 404
      
  def delete(self, id):
    hotel = HotelModel.find_hotel(id)
    if hotel:
      try:
        hotel.delete_hotel()
        return {'message': 'Hotel deleted'}, 200
      except:
        return {'message': 'An internal error ocurred trying to delete'}, 500
    return {'message': 'Hotel not found'}, 404
    