import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db

class TestServer(unittest.TestCase):
    def test_search(self):
        res = db.search_records('students', filters={'cohort': 'A1'})
        self.assertGreaterEqual(len(res), 3)

    def test_invalid_table(self):
        with self.assertRaises(ValueError):
            db.search_records('invalid_table')
            
    def test_invalid_column(self):
        with self.assertRaises(ValueError):
            db.search_records('students', filters={'bad_col': 'val'})
            
    def test_aggregate(self):
        cnt = db.aggregate_records('students', 'count')
        self.assertGreater(cnt, 0)
        
    def test_insert(self):
        res = db.insert_record('courses', {'title': 'AI Engineering', 'credits': 4})
        self.assertIsNotNone(res.get('id'))
        
if __name__ == '__main__':
    unittest.main()
