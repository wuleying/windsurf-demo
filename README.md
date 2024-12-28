# 英语单词学习系统

这是一个基于 Flask 框架开发的英语单词学习系统，帮助用户更好地记忆和掌握英语单词。

## 功能特性

1. 单词管理
   - 单词录入：支持录入英文单词、词性、正确中文翻译及三个错误翻译选项
   - 单词编辑：修改已录入的单词信息
   - 单词删除：支持单条或批量删除单词

2. 学习功能
   - 单词测试：随机展示单词，用户从四个中文翻译中选择正确答案
   - 错误统计：记录用户答题错误次数
   - 易错词复习：针对性展示高频错误单词，帮助巩固学习

3. 数据展示
   - 首页展示易错单词列表
   - 按错误次数排序展示
   - 清晰展示每个单词的出错频率

## 技术栈

- 后端框架：Flask
- 数据库：MySQL 5.7
- Python版本：3.11

## 项目结构

```
windsurf-demo/
├── app/                    # 应用主目录
│   ├── models/            # 数据模型
│   ├── routes/            # 路由控制器
│   ├── services/          # 业务逻辑层
│   ├── templates/         # 前端模板
│   └── static/            # 静态资源
├── tests/                 # 单元测试
├── config.py              # 配置文件
└── requirements.txt       # 项目依赖
```

## 开发规范

- 遵循 PEP 8 Python代码规范
- 使用中文注释，保证代码可读性
- 实现完整的单元测试
- 采用 RESTful API 设计规范

## 数据库设计

### words 表
- id: 主键
- word: 英文单词
- part_of_speech: 词性
- correct_translation: 正确翻译
- wrong_translation_1: 错误翻译1
- wrong_translation_2: 错误翻译2
- wrong_translation_3: 错误翻译3
- error_count: 错误次数
- created_at: 创建时间
- updated_at: 更新时间

## 安装和运行

1. 克隆项目
```bash
git clone https://github.com/wuleying/windsurf-demo.git
cd windsurf-demo
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置数据库
```bash
# 配置 MySQL 连接信息
编辑 config.py 文件
```

4. 运行项目
```bash
python run.py
```

## 测试

运行单元测试：
```bash
python -m pytest tests/
``` 
