from datetime import datetime, timezone
from app import db

class Word(db.Model):
    """单词模型类"""
    __tablename__ = 'words'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, index=True, comment='英文单词')
    part_of_speech = db.Column(db.String(50), nullable=False, comment='词性')
    correct_translation = db.Column(db.String(200), nullable=False, comment='正确翻译')
    wrong_translation_1 = db.Column(db.String(200), nullable=False, comment='错误翻译1')
    wrong_translation_2 = db.Column(db.String(200), nullable=False, comment='错误翻译2')
    wrong_translation_3 = db.Column(db.String(200), nullable=False, comment='错误翻译3')
    error_count = db.Column(db.Integer, default=0, comment='错误次数')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), comment='更新时间')

    def to_dict(self):
        """
        将模型转换为字典
        
        Returns:
            dict: 包含模型数据的字典
        """
        return {
            'id': self.id,
            'word': self.word,
            'part_of_speech': self.part_of_speech,
            'correct_translation': self.correct_translation,
            'wrong_translation_1': self.wrong_translation_1,
            'wrong_translation_2': self.wrong_translation_2,
            'wrong_translation_3': self.wrong_translation_3,
            'error_count': self.error_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Word {self.word}>'
