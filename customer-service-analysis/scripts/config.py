"""
Configuration Module
Central configuration for customer service analysis
"""

# Industry configuration
INDUSTRY = "fitness"

# Chart styling configuration
CHART_CONFIG = {
    'figure_size': (18, 12),
    'dpi': 300,
    'font_size': 10,
    'title_font_size': 20,
    'subtitle_font_size': 14
}

# Analysis parameters
ANALYSIS_CONFIG = {
    'outlier_removal': True,
    'top_intents_display': 6,
    'min_queries_for_analysis': 10
}

# File naming conventions
OUTPUT_FILES = {
    'chart': '客服数据分析图表.png',
    'report': '智能客服数据分析报告.md',
    'trend_chart': '意图趋势分析.png'
}

# Intent categories for fitness center
FITNESS_INTENTS = [
    '会员卡服务',
    '器械使用', 
    '基础配套',
    '环境控制',
    '物品遗失',
    '入场服务',
    '营业服务',
    '支付相关',
    '客服需求',
    '技术问题',
    '闲聊互动',
    '其他咨询'
]

# Color scheme for charts
COLOR_SCHEME = [
    '#FF6B6B',  # Red
    '#4ECDC4',  # Teal
    '#45B7D1',  # Blue
    '#96CEB4',  # Green
    '#FFEAA7',  # Yellow
    '#DDA0DD',  # Purple
    '#FFA07A',  # Light Salmon
    '#98D8C8',  # Mint
    '#F7DC6F',  # Yellow
    '#BB8FCE',  # Light Purple
    '#85C1E2',  # Light Blue
    '#F8B739'   # Orange
]

# Time analysis settings
TIME_CONFIG = {
    'business_hours_start': 9,
    'business_hours_end': 18,
    'evening_hours_start': 18,
    'evening_hours_end': 22
}