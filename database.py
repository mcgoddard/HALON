from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:test1@localhost/halon', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    from models import Character
    Base.metadata.create_all(bind=engine)
    # Seed characters in the database
    medic = Character("Medic", "The ships medic. Not much of a fighter, but he has regenerating health.", 1000, 4, 5, 2)
    infiltrator = Character("Infiltrator", "The infiltrator was just hitching a ride. Greater movement speed.", 1000, 6, 5, 0)
    engineer = Character("Engineer", "The chief engineer on board the ship. Decreased hacking times.", 1000, 4, 3, 0)
    security = Character("Security", "The head of security aboard the ship. He benefits from additional health.", 1250, 4, 5, 0)
    captain = Character("Captain", "The ships captain. Jack of all trades, master of none.", 1100, 5, 4, 1)
    hal = Character("HAL", "The homicidal computer causing this mess!", 1000, 0, 0, 10)
    db_session.add(medic)
    db_session.add(infiltrator)
    db_session.add(engineer)
    db_session.add(security)
    db_session.add(captain)
    db_session.add(hal)
    db_session.commit()
    # Seed the game map
