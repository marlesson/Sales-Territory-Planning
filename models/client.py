import random

class Client(object):
  def __init__(self, benefit, lat= None, lon= None, visits=1, time_service = random.gauss(100, 30)):
    self.benefit      = benefit
    self.salesman_id  = None
    self.visits       = visits
    self.time_service = time_service
    self.lat   = lat
    self.lon   = lon