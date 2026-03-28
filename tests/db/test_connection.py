def test_database_engine_initialized(db):
    assert db.engine is not None

def test_database_can_connect(db):
    with db.engine.connect() as conn:
        result = conn.execute("SELECT 1")
        assert result.scalar() == 1
        