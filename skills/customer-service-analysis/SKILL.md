---
name: customer-service-analysis
description: Comprehensive analysis tool for customer service conversation data from Excel files. Automatically performs intent classification, user behavior analysis, time-based pattern analysis, and generates both detailed text reports and visualization charts. Use when you need to analyze customer service data to understand user behavior, question patterns, operational metrics, or generate business insights from conversation logs.
---

# Customer Service Analysis

## Overview

This skill enables comprehensive analysis of customer service conversation data, providing business insights through automated intent classification, user behavior patterns, time-based analysis, and visual reporting.

## Quick Start

For immediate analysis of customer service data:

1. **Input**: Excel file with columns `创建时间` (creation time), `问题` (questions), `回复` (replies), `用户` (users)
2. **Run**: Execute the main analysis script
3. **Output**: Get text report and visualization charts

## Core Capabilities

### 1. Intent Classification
Automatically categorizes customer questions into predefined intents based on domain-specific keywords:

**Fitness Center Intent Categories:**
- 会员卡服务 (Membership services)
- 器械使用 (Equipment usage) 
- 基础配套 (Basic facilities)
- 环境控制 (Environment control)
- 物品遗失 (Lost items)
- 入场服务 (Entry services)
- 营业服务 (Business hours)
- 支付相关 (Payment issues)
- 客服需求 (Customer service requests)
- 技术问题 (Technical issues)
- 闲聊互动 (Casual interactions)
- 其他咨询 (Other inquiries)

### 2. User Behavior Analysis
- Query frequency distribution with outlier removal
- User engagement patterns
- High-value user identification
- Activity trend analysis

### 3. Time-Based Analysis
- Hourly consultation patterns
- Daily trend analysis
- Weekly distribution analysis
- Peak time identification

### 4. Visualization Generation
Creates comprehensive charts including:
- Intent classification pie chart
- User query distribution histogram
- 24-hour activity timeline
- Daily trend line chart
- Weekly distribution bar chart
- Reply length distribution

### 5. Text Report Generation
Generates detailed analysis covering:
- Executive summary
- Intent analysis with percentages
- User behavior insights
- Time-based patterns
- Operational recommendations

## Usage Workflow

### Step 1: Data Preparation
Ensure your Excel file contains the required columns:
- `创建时间` - Timestamp of the conversation
- `问题` - Customer questions/queries
- `回复` - Service responses
- `用户` - User identifiers

### Step 2: Run Analysis
Execute the main analysis script with your Excel file path:

```bash
python scripts/analyze_customer_service.py /path/to/your/data.xlsx
```

### Step 3: Review Results
The analysis generates:
- `智能客服数据分析报告.md` - Detailed text report
- `客服数据分析图表.png` - Comprehensive visualization charts

## Customization

### Adapting to Different Industries

Modify the intent classification in `scripts/intent_classifier.py`:

```python
def classify_industry_intent(question):
    # Add industry-specific keywords and categories
    if any(keyword in question for keyword in ['industry_specific_terms']):
        return 'industry_category'
    # Add more categories as needed
```

### Adjusting Analysis Parameters

Key parameters in `scripts/config.py`:
- Intent keywords and categories
- Outlier removal thresholds
- Visualization color schemes
- Chart dimensions and styling

## Resources

### scripts/

**Main analysis script:**
- `analyze_customer_service.py` - Complete analysis pipeline

**Utility modules:**
- `intent_classifier.py` - Industry-specific intent classification
- `visualizer.py` - Chart generation and styling
- `report_generator.py` - Text report creation
- `config.py` - Configuration parameters
- `data_processor.py` - Data cleaning and preparation

**Execution:** Scripts can be run directly without loading into context. For modifications, read the specific script files as needed.

### references/

**Documentation files:**
- `intent_categories.md` - Complete intent taxonomy and keyword mappings
- `analysis_metrics.md` - Detailed explanations of all calculated metrics
- `customization_guide.md` - Guide for adapting to different industries

**Usage:** Load these files when modifying intent categories, understanding metrics, or customizing for specific business needs.

### assets/

**Template files:**
- `chart_templates/` - Chart styling templates
- `report_templates/` - Text report templates
- `font_files/` - Chinese font files for proper text rendering

**Usage:** These files are used directly in output generation and don't need to be loaded into context.