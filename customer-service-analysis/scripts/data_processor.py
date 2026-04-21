"""
Data Processor Module
Data preparation and cleaning functions for customer service analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime

def prepare_data(excel_file_path):
    """
    Read and prepare customer service data for analysis
    
    Args:
        excel_file_path (str): Path to Excel file
        
    Returns:
        pd.DataFrame: Prepared DataFrame
    """
    # Read Excel file
    df = pd.read_excel(excel_file_path)
    
    # Check required columns
    required_columns = ['创建时间', '问题', '回复', '用户']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Clean and prepare data
    df['创建时间'] = pd.to_datetime(df['创建时间'])
    
    # Fill missing values
    df['问题'] = df['问题'].fillna('')
    df['回复'] = df['回复'].fillna('')
    df['用户'] = df['用户'].fillna('Unknown')
    
    # Remove empty rows
    df = df[(df['问题'].str.strip() != '') & (df['回复'].str.strip() != '')]
    
    # Sort by time
    df = df.sort_values('创建时间')
    
    return df

def calculate_user_metrics(df):
    """
    Calculate user behavior metrics
    
    Args:
        df (pd.DataFrame): Customer service data
        
    Returns:
        dict: User metrics
    """
    user_query_counts = df['用户'].value_counts()
    
    metrics = {
        'total_users': len(user_query_counts),
        'total_queries': len(df),
        'avg_queries_per_user': user_query_counts.mean(),
        'median_queries_per_user': user_query_counts.median(),
        'max_queries_by_user': user_query_counts.max(),
        'min_queries_by_user': user_query_counts.min()
    }
    
    # Outlier removal metrics
    sorted_counts = user_query_counts.sort_values()
    if len(sorted_counts) > 2:
        trimmed_counts = sorted_counts.iloc[1:-1]
        metrics['trimmed_mean'] = trimmed_counts.mean()
        metrics['trimmed_median'] = trimmed_counts.median()
    
    return metrics

def calculate_time_metrics(df):
    """
    Calculate time-based metrics
    
    Args:
        df (pd.DataFrame): Customer service data
        
    Returns:
        dict: Time metrics
    """
    # Time range
    time_range = df['创建时间'].max() - df['创建时间'].min()
    
    # Peak hours
    df['小时'] = df['创建时间'].dt.hour
    hourly_counts = df['小时'].value_counts()
    peak_hour = hourly_counts.idxmax()
    
    # Peak day
    df['日期'] = df['创建时间'].dt.date
    daily_counts = df['日期'].value_counts()
    peak_day = daily_counts.idxmax()
    
    # Weekday vs weekend
    df['星期几'] = df['创建时间'].dt.day_name()
    weekday_mask = df['星期几'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    weekday_count = df[weekday_mask].shape[0]
    weekend_count = df[~weekday_mask].shape[0]
    
    metrics = {
        'analysis_period_days': time_range.days,
        'peak_hour': peak_hour,
        'peak_day': peak_day,
        'weekday_queries': weekday_count,
        'weekend_queries': weekend_count,
        'weekday_ratio': weekday_count / (weekday_count + weekend_count)
    }
    
    return metrics

def calculate_intent_metrics(df):
    """
    Calculate intent distribution metrics
    
    Args:
        df (pd.DataFrame): Customer service data with intent classification
        
    Returns:
        dict: Intent metrics
    """
    if '新意图v2' not in df.columns:
        return {}
    
    intent_counts = df['新意图v2'].value_counts()
    total_queries = len(df)
    
    metrics = {
        'total_intents': len(intent_counts),
        'top_intent': intent_counts.index[0],
        'top_intent_count': intent_counts.iloc[0],
        'top_intent_percentage': (intent_counts.iloc[0] / total_queries) * 100
    }
    
    # Add percentages for all intents
    for intent, count in intent_counts.items():
        metrics[f'{intent}_percentage'] = (count / total_queries) * 100
    
    return metrics