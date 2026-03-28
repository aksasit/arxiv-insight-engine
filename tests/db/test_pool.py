def test_connection_pool(db):
    sessions = []
    
    for _ in range(5):
        s = db.session_factory()
        sessions.append(s)
    
    assert len(sessions) == 5
    
    for s in sessions:
        s.close()
    

def test_pool_reuse(db):
    s1 = db.session_factory()
    s2 = db.session_factory()
    
    assert s1.bind() == s2.bind() # Same Engine
    
    s1.close()
    s2.close()   
        