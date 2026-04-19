import pytest
import logging
import os
import time
from db.database_manager import init_db, get_session, Account, process_transfer, engine

# --- AUDIT LOGGER CONFIGURATION ---
# The 'force=True' ensures that Pytest doesn't block the file creation
logging.basicConfig(
    filename='audit.log',
    filemode='a', # 'a' means append, so it keeps a history
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True 
)

@pytest.fixture(scope="function", autouse=True)
def setup_bank_system():
    """
    CLEAN SLATE PROTOCOL:
    Forces the database engine to disconnect so Windows can delete
    the file and recreate it fresh for every test.
    """
    db_file = "fintech_bank.db"
    
    # Force SQLAlchemy to release the file lock
    engine.dispose() 

    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except PermissionError:
            # Short pause to let Windows catch up if the file is being stubborn
            time.sleep(0.2)
            os.remove(db_file)
    
    init_db()

def test_successful_transfer_audit():
    """
    Scenario: Standard internal transfer.
    Requirement: Checking must decrease, Savings must increase, Sum must remain constant.
    """
    session = get_session()
    transfer_amount = 100.0
    
    # Audit Baseline
    checking = session.query(Account).filter_by(id=1).first()
    savings = session.query(Account).filter_by(id=2).first()
    initial_total = checking.balance + savings.balance

    logging.info(f"STARTING AUDIT: Transferring ${transfer_amount} from ID:1 to ID:2")
    
    # Execute transaction
    success = process_transfer(session, from_id=1, to_id=2, amount=transfer_amount)
    
    # Force refresh from disk
    session.expire_all() 
    
    updated_total = checking.balance + savings.balance

    assert success is True
    assert checking.balance == 900.0
    assert savings.balance == 600.0
    assert updated_total == initial_total
    
    logging.info(f"AUDIT PASSED: Balance integrity verified. Total funds: ${updated_total}")
    session.close()

def test_insufficient_funds_protection():
    """
    Scenario: User attempts to transfer more than their balance.
    Requirement: System must reject transfer and keep balances untouched.
    """
    session = get_session()
    overdraft_amount = 5000.0 
    
    logging.warning(f"SECURITY AUDIT: Attempting high-value transfer of ${overdraft_amount}")
    
    success = process_transfer(session, from_id=1, to_id=2, amount=overdraft_amount)
    
    session.expire_all()
    checking = session.query(Account).filter_by(id=1).first()
    
    assert success is False
    assert checking.balance == 1000.0
    
    logging.info("AUDIT PASSED: System correctly blocked insufficient funds transfer.")
    session.close()