"""
Visualizer Module
Chart generation for customer service data analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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

def generate_charts_without_reply_length(df, trimmed_counts):
    """
    Generate comprehensive visualization charts (without reply length analysis)
    
    Args:
        df (pd.DataFrame): Customer service data with intent classification
        trimmed_counts (pd.Series): User query counts with outliers removed
        
    Returns:
        str: Path to generated chart file
    """
    # Set up fonts
    setup_chinese_fonts()
    
    # Create figure with subplots (2x2 instead of 2x3)
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('智能客服数据分析报告', fontsize=20, fontweight='bold')
    
    # 1. Intent classification pie chart
    if '新意图v2' in df.columns:
        intent_counts = df['新意图v2'].value_counts()
        top_intents = intent_counts.head(6)
        other_count = intent_counts.iloc[6:].sum()
        if other_count > 0:
            top_intents['其他'] = other_count
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        axes[0, 0].pie(top_intents.values, labels=top_intents.index, autopct='%1.1f%%', 
                       startangle=90, colors=colors[:len(top_intents)])
        axes[0, 0].set_title('用户问题分类占比', fontsize=14, fontweight='bold')
    else:
        axes[0, 0].text(0.5, 0.5, '无意图分类数据', ha='center', va='center', transform=axes[0, 0].transAxes)
        axes[0, 0].set_title('用户问题分类占比', fontsize=14, fontweight='bold')
    
    # 2. User query distribution
    query_dist = trimmed_counts.value_counts().sort_index()
    bars = axes[0, 1].bar(query_dist.index.astype(str), query_dist.values, 
                        color='skyblue', edgecolor='navy', alpha=0.7)
    axes[0, 1].set_title('用户咨询次数分布（去极值）', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('咨询次数')
    axes[0, 1].set_ylabel('用户数')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom')
    
    # 3. Hourly distribution
    df['小时'] = df['创建时间'].dt.hour
    hourly_counts = df['小时'].value_counts().sort_index()
    axes[1, 0].plot(hourly_counts.index, hourly_counts.values, marker='o', 
                    linewidth=2, markersize=6, color='red')
    axes[1, 0].set_title('24小时咨询量分布', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('小时')
    axes[1, 0].set_ylabel('咨询次数')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_xticks(range(24))
    
    # 4. Daily trend
    df['日期'] = df['创建时间'].dt.date
    daily_counts = df['日期'].value_counts().sort_index()
    axes[1, 1].plot(daily_counts.index, daily_counts.values, marker='s', 
                    linewidth=2, markersize=4, color='green')
    axes[1, 1].set_title('每日咨询量趋势', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('日期')
    axes[1, 1].set_ylabel('咨询次数')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save chart
    chart_filename = '客服数据分析图表.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return chart_filename

def generate_charts(df, trimmed_counts):
    """
    Generate comprehensive visualization charts
    
    Args:
        df (pd.DataFrame): Customer service data with intent classification
        trimmed_counts (pd.Series): User query counts with outliers removed
        
    Returns:
        str: Path to generated chart file
    """
    # Set up fonts
    setup_chinese_fonts()
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('智能客服数据分析报告', fontsize=20, fontweight='bold')
    
    # 1. Intent classification pie chart
    if '新意图v2' in df.columns:
        intent_counts = df['新意图v2'].value_counts()
        top_intents = intent_counts.head(6)
        other_count = intent_counts.iloc[6:].sum()
        if other_count > 0:
            top_intents['其他'] = other_count
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        axes[0, 0].pie(top_intents.values, labels=top_intents.index, autopct='%1.1f%%', 
                       startangle=90, colors=colors[:len(top_intents)])
        axes[0, 0].set_title('用户问题分类占比', fontsize=14, fontweight='bold')
    else:
        axes[0, 0].text(0.5, 0.5, '无意图分类数据', ha='center', va='center', transform=axes[0, 0].transAxes)
        axes[0, 0].set_title('用户问题分类占比', fontsize=14, fontweight='bold')
    
    # 2. User query distribution
    query_dist = trimmed_counts.value_counts().sort_index()
    bars = axes[0, 1].bar(query_dist.index.astype(str), query_dist.values, 
                        color='skyblue', edgecolor='navy', alpha=0.7)
    axes[0, 1].set_title('用户咨询次数分布（去极值）', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('咨询次数')
    axes[0, 1].set_ylabel('用户数')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom')
    
    # 3. Hourly distribution
    df['小时'] = df['创建时间'].dt.hour
    hourly_counts = df['小时'].value_counts().sort_index()
    axes[0, 2].plot(hourly_counts.index, hourly_counts.values, marker='o', 
                    linewidth=2, markersize=6, color='red')
    axes[0, 2].set_title('24小时咨询量分布', fontsize=14, fontweight='bold')
    axes[0, 2].set_xlabel('小时')
    axes[0, 2].set_ylabel('咨询次数')
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].set_xticks(range(24))
    
    # 4. Daily trend
    df['日期'] = df['创建时间'].dt.date
    daily_counts = df['日期'].value_counts().sort_index()
    axes[1, 0].plot(daily_counts.index, daily_counts.values, marker='s', 
                    linewidth=2, markersize=4, color='green')
    axes[1, 0].set_title('每日咨询量趋势', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('日期')
    axes[1, 0].set_ylabel('咨询次数')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 5. Weekly distribution
    df['星期几'] = df['创建时间'].dt.day_name()
    weekly_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_counts = df['星期几'].value_counts().reindex(weekly_order)
    bars = axes[1, 1].bar(range(len(weekly_counts)), weekly_counts.values, 
                        color='lightcoral', edgecolor='darkred', alpha=0.7)
    axes[1, 1].set_title('每周咨询量分布', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('星期')
    axes[1, 1].set_ylabel('咨询次数')
    axes[1, 1].set_xticks(range(len(weekly_counts)))
    axes[1, 1].set_xticklabels(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom')
    
    # 6. Reply length distribution
    df['回复长度'] = df['回复'].str.len()
    axes[1, 2].hist(df['回复长度'], bins=20, color='mediumpurple', 
                    edgecolor='purple', alpha=0.7)
    axes[1, 2].set_title('客服回复长度分布', fontsize=14, fontweight='bold')
    axes[1, 2].set_xlabel('回复字符数')
    axes[1, 2].set_ylabel('频次')
    axes[1, 2].grid(True, alpha=0.3)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save chart
    chart_filename = '客服数据分析图表.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return chart_filename

def create_intent_trend_chart(df):
    """
    Create a trend chart showing intent distribution over time
    
    Args:
        df (pd.DataFrame): Customer service data with intent and time columns
        
    Returns:
        str: Path to generated trend chart
    """
    setup_chinese_fonts()
    
    # Prepare data
    df['日期'] = df['创建时间'].dt.date
    df['星期几'] = df['创建时间'].dt.day_name()
    
    if '新意图v2' not in df.columns:
        return None
    
    # Create intent trends over time
    intent_time = df.groupby(['日期', '新意图v2']).size().unstack(fill_value=0)
    
    # Create stacked area chart
    fig, ax = plt.subplots(figsize=(15, 8))
    intent_time.plot(kind='area', stacked=True, ax=ax, alpha=0.7)
    
    ax.set_title('用户意图趋势分析', fontsize=16, fontweight='bold')
    ax.set_xlabel('日期')
    ax.set_ylabel('咨询次数')
    ax.legend(title='意图分类', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save chart
    trend_filename = '意图趋势分析.png'
    plt.savefig(trend_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return trend_filename