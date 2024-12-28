from typing import List, Dict, Optional
from app import db
from app.models.word import Word

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
