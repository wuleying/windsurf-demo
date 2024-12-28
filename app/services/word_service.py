from typing import List, Dict, Optional, Tuple
from app import db
from app.models.word import Word
import random
from sqlalchemy import func

class WordService:
    """单词服务类"""
    
    @staticmethod
    def create_word(word_data: Dict) -> Word:
        """
        创建新单词
        
        Args:
            word_data: 单词数据字典
            
        Returns:
            Word: 创建的单词实例
        """
        word = Word(**word_data)
        db.session.add(word)
        db.session.commit()
        return word
    
    @staticmethod
    def get_word_by_id(word_id: int) -> Optional[Word]:
        """
        通过ID获取单词
        
        Args:
            word_id: 单词ID
            
        Returns:
            Optional[Word]: 单词实例或None
        """
        return Word.query.get(word_id)
    
    @staticmethod
    def get_all_words() -> List[Word]:
        """
        获取所有单词
        
        Returns:
            List[Word]: 单词列表
        """
        return Word.query.all()
    
    @staticmethod
    def get_error_prone_words(limit: int = 10) -> List[Word]:
        """
        获取易错单词列表
        
        Args:
            limit: 返回数量限制
            
        Returns:
            List[Word]: 单词列表
        """
        return Word.query.order_by(Word.error_count.desc()).limit(limit).all()
    
    @staticmethod
    def update_word(word_id: int, word_data: Dict) -> Optional[Word]:
        """
        更新单词信息
        
        Args:
            word_id: 单词ID
            word_data: 更新的单词数据
            
        Returns:
            Optional[Word]: 更新后的单词实例或None
        """
        word = Word.query.get(word_id)
        if word:
            for key, value in word_data.items():
                setattr(word, key, value)
            db.session.commit()
        return word
    
    @staticmethod
    def delete_word(word_id: int) -> bool:
        """
        删除单词
        
        Args:
            word_id: 单词ID
            
        Returns:
            bool: 删除是否成功
        """
        word = Word.query.get(word_id)
        if word:
            db.session.delete(word)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def increment_error_count(word_id: int) -> Optional[Word]:
        """
        增加单词错误次数
        
        Args:
            word_id: 单词ID
            
        Returns:
            Optional[Word]: 更新后的单词实例或None
        """
        word = Word.query.get(word_id)
        if word:
            word.error_count += 1
            db.session.commit()
        return word

    @staticmethod
    def calculate_word_weight(word: Word) -> float:
        """
        计算单词的权重分数
        
        权重计算规则：
        1. 基础权重为1
        2. 每次错误增加0.5的权重
        3. 最近更新的单词获得额外权重(1.5)
        
        Args:
            word: 单词实例
            
        Returns:
            float: 权重分数
        """
        # 基础权重
        weight = 1.0
        
        # 错误次数权重
        weight += word.error_count * 0.5
            
        return weight

    @staticmethod
    def get_weighted_random_word() -> Tuple[Optional[Word], List[str]]:
        """
        根据权重随机选择一个单词进行测试
        
        Returns:
            Tuple[Optional[Word], List[str]]: 
                - 选中的单词实例或None
                - 打乱顺序的翻译选项列表
        """
        words = WordService.get_all_words()
        if not words:
            return None, []
            
        # 计算每个单词的权重
        weighted_words = [(word, WordService.calculate_word_weight(word)) for word in words]
        
        # 计算总权重
        total_weight = sum(weight for _, weight in weighted_words)
        
        # 随机选择一个单词
        r = random.uniform(0, total_weight)
        current_weight = 0
        
        for word, weight in weighted_words:
            current_weight += weight
            if r <= current_weight:
                # 准备翻译选项
                translations = [
                    word.correct_translation,
                    word.wrong_translation_1,
                    word.wrong_translation_2,
                    word.wrong_translation_3
                ]
                random.shuffle(translations)
                return word, translations
                
        # 如果没有选中（理论上不会发生），返回随机一个
        word = random.choice(words)
        translations = [
            word.correct_translation,
            word.wrong_translation_1,
            word.wrong_translation_2,
            word.wrong_translation_3
        ]
        random.shuffle(translations)
        return word, translations
