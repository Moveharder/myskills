#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unanswered Questions Analysis Module
用于分析无法回答的问题和场景分布
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import matplotlib.font_manager as fm

def setup_chinese_fonts():
    """Set up Chinese fonts for proper text display in matplotlib"""
    try:
        # Try different Chinese fonts in order of preference
        chinese_fonts = ['Hiragino Sans GB', 'STHeiti', 'Arial Unicode MS', 'SimHei', 'DejaVu Sans']
        
        for font in chinese_fonts:
            try:
                plt.rcParams['font.family'] = font
                plt.rcParams['axes.unicode_minus'] = False
                plt.rcParams['font.size'] = 10
                break
            except:
                continue
    except:
        # Fallback to default if Chinese fonts not available
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 10

def classify_question_intent(question):
    """对问题进行意图分类"""
    question = str(question).lower()
    
    # 意图分类关键词
    intent_keywords = {
        '会员卡服务': ['会员', '卡', '办理', '退卡', '续费', '年卡', '次卡', '押金'],
        '器械使用': ['器械', '器材', '设备', '跑步机', '哑铃', '杠铃', '健身器'],
        '基础配套': ['淋浴', '储物', '更衣', '洗手间', '卫生间', '毛巾', '吹风机'],
        '环境控制': ['空调', '温度', '音乐', '灯光', '通风', '暖气'],
        '物品遗失': ['丢失', '遗失', '捡到', '失物', '物品', '手机', '钱包'],
        '入场服务': ['进门', '入场', '登记', '二维码', '门禁', '刷脸'],
        '营业服务': ['营业时间', '开门', '关门', '时间', '营业'],
        '支付相关': ['支付', '付款', '退款', '收费', '价格', '费用', '微信', '支付宝'],
        '客服需求': ['客服', '人工', '电话', '联系', '投诉', '建议'],
        '技术问题': ['小程序', 'APP', '登录', '注册', '系统', '网络', '技术'],
        '闲聊互动': ['你好', '谢谢', '再见', '哈哈', '呵呵', '聊天'],
        '其他咨询': ['什么', '如何', '怎么', '为什么', '请问']
    }
    
    for intent, keywords in intent_keywords.items():
        if any(keyword in question for keyword in keywords):
            return intent
    
    return '其他咨询'

def analyze_unanswered_questions(df, unable_response_pattern="嘎嘎嘎，这个问题小鸭头不清楚，请拨打"):
    """
    分析无法回答的问题
    
    Args:
        df (pd.DataFrame): 客服数据
        unable_response_pattern (str): 无法回答的回复标识
        
    Returns:
        tuple: (汇总表格, 意图分布)
    """
    # 设置中文字体
    setup_chinese_fonts()
    
    # 筛选无法回答的问题
    mask = df['回复'].str.contains(unable_response_pattern, na=False)
    unable_to_answer = df[mask].copy()
    
    if len(unable_to_answer) == 0:
        print("未找到无法回答的问题记录")
        return None, None
    
    # 添加意图分类
    unable_to_answer['意图分类'] = unable_to_answer['问题'].apply(classify_question_intent)
    
    # 统计意图分布
    intent_counts = unable_to_answer['意图分类'].value_counts()
    
    # 创建汇总表格
    summary_table = unable_to_answer[['创建时间', '用户', '问题', '意图分类']].copy()
    summary_table['创建时间'] = pd.to_datetime(summary_table['创建时间'])
    summary_table['创建时间'] = summary_table['创建时间'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 保存汇总表格
    summary_table.to_excel('无法回答问题汇总表.xlsx', index=False, engine='openpyxl')
    
    return summary_table, intent_counts

def create_unanswered_questions_chart(intent_counts):
    """
    创建无法回答问题场景分布图
    
    Args:
        intent_counts (pd.Series): 意图分布统计
        
    Returns:
        str: 图表文件路径
    """
    setup_chinese_fonts()
    
    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('无法回答问题场景分布分析', fontsize=20, fontweight='bold')
    
    # 颜色方案
    colors = plt.colormaps.get_cmap('Set3')(np.linspace(0, 1, len(intent_counts)))
    
    # 1. 饼图
    axes[0, 0].pie(intent_counts.values, labels=intent_counts.index, 
                   autopct='%1.1f%%', colors=colors, startangle=90)
    axes[0, 0].set_title('无法回答问题意图分布', fontsize=14, fontweight='bold')
    
    # 2. 柱状图
    bars = axes[0, 1].bar(intent_counts.index, intent_counts.values, color=colors)
    axes[0, 1].set_title('无法回答问题意图频次', fontsize=14, fontweight='bold')
    axes[0, 1].set_xticks(range(len(intent_counts)))
    axes[0, 1].set_xticklabels(intent_counts.index, rotation=45, ha='right')
    axes[0, 1].set_ylabel('频次')
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom')
    
    # 3. 无法回答率分析
    total_unanswered = intent_counts.sum()
    labels = ['无法回答', '可回答']
    sizes = [total_unanswered, 98 - total_unanswered]  # 总共98条记录
    colors_rate = ['#FF6B6B', '#4ECDC4']
    
    axes[1, 0].pie(sizes, labels=labels, autopct='%1.1f%%', 
                   colors=colors_rate, startangle=90)
    axes[1, 0].set_title('问题可回答性分析', fontsize=14, fontweight='bold')
    
    # 4. 高频问题分析
    top_intents = intent_counts.head(5)
    bars = axes[1, 1].barh(range(len(top_intents)), top_intents.values, 
                           color='skyblue', edgecolor='navy', alpha=0.7)
    axes[1, 1].set_title('TOP 5 无法回答问题场景', fontsize=14, fontweight='bold')
    axes[1, 1].set_yticks(range(len(top_intents)))
    axes[1, 1].set_yticklabels(top_intents.index)
    axes[1, 1].set_xlabel('频次')
    
    # 添加数值标签
    for i, bar in enumerate(bars):
        width = bar.get_width()
        axes[1, 1].text(width, bar.get_y() + bar.get_height()/2.,
                       f'{int(width)}', ha='left', va='center')
    
    plt.tight_layout()
    
    # 保存图表
    chart_filename = '无法回答问题场景分布图.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return chart_filename

def generate_unanswered_report(summary_table, intent_counts):
    """
    生成无法回答问题分析报告
    
    Args:
        summary_table (pd.DataFrame): 汇总表格
        intent_counts (pd.Series): 意图分布
        
    Returns:
        str: 报告文件路径
    """
    total_unanswered = len(summary_table)
    total_questions = 98  # 总问题数
    unanswered_rate = total_unanswered / total_questions * 100
    unique_users = summary_table['用户'].nunique()
    
    report = f"""# 无法回答问题专项分析报告

## 1. 概述
- **无法回答问题总数**: {total_unanswered} 个
- **无法回答率**: {unanswered_rate:.1f}%
- **涉及用户数**: {unique_users} 人
- **占总咨询比例**: {unanswered_rate:.1f}%

## 2. 问题场景分布分析

### 意图分布统计
"""
    
    for intent, count in intent_counts.items():
        percentage = count / total_unanswered * 100
        report += f"- **{intent}**: {count}个 ({percentage:.1f}%)\n"
    
    report += f"""
### 主要发现
1. **最常见无法回答场景**: {intent_counts.index[0]} ({intent_counts.iloc[0]}个)
2. **无法回答率**: {unanswered_rate:.1f}%，{'处于较高水平' if unanswered_rate > 10 else '处于可接受范围'}
3. **知识覆盖不足**: 以下场景需要补充知识库内容

## 3. 详细问题列表
| 时间 | 用户 | 问题 | 意图分类 |
|------|------|------|----------|
"""
    
    # 添加详细问题列表（只显示前20个）
    for idx, row in summary_table.head(20).iterrows():
        report += f"| {row['创建时间']} | {row['用户']} | {row['问题'][:50]}... | {row['意图分类']} |\n"
    
    report += f"""
## 4. 改进建议

### 紧急优化措施
1. **补充知识库**: 针对{intent_counts.index[0]}等高频场景添加标准回复
2. **培训优化**: 加强客服对{intent_counts.index[0]}业务的理解和回复能力
3. **转接流程**: 建立{intent_counts.index[0]}问题的专家转接机制

### 长期改进计划  
1. **智能识别**: 开发自动识别可能无法回答问题的预警机制
2. **知识管理**: 建立动态知识库更新和维护流程
3. **质量监控**: 定期分析和监控无法回答问题的趋势变化

### 具体行动项
- [ ] 完善知识库{intent_counts.index[0]}相关条目
- [ ] 组织客服{intent_counts.index[0]}场景培训
- [ ] 建立无法回答问题周报机制
- [ ] 优化问题转接和处理流程

---
报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
数据周期: 2026-01-13 至 2026-02-11
"""
    
    # 保存报告
    report_filename = '无法回答问题分析报告.md'
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_filename

def run_unanswered_analysis(excel_file):
    """
    运行完整的无法回答问题分析
    
    Args:
        excel_file (str): Excel文件路径
        
    Returns:
        dict: 分析结果文件路径
    """
    print("=== 无法回答问题分析开始 ===")
    
    # 读取数据
    df = pd.read_excel(excel_file)
    df['创建时间'] = pd.to_datetime(df['创建时间'])
    
    # 分析无法回答的问题
    summary_table, intent_counts = analyze_unanswered_questions(df)
    
    if summary_table is None:
        return None
    
    # 创建图表
    chart_file = create_unanswered_questions_chart(intent_counts)
    
    # 生成报告
    report_file = generate_unanswered_report(summary_table, intent_counts)
    
    print(f"✅ 汇总表格: 无法回答问题汇总表.xlsx")
    print(f"✅ 分析图表: {chart_file}")
    print(f"✅ 详细报告: {report_file}")
    print("=== 无法回答问题分析完成 ===")
    
    return {
        'summary_table': '无法回答问题汇总表.xlsx',
        'chart': chart_file,
        'report': report_file
    }