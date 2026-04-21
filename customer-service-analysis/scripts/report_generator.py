"""
Report Generator Module
Generate comprehensive text reports for customer service analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
from data_processor import calculate_user_metrics, calculate_time_metrics, calculate_intent_metrics

def generate_executive_summary(df, user_metrics, time_metrics, intent_metrics):
    """
    Generate executive summary of the analysis
    
    Args:
        df (pd.DataFrame): Customer service data
        user_metrics (dict): User behavior metrics
        time_metrics (dict): Time-based metrics
        intent_metrics (dict): Intent distribution metrics
        
    Returns:
        str: Executive summary text
    """
    total_users = user_metrics['total_users']
    total_queries = user_metrics['total_queries']
    avg_queries = user_metrics['avg_queries_per_user']
    analysis_period = time_metrics['analysis_period_days']
    
    summary = f"""## 执行摘要

### 数据概览
- **分析周期**: {analysis_period} 天
- **总用户数**: {total_users:,} 人
- **总咨询量**: {total_queries:,} 次
- **人均咨询**: {avg_queries:.1f} 次

### 关键发现
"""
    
    if intent_metrics:
        top_intent = intent_metrics['top_intent']
        top_intent_pct = intent_metrics['top_intent_percentage']
        summary += f"- **主要需求**: {top_intent} 占比 {top_intent_pct:.1f}%\n"
    
    peak_hour = time_metrics['peak_hour']
    weekday_ratio = time_metrics['weekday_ratio']
    summary += f"- **高峰时段**: {peak_hour}:00 点咨询量最高\n"
    summary += f"- **工作日咨询**: 占比 {weekday_ratio*100:.1f}%\n"
    
    return summary

def generate_intent_analysis(df):
    """
    Generate detailed intent analysis
    
    Args:
        df (pd.DataFrame): Customer service data with intent classification
        
    Returns:
        str: Intent analysis text
    """
    if '新意图v2' not in df.columns:
        return "## 意图分析\n\n无意图分类数据。\n"
    
    intent_counts = df['新意图v2'].value_counts()
    total_queries = len(df)
    
    analysis = "## 用户意图分析\n\n"
    analysis += "### 意图分类统计\n\n"
    analysis += "| 排名 | 意图分类 | 咨询次数 | 占比 |\n"
    analysis += "|------|----------|----------|------|\n"
    
    for rank, (intent, count) in enumerate(intent_counts.items(), 1):
        percentage = (count / total_queries) * 100
        analysis += f"| {rank} | {intent} | {count:,} | {percentage:.1f}% |\n"
    
    analysis += "\n### 意图分析洞察\n\n"
    
    # Top 3 insights
    top_intent = intent_counts.index[0]
    top_percentage = (intent_counts.iloc[0] / total_queries) * 100
    
    analysis += f"1. **主要需求**: '{top_intent}' 是最主要的用户需求，占比 {top_percentage:.1f}%\n"
    
    if len(intent_counts) >= 2:
        second_intent = intent_counts.index[1]
        second_percentage = (intent_counts.iloc[1] / total_queries) * 100
        analysis += f"2. **次要需求**: '{second_intent}' 占比 {second_percentage:.1f}%\n"
    
    # Long tail analysis
    long_tail_count = len(intent_counts) - 3
    if long_tail_count > 0:
        long_tail_percentage = (intent_counts.iloc[3:].sum() / total_queries) * 100
        analysis += f"3. **长尾需求**: 剩余 {long_tail_count} 类意图合计占比 {long_tail_percentage:.1f}%\n"
    
    return analysis

def generate_user_behavior_analysis(trimmed_counts):
    """
    Generate user behavior analysis
    
    Args:
        trimmed_counts (pd.Series): User query counts with outliers removed
        
    Returns:
        str: User behavior analysis text
    """
    analysis = "## 用户行为分析\n\n"
    
    # Statistics
    total_users = len(trimmed_counts)
    mean_queries = trimmed_counts.mean()
    median_queries = trimmed_counts.median()
    max_queries = trimmed_counts.max()
    
    analysis += f"### 用户咨询分布（已去除极值）\n\n"
    analysis += f"- **分析用户数**: {total_users:,} 人\n"
    analysis += f"- **平均咨询次数**: {mean_queries:.1f} 次\n"
    analysis += f"- **中位数咨询次数**: {median_queries:.1f} 次\n"
    analysis += f"- **最高咨询次数**: {max_queries} 次\n"
    
    # User segments
    one_time_users = (trimmed_counts == 1).sum()
    repeat_users = (trimmed_counts > 1).sum()
    
    analysis += f"\n### 用户分层\n\n"
    analysis += f"- **一次性用户**: {one_time_users} 人 ({one_time_users/total_users*100:.1f}%)\n"
    analysis += f"- **重复咨询用户**: {repeat_users} 人 ({repeat_users/total_users*100:.1f}%)\n"
    
    # Engagement analysis
    if repeat_users > 0:
        high_engagement = (trimmed_counts >= 5).sum()
        analysis += f"- **高频用户** (≥5次): {high_engagement} 人 ({high_engagement/total_users*100:.1f}%)\n"
    
    return analysis

def generate_time_pattern_analysis(df):
    """
    Generate time-based pattern analysis
    
    Args:
        df (pd.DataFrame): Customer service data with time columns
        
    Returns:
        str: Time pattern analysis text
    """
    analysis = "## 时间模式分析\n\n"
    
    # Hourly patterns
    df['小时'] = df['创建时间'].dt.hour
    hourly_counts = df['小时'].value_counts().sort_index()
    peak_hour = hourly_counts.idxmax()
    peak_hour_count = hourly_counts.max()
    
    analysis += f"### 24小时分布\n\n"
    analysis += f"- **咨询高峰**: {peak_hour}:00 点，咨询量 {peak_hour_count:,} 次\n"
    
    # Business hours analysis (9:00-18:00)
    business_hours = df[(df['小时'] >= 9) & (df['小时'] <= 18)]
    business_percentage = len(business_hours) / len(df) * 100
    analysis += f"- **工作时间咨询** (9:00-18:00): {business_percentage:.1f}%\n"
    
    # Evening hours (18:00-22:00)
    evening_hours = df[(df['小时'] >= 18) & (df['小时'] <= 22)]
    evening_percentage = len(evening_hours) / len(df) * 100
    analysis += f"- **晚间咨询** (18:00-22:00): {evening_percentage:.1f}%\n"
    
    # Weekly patterns
    df['星期几'] = df['创建时间'].dt.day_name()
    weekday_mask = df['星期几'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    weekend_mask = ~weekday_mask
    
    weekday_count = df[weekday_mask].shape[0]
    weekend_count = df[weekend_mask].shape[0]
    
    analysis += f"\n### 每周分布\n\n"
    analysis += f"- **工作日咨询**: {weekday_count:,} 次 ({weekday_count/(weekday_count+weekend_count)*100:.1f}%)\n"
    analysis += f"- **周末咨询**: {weekend_count:,} 次 ({weekend_count/(weekday_count+weekend_count)*100:.1f}%)\n"
    
    # Daily trend
    df['日期'] = df['创建时间'].dt.date
    daily_counts = df['日期'].value_counts().sort_index()
    
    if len(daily_counts) > 1:
        max_day_count = daily_counts.max()
        min_day_count = daily_counts.min()
        avg_day_count = daily_counts.mean()
        
        analysis += f"\n### 每日趋势\n\n"
        analysis += f"- **最高日咨询量**: {max_day_count:,} 次\n"
        analysis += f"- **最低日咨询量**: {min_day_count:,} 次\n"
        analysis += f"- **平均日咨询量**: {avg_day_count:.1f} 次\n"
    
    return analysis

def generate_operational_recommendations(df, intent_metrics, time_metrics):
    """
    Generate operational recommendations based on analysis
    
    Args:
        df (pd.DataFrame): Customer service data
        intent_metrics (dict): Intent distribution metrics
        time_metrics (dict): Time-based metrics
        
    Returns:
        str: Operational recommendations text
    """
    recommendations = "## 运营建议\n\n"
    
    # Staffing recommendations
    peak_hour = time_metrics['peak_hour']
    recommendations += f"### 人员配置建议\n\n"
    recommendations += f"1. **高峰时段加强**: 在 {peak_hour}:00 点左右增加客服人员配置\n"
    
    weekday_ratio = time_metrics['weekday_ratio']
    if weekday_ratio > 0.7:
        recommendations += "2. **工作日重点保障**: 工作日咨询量占比较高，确保工作日人员充足\n"
    else:
        recommendations += "2. **周末配置优化**: 周末咨询量占比较高，需加强周末人员安排\n"
    
    # Content recommendations
    if intent_metrics:
        top_intent = intent_metrics['top_intent']
        top_percentage = intent_metrics['top_intent_percentage']
        
        recommendations += f"\n### 内容优化建议\n\n"
        recommendations += f"1. **重点问题知识库**: 针对'{top_intent}'类问题（占比{top_percentage:.1f}%），完善FAQ和自动回复\n"
        
        if top_percentage > 40:
            recommendations += "2. **自动化优先**: 考虑为高频问题开发智能回复，提高处理效率\n"
    
    # Service improvement recommendations
    recommendations += f"\n### 服务改进建议\n\n"
    recommendations += "1. **响应时长优化**: 分析不同时段的响应时长，优化资源配置\n"
    recommendations += "2. **用户分层服务**: 为高频用户提供差异化服务策略\n"
    recommendations += "3. **主动服务**: 基于用户咨询模式，提供主动式服务\n"
    
    return recommendations

def generate_report_without_reply_length(df, trimmed_counts):
    """
    Generate comprehensive text report (without reply length analysis)
    
    Args:
        df (pd.DataFrame): Customer service data with intent classification
        trimmed_counts (pd.Series): User query counts with outliers removed
        
    Returns:
        str: Path to generated report file
    """
    # Calculate metrics
    user_metrics = calculate_user_metrics(df)
    time_metrics = calculate_time_metrics(df)
    intent_metrics = calculate_intent_metrics(df)
    
    # Generate report sections
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_content = f"""# 智能客服数据分析报告

**生成时间**: {timestamp}
**数据周期**: {df['创建时间'].min().strftime('%Y-%m-%d')} 至 {df['创建时间'].max().strftime('%Y-%m-%d')}

---

"""
    
    # Add all sections (except reply length)
    report_content += generate_executive_summary(df, user_metrics, time_metrics, intent_metrics)
    report_content += "\n\n"
    
    report_content += generate_intent_analysis(df)
    report_content += "\n\n"
    
    report_content += generate_user_behavior_analysis(trimmed_counts)
    report_content += "\n\n"
    
    report_content += generate_time_pattern_analysis(df)
    report_content += "\n\n"
    
    report_content += generate_operational_recommendations(df, intent_metrics, time_metrics)
    report_content += "\n\n"
    
    # Add appendix
    report_content += "---\n\n"
    report_content += "## 附录\n\n"
    report_content += "### 数据处理说明\n\n"
    report_content += "- 数据已清洗，移除了空值和无效记录\n"
    report_content += "- 用户咨询次数分析已去除最高和最低极值\n"
    report_content += "- 意图分类基于关键词匹配算法\n"
    report_content += "- 时间分析基于服务器的本地时间\n"
    report_content += "- **注意**: 本次分析已排除客服回复字数统计\n"
    
    # Save report
    report_filename = '智能客服数据分析报告.md'
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return report_filename

def generate_report(df, trimmed_counts):
    """
    Generate comprehensive text report
    
    Args:
        df (pd.DataFrame): Customer service data with intent classification
        trimmed_counts (pd.Series): User query counts with outliers removed
        
    Returns:
        str: Path to generated report file
    """
    # Calculate metrics
    user_metrics = calculate_user_metrics(df)
    time_metrics = calculate_time_metrics(df)
    intent_metrics = calculate_intent_metrics(df)
    
    # Generate report sections
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_content = f"""# 智能客服数据分析报告

**生成时间**: {timestamp}
**数据周期**: {df['创建时间'].min().strftime('%Y-%m-%d')} 至 {df['创建时间'].max().strftime('%Y-%m-%d')}

---

"""
    
    # Add all sections
    report_content += generate_executive_summary(df, user_metrics, time_metrics, intent_metrics)
    report_content += "\n\n"
    
    report_content += generate_intent_analysis(df)
    report_content += "\n\n"
    
    report_content += generate_user_behavior_analysis(trimmed_counts)
    report_content += "\n\n"
    
    report_content += generate_time_pattern_analysis(df)
    report_content += "\n\n"
    
    report_content += generate_operational_recommendations(df, intent_metrics, time_metrics)
    report_content += "\n\n"
    
    # Add appendix
    report_content += "---\n\n"
    report_content += "## 附录\n\n"
    report_content += "### 数据处理说明\n\n"
    report_content += "- 数据已清洗，移除了空值和无效记录\n"
    report_content += "- 用户咨询次数分析已去除最高和最低极值\n"
    report_content += "- 意图分类基于关键词匹配算法\n"
    report_content += "- 时间分析基于服务器的本地时间\n"
    
    # Save report
    report_filename = '智能客服数据分析报告.md'
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return report_filename