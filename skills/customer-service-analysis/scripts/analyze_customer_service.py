#!/usr/bin/env python3
"""
Customer Service Data Analysis Tool
Comprehensive analysis of customer service conversation data with intent classification,
user behavior analysis, and visualization generation.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import matplotlib.font_manager as fm
import os
import sys

# Import utility modules
import os
import sys

# Add current directory to Python path for module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from intent_classifier import classify_fitness_intent
    from visualizer import generate_charts, generate_charts_without_reply_length
    from report_generator import generate_report, generate_report_without_reply_length
    from data_processor import prepare_data
    from unanswered_questions_analysis import run_unanswered_analysis
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    print("Running in standalone mode...")
    
    # Fallback implementations if modules aren't available
    def classify_fitness_intent(question):
        return "其他咨询"
    
    def generate_charts(df, trimmed_counts):
        return "fallback_chart.png"
    
    def generate_report(df, trimmed_counts):
        return "fallback_report.md"
    
    def generate_charts_without_reply_length(df, trimmed_counts):
        return "fallback_chart_no_reply.png"
    
    def generate_report_without_reply_length(df, trimmed_counts):
        return "fallback_report_no_reply.md"
    
    def prepare_data(excel_file_path):
        import pandas as pd
        df = pd.read_excel(excel_file_path)
        df['创建时间'] = pd.to_datetime(df['创建时间'])
        return df
    
    def run_unanswered_analysis(excel_file_path):
        return None

def analyze_customer_service_data(excel_file_path, include_unanswered_analysis=True, exclude_reply_length=True):
    """
    Main analysis function for customer service data
    
    Args:
        excel_file_path (str): Path to Excel file containing customer service data
        include_unanswered_analysis (bool): Whether to include unanswered questions analysis
        exclude_reply_length (bool): Whether to exclude reply length analysis
        
    Returns:
        dict: Paths to generated output files
    """
    print(f"🚀 Starting customer service analysis for: {excel_file_path}")
    
    # Validate input file
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
        trimmed_counts = sorted_counts.iloc[1:-1]  # Remove highest and lowest values
        
        # Generate comprehensive charts (without reply length)
        print("📈 Generating visualization charts...")
        if exclude_reply_length:
            chart_file = generate_charts_without_reply_length(df, trimmed_counts)
        else:
            chart_file = generate_charts(df, trimmed_counts)
        
        # Generate detailed text report (without reply length)
        print("📝 Generating text report...")
        if exclude_reply_length:
            report_file = generate_report_without_reply_length(df, trimmed_counts)
        else:
            report_file = generate_report(df, trimmed_counts)
        
        result = {
            'text_report': report_file,
            'chart_file': chart_file
        }
        
        # Unanswered questions analysis
        if include_unanswered_analysis:
            print("🔍 Analyzing unanswered questions...")
            unanswered_result = run_unanswered_analysis(excel_file_path)
            if unanswered_result:
                result.update(unanswered_result)
        
        print("✅ Analysis complete!")
        print(f"📊 Text report: {report_file}")
        print(f"📈 Charts: {chart_file}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        raise

def main():
    """Main entry point for command line usage"""
    if len(sys.argv) != 2:
        print("Usage: python analyze_customer_service.py <excel_file_path>")
        print("Example: python analyze_customer_service.py ./data/customer_service.xlsx")
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