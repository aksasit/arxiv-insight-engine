from sqlalchemy import text

def test_commit(session):
    session.execute(text("CREATE TABLE IF NOT EXISTS test_table (id INT)"))
    session.execute(text("INSERT INTO test_table (id) VALUES (1)"))
    session.commit()
    
    result = session.execute(
        text("SELECT COUNT(*) FROM test_table WHERE id = 1")
    )
    
    assert result.scalar() == 1
    
def test_rollback(db):
    try:
        with db.get_session() as session:
            session.execute(text("INSERT INTO test_table (id) VALUES (2)"))
            raise Exception('Force rollback')
    except Exception:
        pass
    
    with db.get_session() as session:
        result = session.execute(
            text("SELECT COUNT(*) FROM test_table WHERE id = 2")
        )
        
        assert result.scalar() == 0