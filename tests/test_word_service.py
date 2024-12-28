from tests.base import BaseTestCase
from app.services.word_service import WordService

class TestWordService(BaseTestCase):
    """单词服务测试类"""
    
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
        
    def test_create_word(self):
        """测试创建单词"""
        word = WordService.create_word(self.word_data)
        self.assertEqual(word.word, 'test')
        self.assertEqual(word.correct_translation, '测试')
        self.assertEqual(word.error_count, 0)
        
    def test_get_word_by_id(self):
        """测试通过ID获取单词"""
        word = WordService.create_word(self.word_data)
        fetched_word = WordService.get_word_by_id(word.id)
        self.assertEqual(fetched_word.word, word.word)
        
    def test_get_all_words(self):
        """测试获取所有单词"""
        WordService.create_word(self.word_data)
        words = WordService.get_all_words()
        self.assertEqual(len(words), 1)
        
    def test_get_error_prone_words(self):
        """测试获取易错单词"""
        word1 = WordService.create_word(self.word_data)
        word2 = WordService.create_word({
            'word': 'test2',
            'part_of_speech': 'v.',
            'correct_translation': '测试2',
            'wrong_translation_1': '错误1',
            'wrong_translation_2': '错误2',
            'wrong_translation_3': '错误3'
        })
        
        # 增加错误次数
        WordService.increment_error_count(word1.id)
        WordService.increment_error_count(word2.id)
        WordService.increment_error_count(word2.id)
        
        error_prone_words = WordService.get_error_prone_words(limit=2)
        self.assertEqual(len(error_prone_words), 2)
        self.assertEqual(error_prone_words[0].error_count, 2)
        
    def test_update_word(self):
        """测试更新单词"""
        word = WordService.create_word(self.word_data)
        updated_data = {'correct_translation': '新测试'}
        updated_word = WordService.update_word(word.id, updated_data)
        self.assertEqual(updated_word.correct_translation, '新测试')
        
    def test_delete_word(self):
        """测试删除单词"""
        word = WordService.create_word(self.word_data)
        success = WordService.delete_word(word.id)
        self.assertTrue(success)
        self.assertIsNone(WordService.get_word_by_id(word.id))
        
    def test_increment_error_count(self):
        """测试增加错误次数"""
        word = WordService.create_word(self.word_data)
        updated_word = WordService.increment_error_count(word.id)
        self.assertEqual(updated_word.error_count, 1)
