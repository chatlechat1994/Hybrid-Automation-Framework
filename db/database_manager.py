from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Define the Bank Account structure
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    account_type = Column(String)  # 'Checking' or 'Savings'
    balance = Column(Float)

engine = create_engine('sqlite:///fintech_bank.db')

def init_db():
    """Initializes the database and seeds it with starting money."""
    Base.metadata.create_all(engine)
    session = get_session()
    # Only seed if the database is empty
    if not session.query(Account).first():
        session.add_all([
            Account(id=1, account_type='Checking', balance=1000.0),
            Account(id=2, account_type='Savings', balance=500.0)
        ])
        session.commit()
    session.close()

def get_session():
    """Creates a new database session."""
    Session = sessionmaker(bind=engine)
    return Session()


def process_transfer(session, from_id, to_id, amount):
    """
    Business Logic: Transfers money between accounts.
    Returns True if successful, False if insufficient funds.
    """
    sender = session.query(Account).filter_by(id=from_id).first()
    receiver = session.query(Account).filter_by(id=to_id).first()

    if sender and receiver and sender.balance >= amount:
        sender.balance -= amount
        receiver.balance += amount
        session.commit()
        return True
    
    return False # Not enough money or account not found