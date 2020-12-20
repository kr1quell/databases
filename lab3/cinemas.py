from sqlalchemy import Column, String, Integer

from base import Base


class Cinema(Base):
    __tablename__ = 'Cinemas'
    id = Column(Integer, primary_key=True)
    name_c = Column(String(30))
    street = Column(String(30))

    def __repr__(self):
        return "<Cinemas('%s', '%s')>" % (self.name_c, self.street)
