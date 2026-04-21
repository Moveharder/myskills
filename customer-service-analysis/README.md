# Customer Service Analysis Skill Usage Guide

## Quick Start

This skill provides comprehensive analysis of customer service conversation data from Excel files.

### Prerequisites
- Python 3.7+
- Required packages: pandas, matplotlib, seaborn, openpyxl

### Installation
```bash
pip install pandas matplotlib seaborn openpyxl
```

### Usage

#### Method 1: Using the Standalone Script (Recommended)
```bash
cd scripts
python customer_service_analysis_standalone.py path/to/your/data.xlsx
```

#### Method 2: Using the Modular Scripts
```bash
cd scripts
python analyze_customer_service.py path/to/your/data.xlsx
```

#### Method 3: Advanced Analysis with Unanswered Questions
```python
from scripts.analyze_customer_service import analyze_customer_service_data

# Include unanswered questions analysis, exclude reply length statistics
result = analyze_customer_service_data(
    'path/to/your/data.xlsx', 
    include_unanswered_analysis=True, 
    exclude_reply_length=True
)
```

## Expected Data Format

Your Excel file should contain these columns:
- `创建时间` - Conversation timestamp (required)
- `问题` - Customer questions/queries (required)
- `回复` - Service responses (required)
- `用户` - User identifiers (required)

## Output Files

The analysis generates:
- `智能客服数据分析报告.md` - Detailed text report with insights and recommendations (excluding reply length)
- `客服数据分析图表.png` - Comprehensive visualization charts (excluding reply length)
- `无法回答问题汇总表.xlsx` - Summary of unanswered questions with intent classification
- `无法回答问题场景分布图.png` - Visualization of unanswered question patterns
- `无法回答问题分析报告.md` - Detailed analysis and recommendations for unanswered questions

## Features

### Intent Classification
Automatically categorizes customer questions into fitness center intents:
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

### Analysis Capabilities
- User behavior analysis with outlier removal
- Time-based pattern analysis (hourly, daily, weekly)
- Intent distribution analysis
- Engagement metrics calculation
- Operational recommendations
- **Unanswered questions analysis** - Identify patterns in questions that cannot be answered
- **Chinese font support** - Proper handling of Chinese text in visualizations

### Visualizations
- Intent classification pie chart
- User query distribution histogram
- 24-hour activity timeline
- Daily trend analysis
- Weekly distribution chart
- **Unanswered questions scenario distribution** - Patterns in questions requiring escalation
- **Chinese text rendering** - Proper font handling for all charts

## Customization

### For Different Industries
Edit `intent_classifier.py` to customize intent categories for your specific industry.

### Analysis Parameters
Modify `config.py` to adjust:
- Chart styling and colors
- Analysis thresholds
- Output file names

### Adding New Metrics
Extend the analysis by adding new calculation functions in the appropriate modules.

## Troubleshooting

### Chinese Font Issues
The skill now includes automatic Chinese font handling. If charts still show garbled text:
1. Ensure system has Chinese fonts installed
2. Font fallback is automatically handled in `setup_chinese_fonts()` function
3. Charts are generated with proper Chinese text rendering

### Memory Issues with Large Datasets
For datasets with >100,000 records:
1. Process data in chunks
2. Reduce chart complexity
3. Use sampling for visualization

### Import Errors
Ensure all required packages are installed:
```bash
pip install --upgrade pandas matplotlib seaborn openpyxl
```

## Examples

### Basic Usage
```bash
python customer_service_analysis_standalone.py ./customer_data.xlsx
```

### Output Example
```
🚀 Starting customer service analysis for: ./customer_data.xlsx
📊 Reading and preparing data...
🏷️  Classifying user intents...
👥 Analyzing user behavior patterns...
📈 Generating visualization charts...
📝 Generating text report...
✅ Analysis complete!
📊 Text report: 智能客服数据分析报告.md
📈 Charts: 客服数据分析图表.png

🎉 Analysis completed successfully!
```

## Support

For detailed customization options and industry adaptations, see:
- `references/intent_categories.md` - Intent classification reference
- `references/analysis_metrics.md` - Metrics explanations
- `references/customization_guide.md` - Customization guide