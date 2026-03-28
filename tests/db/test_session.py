from sqlalchemy import text

def test_session_created(session):
    assert session is not None

def test_session_execute_query(session):
    result = session.execute(text("SELECT 1"))
    assert result.scalar() == 1
    
def test_multiple_queries(session):
    result1 = session.execute(text("SELECT 1")).scalar()
    result2 = session.execute(text("SELECT 2")).scalar()
    
    assert result1 == 1
    assert result2 == 2
    