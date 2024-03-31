from sql_alchemy import db

class HotelModel(db.Model):
  __tablename__ = 'hotels'
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(80))
  stars = db.Column(db.Float(precision=1))
  price = db.Column(db.Float(precision=2))
  city = db.Column(db.String(40))
  
  def __init__(self, name, stars, price, city):
    self.name = name
    self.stars = stars
    self.price = price
    self.city = city
  
  def json(self):
    return {
      'id': self.id,
      'name': self.name,
      'stars': self.stars,
      'price': self.price,
      'city': self.city,
    }
    
  def save_hotel(self):
    db.session.add(self)
    db.session.commit()
    
  def update_hotel(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)
    
  def delete_hotel(self):
    db.session.delete(self)
    db.session.commit()
    
  @classmethod
  def find_hotel(cls, id):
    hotel = cls.query.filter_by(id=id).first()
    if hotel:
      return hotel
    return None