from sqlalchemy import Column, String, Integer

from base import Base


class Film(Base):
    __tablename__ = 'Films'
    id = Column(Integer, primary_key=True)
    name_f = Column(String(30))
    year_f = Column(Integer)
    genre_f = Column(String(30))
    duration_f = Column(Integer)

    def __repr__(self):
        return "<Films('%s', '%s', '%s', '%s')>" % (self.name_f, self.year_f, self.genre_f, self.duration_f)
