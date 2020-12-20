from sqlalchemy import Column, String, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

from base import Base

schedule = Table(
    'Schedule', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_s', Integer, ForeignKey('Sessions.id')),
    Column('id_c', Integer, ForeignKey('Cinemas.id'))
)


class Session(Base):
    __tablename__ = 'Sessions'
    id = Column(Integer, primary_key=True)
    id_f = Column(Integer, ForeignKey('Films.id'))
    start_date = Column(Date)
    hall_name = Column(String(30))
    film = relationship("Film", uselist=False)
    cinemas = relationship("Cinema", secondary=schedule)

    def __repr__(self):
        return "<Sessions('%s', '%s', '%s')>" % (self.start_date, self.hall_name, self.film.name_f)
