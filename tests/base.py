import unittest
from app import create_app, db

class BaseTestCase(unittest.TestCase):
    """测试基类"""
    
    def setUp(self):
        """测试前置"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        """测试后置"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
