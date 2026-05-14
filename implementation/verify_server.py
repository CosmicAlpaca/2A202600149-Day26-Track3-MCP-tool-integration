import sys

def verify():
    import db
    print("Testing DB logic...")
    schema = db.get_schema()
    assert 'students' in schema, "students table missing"
    
    # Test search
    res = db.search_records('students', filters={'cohort': 'A1'})
    assert len(res) == 3, f"Expected 3 A1 students, got {len(res)}"
    
    # Test insert
    new_student = db.insert_record('students', {'name': 'Test Student', 'cohort': 'T1', 'score': 100})
    assert new_student['id'] is not None
    
    # Test aggregate
    count = db.aggregate_records('students', 'count')
    assert count >= 5, f"Expected at least 5 students, got {count}"
    
    # Test error handling
    try:
        db.search_records('unknown_table')
        assert False, "Should reject unknown table"
    except ValueError as e:
        assert 'Unknown table' in str(e)
        
    try:
        db.search_records('students', filters={'unknown_col': 1})
        assert False, "Should reject unknown column"
    except ValueError as e:
        assert 'Unknown column' in str(e)

    try:
        db.insert_record('students', {})
        assert False, "Should reject empty insert"
    except ValueError as e:
        assert 'Empty insert' in str(e)

    print("DB logic tests passed!")

if __name__ == "__main__":
    verify()
