from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from app.services.word_service import WordService
import random

word_bp = Blueprint('word', __name__)

@word_bp.route('/')
def index():
    """首页"""
    error_prone_words = WordService.get_error_prone_words(10)
    return render_template('index.html', error_prone_words=error_prone_words)

@word_bp.route('/words')
def word_list():
    """单词列表页面"""
    words = WordService.get_all_words()
    return render_template('word_list.html', words=words)

@word_bp.route('/words/add', methods=['GET'])
def add_word():
    """添加单词页面"""
    return render_template('word_form.html')

@word_bp.route('/words/<int:word_id>/edit', methods=['GET'])
def edit_word(word_id):
    """编辑单词页面"""
    word = WordService.get_word_by_id(word_id)
    if not word:
        flash('单词不存在', 'danger')
        return redirect(url_for('word.word_list'))
    return render_template('word_form.html', word=word)

@word_bp.route('/test')
def test():
    """单词测试页面"""
    # 获取所有单词
    words = WordService.get_all_words()
    if not words:
        return render_template('test.html')
    
    # 随机选择一个单词
    word = random.choice(words)
    
    # 准备翻译选项（1个正确答案和3个错误答案）
    translations = [
        word.correct_translation,
        word.wrong_translation_1,
        word.wrong_translation_2,
        word.wrong_translation_3
    ]
    # 随机打乱顺序
    random.shuffle(translations)
    
    return render_template('test.html', word=word, translations=translations)

# API 路由
@word_bp.route('/api/words/', methods=['GET'])
def get_words():
    """获取所有单词"""
    words = WordService.get_all_words()
    return jsonify([word.to_dict() for word in words])

@word_bp.route('/api/words/error-prone', methods=['GET'])
def get_error_prone_words():
    """获取易错单词"""
    limit = request.args.get('limit', 10, type=int)
    words = WordService.get_error_prone_words(limit)
    return jsonify([word.to_dict() for word in words])

@word_bp.route('/api/words/<int:word_id>', methods=['GET'])
def get_word(word_id):
    """获取单个单词"""
    word = WordService.get_word_by_id(word_id)
    if word:
        return jsonify(word.to_dict())
    return jsonify({'error': '单词不存在'}), 404

@word_bp.route('/api/words/', methods=['POST'])
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

@word_bp.route('/api/words/<int:word_id>', methods=['PUT'])
def update_word_api(word_id):
    """更新单词"""
    data = request.get_json()
    word = WordService.update_word(word_id, data)
    if word:
        return jsonify(word.to_dict())
    return jsonify({'error': '单词不存在'}), 404

@word_bp.route('/api/words/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    """删除单词"""
    success = WordService.delete_word(word_id)
    if success:
        return '', 204
    return jsonify({'error': '单词不存在'}), 404

@word_bp.route('/api/words/<int:word_id>/increment-error', methods=['POST'])
def increment_error_count(word_id):
    """增加单词错误次数"""
    word = WordService.increment_error_count(word_id)
    if word:
        return jsonify(word.to_dict())
    return jsonify({'error': '单词不存在'}), 404
