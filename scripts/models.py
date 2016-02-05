from sqlalchemy import PrimaryKeyConstraint, Column, String, Integer, LargeBinary, Date, Time, Float
from settings import Base

class DotImage(Base):
    
    __tablename__ = 'DotImage'
    
    id = Column(Integer)
    locationId = Column(String)
    time = Column(Time)
    date = Column(Date)
    path = Column(String)
    filename = Column(String)
    rain = Column(Integer)
    size = Column(Float(precision=2)) #Kb

    PrimaryKeyConstraint(locationId, date, time, name="pk")

    def __repr__(self):
        return "id: {id}\nlocationId: {lid}\ntime: {t}\ndate: {d}\npath: {p}, size: {s}".format(
            id=self.id, lid=self.locationId, t=self.time, d=self.date, p=self.path, s=self.size)

        