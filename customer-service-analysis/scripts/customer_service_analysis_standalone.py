#!/usr/bin/env python3
"""
Customer Service Analysis - Standalone Script
Complete analysis for customer service data with all components integrated
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import matplotlib.font_manager as fm
import os
import sys

def setup_chinese_fonts():
    """Set up Chinese fonts for proper text display"""
    try:
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
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 10

def classify_fitness_intent(question):
    """Classify customer questions into fitness center intent categories"""
    question = str(question).lower().strip()
    
    if any(keyword in question for keyword in ['月卡', '周卡', '年卡', '卡', '办理', '退款', '使用', '规则', '多人', '停卡', '续费', '绑定']):
        return '会员卡服务'
    elif any(keyword in question for keyword in ['器械', '哑铃', '跑步机', '史密斯', '插片式', '自行车', '卷腹机器', '卡扣']):
        return '器械使用'
    elif any(keyword in question for keyword in ['淋浴', '卫生间', '更衣室', '放衣服', '篮子', '饮水', '洗澡']):
        return '基础配套'
    elif any(keyword in question for keyword in ['空调', '温度', '热', '冷']):
        return '环境控制'
    elif any(keyword in question for keyword in ['遗失', '丢失', '东西', '物品', '拉在店里', '丢在店里', '落在店里']):
        return '物品遗失'
    elif any(keyword in question for keyword in ['扫码', '入场', '进店', '进去', '参观']):
        return '入场服务'
    elif any(keyword in question for keyword in ['营业时间', '几点']):
        return '营业服务'
    elif any(keyword in question for keyword in ['团购券', '美团', '大众点评']):
        return '支付相关'
    elif any(keyword in question for keyword in ['人工客服', '人工', '投诉', '投诉建议', '报修']):
        return '客服需求'
    elif any(keyword in question for keyword in ['投屏', '电视', '网络', 'wifi', '停电', 'keep']):
        return '技术问题'
    elif any(keyword in question for keyword in ['你好', '在吗', '聊天', '哈哈', '呵呵']):
        return '闲聊互动'
    else:
        return '其他咨询'

def prepare_data(excel_file_path):
    """Read and prepare customer service data"""
    df = pd.read_excel(excel_file_path)
    
    # Check required columns
    required_columns = ['创建时间', '问题', '回复', '用户']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Clean data
    df['创建时间'] = pd.to_datetime(df['创建时间'])
    df['问题'] = df['问题'].fillna('')
    df['回复'] = df['回复'].fillna('')
    df['用户'] = df['用户'].fillna('Unknown')
    
    # Remove empty rows
    df = df[(df['问题'].str.strip() != '') & (df['回复'].str.strip() != '')]
    df = df.sort_values(by='创建时间')
    
    return df

def generate_charts(df, trimmed_counts):
    """Generate comprehensive visualization charts"""
    setup_chinese_fonts()
    
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
    
    plt.tight_layout()
    
    chart_filename = '客服数据分析图表.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return chart_filename

def generate_report(df, trimmed_counts):
    """Generate comprehensive text report"""
    user_query_counts = df['用户'].value_counts()
    total_users = len(user_query_counts)
    total_queries = len(df)
    avg_queries = user_query_counts.mean()
    
    df['小时'] = df['创建时间'].dt.hour
    peak_hour = df['小时'].value_counts().idxmax()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Start building report content
    report_content = "# 智能客服数据分析报告\n\n"
    report_content += f"**生成时间**: {timestamp}\n"
    report_content += f"**数据周期**: {df['创建时间'].min().strftime('%Y-%m-%d')} 至 {df['创建时间'].max().strftime('%Y-%m-%d')}\n\n"
    report_content += "---\n\n"
    report_content += "## 执行摘要\n\n"
    report_content += "### 数据概览\n"
    report_content += f"- **总用户数**: {total_users:,} 人\n"
    report_content += f"- **总咨询量**: {total_queries:,} 次\n"
    report_content += f"- **人均咨询**: {avg_queries:.1f} 次\n"
    report_content += f"- **高峰时段**: {peak_hour}:00 点咨询量最高\n\n"
    
    if '新意图v2' in df.columns:
        intent_counts = df['新意图v2'].value_counts()
        top_intent = intent_counts.index[0]
        top_percentage = (intent_counts.iloc[0] / total_queries) * 100
        report_content += f"- **主要需求**: {top_intent} 占比 {top_percentage:.1f}%\n\n"
        
        report_content += "## 用户意图分析\n\n"
        report_content += "### 意图分类统计\n\n"
        report_content += "| 排名 | 意图分类 | 咨询次数 | 占比 |\n"
        report_content += "|------|----------|----------|------|\n"
        
        for rank, (intent, count) in enumerate(intent_counts.items(), 1):
            percentage = (count / total_queries) * 100
            report_content += f"| {rank} | {intent} | {count:,} | {percentage:.1f}% |\n"
    
    report_content += "\n## 用户行为分析\n\n"
    report_content += "### 用户咨询分布（已去除极值）\n"
    report_content += f"- **分析用户数**: {len(trimmed_counts):,} 人\n"
    report_content += f"- **平均咨询次数**: {trimmed_counts.mean():.1f} 次\n"
    report_content += f"- **中位数咨询次数**: {trimmed_counts.median():.1f} 次\n"
    report_content += f"- **最高咨询次数**: {trimmed_counts.max()} 次\n\n"
    
    report_content += "### 用户分层\n"
    one_time_users = (trimmed_counts == 1).sum()
    repeat_users = (trimmed_counts > 1).sum()
    report_content += f"- **一次性用户**: {one_time_users} 人 ({one_time_users/len(trimmed_counts)*100:.1f}%)\n"
    report_content += f"- **重复咨询用户**: {repeat_users} 人 ({repeat_users/len(trimmed_counts)*100:.1f}%)\n\n"
    
    report_content += "## 时间模式分析\n\n"
    report_content += "### 24小时分布\n"
    report_content += f"- **咨询高峰**: {peak_hour}:00 点\n\n"
    
    report_content += "### 每周分布\n"
    df['星期几'] = df['创建时间'].dt.day_name()
    weekday_mask = df['星期几'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    weekday_count = df[weekday_mask].shape[0]
    weekend_count = df[~weekday_mask].shape[0]
    report_content += f"- **工作日咨询**: {weekday_count:,} 次 ({weekday_count/(weekday_count+weekend_count)*100:.1f}%)\n"
    report_content += f"- **周末咨询**: {weekend_count:,} 次 ({weekend_count/(weekday_count+weekend_count)*100:.1f}%)\n\n"
    
    report_content += "## 运营建议\n\n"
    report_content += "### 人员配置建议\n"
    report_content += f"1. **高峰时段加强**: 在 {peak_hour}:00 点左右增加客服人员配置\n\n"
    
    report_content += "### 内容优化建议\n"
    report_content += "1. **重点问题知识库**: 完善高频问题的FAQ和自动回复\n\n"
    
    report_content += "### 服务改进建议\n"
    report_content += "1. **响应时长优化**: 分析不同时段的响应时长\n"
    report_content += "2. **用户分层服务**: 为高频用户提供差异化服务策略\n\n"
    
    report_content += "---\n\n"
    report_content += "## 附录\n\n"
    report_content += "### 数据处理说明\n"
    report_content += "- 数据已清洗，移除了空值和无效记录\n"
    report_content += "- 用户咨询次数分析已去除最高和最低极值\n"
    report_content += "- 意图分类基于关键词匹配算法\n"
    
    report_filename = '智能客服数据分析报告.md'
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return report_filename

def analyze_customer_service_data(excel_file_path):
    """Main analysis function"""
    print(f"🚀 Starting customer service analysis for: {excel_file_path}")
    
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Excel file not found: {excel_file_path}")
    
    try:
        # Read and prepare data
        print("📊 Reading and preparing data...")
        df = prepare_data(excel_file_path)
        
        # Apply intent classification
        print("🏷️  Classifying user intents...")
        df['新意图v2'] = df['问题'].apply(classify_fitness_intent)
        
        # User analysis with outlier removal
        print("👥 Analyzing user behavior patterns...")
        user_query_counts = df['用户'].value_counts()
        sorted_counts = user_query_counts.sort_values()
        
        if len(sorted_counts) > 2:
            trimmed_counts = sorted_counts.iloc[1:-1]
        else:
            trimmed_counts = sorted_counts
        
        # Generate charts
        print("📈 Generating visualization charts...")
        chart_file = generate_charts(df, trimmed_counts)
        
        # Generate report
        print("📝 Generating text report...")
        report_file = generate_report(df, trimmed_counts)
        
        print("✅ Analysis complete!")
        print(f"📊 Text report: {report_file}")
        print(f"📈 Charts: {chart_file}")
        
        return {
            'text_report': report_file,
            'chart_file': chart_file
        }
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        raise

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python customer_service_analysis_standalone.py <excel_file_path>")
        print("Example: python customer_service_analysis_standalone.py ./data/customer_service.xlsx")
        sys.exit(1)
    
    excel_file_path = sys.argv[1]
    
    try:
        result = analyze_customer_service_data(excel_file_path)
        print(f"\n🎉 Analysis completed successfully!")
        print(f"📄 Report: {result['text_report']}")
        print(f"📊 Charts: {result['chart_file']}")
        
    except Exception as e:
        print(f"\n💥 Analysis failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()