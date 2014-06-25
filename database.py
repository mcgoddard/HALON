from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:test1@localhost/halon', convert_unicode=True, pool_size=20, max_overflow=5)
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
    from models import Character, Tile
    Base.metadata.create_all(bind=engine)
    # Seed characters in the database
    medic = Character("Medic", "The ships medic. Not much of a fighter, but he has regenerating health.", 1000, 4, 5, 2)
    infiltrator = Character("Infiltrator", "The infiltrator was just hitching a ride. Greater movement speed.", 1000, 6, 5, 0)
    engineer = Character("Engineer", "The chief engineer on board the ship. Decreased hacking times.", 1000, 4, 3, 0)
    security = Character("Security", "The head of security aboard the ship. He benefits from additional health.", 1250, 4, 5, 0)
    captain = Character("Captain", "The ships captain. Jack of all trades, master of none.", 1100, 5, 4, 1)
    hal = Character("HAL", "The homicidal computer causing this mess!", 1000, 100, 0, 10)
    db_session.add(medic)
    db_session.add(infiltrator)
    db_session.add(engineer)
    db_session.add(security)
    db_session.add(captain)
    db_session.add(hal)
    # Seed the game map
    tile00 = Tile(0, 0, 3, 0)
    tile01 = Tile(0, 1, 3, 0)
    tile02 = Tile(0, 2, 3, 0)
    tile03 = Tile(0, 3, 3, 0)
    tile10 = Tile(1, 0, 3, 0)
    tile11 = Tile(1, 1, 6, 0)
    tile12 = Tile(1, 2, 6, 0)
    tile13 = Tile(1, 3, 3, 0)
    tile20 = Tile(2, 0, 3, 0)
    tile21 = Tile(2, 1, 6, 0)
    tile22 = Tile(2, 2, 1, 1)
    tile23 = Tile(2, 3, 3, 0)
    tile30 = Tile(3, 0, 3, 0)
    tile31 = Tile(3, 1, 3, 0)
    tile32 = Tile(3, 2, 3, 0)
    tile33 = Tile(3, 3, 3, 0)
    db_session.add(tile00)
    db_session.add(tile01)
    db_session.add(tile02)
    db_session.add(tile03)
    db_session.add(tile10)
    db_session.add(tile11)
    db_session.add(tile12)
    db_session.add(tile13)
    db_session.add(tile20)
    db_session.add(tile21)
    db_session.add(tile22)
    db_session.add(tile23)
    db_session.add(tile30)
    db_session.add(tile31)
    db_session.add(tile32)
    db_session.add(tile33)
    # Commit seeds
    db_session.commit()