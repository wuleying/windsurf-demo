import json
from tests.base import BaseTestCase
from app.services.word_service import WordService

class TestWordRoutes(BaseTestCase):
    """单词路由测试类"""
    
    def setUp(self):
        """测试前置"""
        super().setUp()
        self.word_data = {
            'word': 'test',
            'part_of_speech': 'n.',
            'correct_translation': '测试',
            'wrong_translation_1': '错误1',
            'wrong_translation_2': '错误2',
            'wrong_translation_3': '错误3'
        }
        
    def test_get_words(self):
        """测试获取所有单词"""
        WordService.create_word(self.word_data)
        response = self.client.get('/api/words/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        
    def test_get_error_prone_words(self):
        """测试获取易错单词"""
        word = WordService.create_word(self.word_data)
        WordService.increment_error_count(word.id)
        response = self.client.get('/api/words/error-prone')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['error_count'], 1)
        
    def test_get_word(self):
        """测试获取单个单词"""
        word = WordService.create_word(self.word_data)
        response = self.client.get(f'/api/words/{word.id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['word'], 'test')
        
    def test_create_word(self):
        """测试创建单词"""
        response = self.client.post(
            '/api/words/',
            data=json.dumps(self.word_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['word'], 'test')
        
    def test_update_word(self):
        """测试更新单词"""
        word = WordService.create_word(self.word_data)
        update_data = {'correct_translation': '新测试'}
        response = self.client.put(
            f'/api/words/{word.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['correct_translation'], '新测试')
        
    def test_delete_word(self):
        """测试删除单词"""
        word = WordService.create_word(self.word_data)
        response = self.client.delete(f'/api/words/{word.id}')
        self.assertEqual(response.status_code, 204)
        
    def test_increment_error_count(self):
        """测试增加错误次数"""
        word = WordService.create_word(self.word_data)
        response = self.client.post(f'/api/words/{word.id}/increment-error')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['error_count'], 1)
