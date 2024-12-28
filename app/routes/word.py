from flask import Blueprint, jsonify, request
from app.services.word_service import WordService

word_bp = Blueprint('word', __name__, url_prefix='/api/words')

@word_bp.route('/', methods=['GET'])
def get_words():
    """获取所有单词"""
    words = WordService.get_all_words()
    return jsonify([word.to_dict() for word in words])

@word_bp.route('/error-prone', methods=['GET'])
def get_error_prone_words():
    """获取易错单词"""
    limit = request.args.get('limit', 10, type=int)
    words = WordService.get_error_prone_words(limit)
    return jsonify([word.to_dict() for word in words])

@word_bp.route('/<int:word_id>', methods=['GET'])
def get_word(word_id):
    """获取单个单词"""
    word = WordService.get_word_by_id(word_id)
    if word:
        return jsonify(word.to_dict())
    return jsonify({'error': '单词不存在'}), 404

@word_bp.route('/', methods=['POST'])
def create_word():
    """创建新单词"""
    data = request.get_json()
    required_fields = ['word', 'part_of_speech', 'correct_translation',
                      'wrong_translation_1', 'wrong_translation_2', 'wrong_translation_3']
    
    # 验证必填字段
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    word = WordService.create_word(data)
    return jsonify(word.to_dict()), 201

@word_bp.route('/<int:word_id>', methods=['PUT'])
def update_word(word_id):
    """更新单词"""
    data = request.get_json()
    word = WordService.update_word(word_id, data)
    if word:
        return jsonify(word.to_dict())
    return jsonify({'error': '单词不存在'}), 404

@word_bp.route('/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    """删除单词"""
    success = WordService.delete_word(word_id)
    if success:
        return '', 204
    return jsonify({'error': '单词不存在'}), 404

@word_bp.route('/<int:word_id>/increment-error', methods=['POST'])
def increment_error_count(word_id):
    """增加单词错误次数"""
    word = WordService.increment_error_count(word_id)
    if word:
        return jsonify(word.to_dict())
    return jsonify({'error': '单词不存在'}), 404
