# Customization Guide

This guide explains how to adapt the customer service analysis skill for different industries and use cases.

## Industry Adaptation

### 1. Intent Classification Customization

#### Step 1: Identify Industry-Specific Categories
Different industries have different customer needs. Common patterns:

**E-commerce**:
- Product inquiries
- Order status
- Shipping/delivery
- Returns/refunds
- Payment issues
- Account management

**Banking/Finance**:
- Account balance
- Transaction history
- Card services
- Loan inquiries
- Investment services
- Security issues

**Healthcare**:
- Appointment booking
- Medical records
- Insurance/billing
- Prescription inquiries
- Facility information
- Emergency services

**Telecommunications**:
- Service plans
- Billing inquiries
- Technical support
- Device issues
- Account changes
- Coverage information

#### Step 2: Define Keywords for Each Category
For each intent category, identify specific keywords:

```python
# Example: E-commerce customization
def classify_ecommerce_intent(question):
    question = str(question).lower().strip()
    
    # Product inquiries
    if any(keyword in question for keyword in ['产品', '商品', '库存', '规格', '尺寸', '颜色']):
        return '商品咨询'
    
    # Order status
    elif any(keyword in question for keyword in ['订单', '状态', '物流', '发货', '配送']):
        return '订单查询'
    
    # Add more categories...
    else:
        return '其他咨询'
```

#### Step 3: Update Color Mapping
Adjust colors to match brand or preferences:

```python
def get_ecommerce_color_mapping():
    return {
        '商品咨询': '#E74C3C',
        '订单查询': '#3498DB',
        '退换货': '#2ECC71',
        '支付问题': '#F39C12',
        # Add more mappings...
    }
```

### 2. Data Structure Adaptation

#### Required Columns
The skill expects these columns by default:
- `创建时间` (Creation time)
- `问题` (Questions)
- `回复` (Replies)
- `用户` (Users)

#### Custom Column Mapping
If your data has different column names, update the data processor:

```python
def prepare_data_custom(excel_file_path):
    df = pd.read_excel(excel_file_path)
    
    # Map your columns to expected names
    column_mapping = {
        'timestamp': '创建时间',
        'question': '问题',
        'answer': '回复',
        'customer_id': '用户'
    }
    
    df = df.rename(columns=column_mapping)
    # Continue with standard processing...
```

### 3. Analysis Customization

#### Adding New Metrics
Extend the analysis with industry-specific metrics:

```python
def calculate_ecommerce_metrics(df):
    metrics = {}
    
    # Conversion tracking
    if '购买转化' in df.columns:
        metrics['conversion_rate'] = df['购买转化'].mean()
    
    # Customer lifetime value
    if '订单金额' in df.columns:
        metrics['avg_order_value'] = df['订单金额'].mean()
    
    return metrics
```

#### Custom Visualizations
Add charts specific to your industry:

```python
def generate_ecommerce_charts(df, trimmed_counts):
    # Standard charts
    chart_file = generate_charts(df, trimmed_counts)
    
    # Add custom e-commerce chart
    if '订单金额' in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        daily_revenue = df.groupby('日期')['订单金额'].sum()
        ax.plot(daily_revenue.index, daily_revenue.values)
        ax.set_title('每日收入趋势')
        # Save additional chart...
    
    return chart_file
```

## Configuration Management

### Create a Configuration File
Create `config.py` to manage all customizations:

```python
# config.py
INDUSTRY = "fitness"  # or "ecommerce", "banking", etc.

# Intent classification function
INTENT_CLASSIFIER = {
    "fitness": classify_fitness_intent,
    "ecommerce": classify_ecommerce_intent,
    "banking": classify_banking_intent,
}

# Color mappings
COLOR_MAPPINGS = {
    "fitness": get_fitness_color_mapping,
    "ecommerce": get_ecommerce_color_mapping,
    "banking": get_banking_color_mapping,
}

# Industry-specific metrics
METRICS_CALCULATORS = {
    "fitness": calculate_fitness_metrics,
    "ecommerce": calculate_ecommerce_metrics,
    "banking": calculate_banking_metrics,
}
```

### Dynamic Configuration Loading
Update the main analysis script to use configuration:

```python
import config

def analyze_customer_service_data(excel_file_path, industry="fitness"):
    # Get industry-specific components
    intent_classifier = config.INTENT_CLASSIFIER[industry]
    color_mapping = config.COLOR_MAPPINGS[industry]()
    metrics_calculator = config.METRICS_CALCULATORS[industry]
    
    # Use industry-specific functions
    df['新意图v2'] = df['问题'].apply(intent_classifier)
    # Continue analysis...
```

## Advanced Customization

### Machine Learning Intent Classification
For higher accuracy, integrate ML models:

```python
import joblib

def ml_intent_classifier(question):
    # Load pre-trained model
    model = joblib.load('intent_classifier_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    
    # Predict intent
    question_vec = vectorizer.transform([question])
    intent = model.predict(question_vec)[0]
    
    return intent
```

### Real-time Analysis
For real-time customer service monitoring:

```python
def real_time_analysis(new_data):
    # Combine with historical data
    historical_data = load_historical_data()
    combined_data = pd.concat([historical_data, new_data])
    
    # Run analysis
    results = analyze_customer_service_data(combined_data)
    
    # Alert on anomalies
    if detect_anomalies(results):
        send_alert(results)
    
    return results
```

### Integration with External Systems
Connect with CRM, ticketing systems, or databases:

```python
def sync_with_crm(analysis_results):
    # Update customer records
    crm_client = CRMClient()
    
    for user, metrics in analysis_results['user_metrics'].items():
        crm_client.update_customer_record(user, {
            'last_activity': metrics['last_query_date'],
            'query_count': metrics['total_queries'],
            'primary_intent': metrics['top_intent']
        })
```

## Testing and Validation

### Test Data Structure
Create test datasets to validate customizations:

```python
def create_test_data():
    test_data = {
        '创建时间': ['2024-01-01 09:00:00', '2024-01-01 10:00:00'],
        '问题': ['怎么办理会员卡？', '健身房几点关门？'],
        '回复': ['可以在线办理...', '晚上10点关门...'],
        '用户': ['user_001', 'user_002']
    }
    return pd.DataFrame(test_data)
```

### Validation Metrics
Test classification accuracy and analysis quality:

```python
def validate_classification(test_data, expected_intents):
    predicted_intents = test_data['问题'].apply(classify_fitness_intent)
    accuracy = (predicted_intents == expected_intents).mean()
    
    print(f"Classification accuracy: {accuracy:.2%}")
    return accuracy
```

## Deployment Considerations

### Environment Setup
Package dependencies for deployment:

```bash
pip freeze > requirements.txt
```

### Docker Configuration
Create Dockerfile for containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts/ ./scripts/
COPY references/ ./references/

CMD ["python", "scripts/analyze_customer_service.py", "data.xlsx"]
```

### Scheduled Analysis
Set up automated analysis using cron or task schedulers:

```bash
# Daily analysis at 8 AM
0 8 * * * /usr/bin/python /app/scripts/analyze_customer_service.py /data/latest_data.xlsx
```

## Best Practices

1. **Start Simple**: Begin with basic intent classification, then add complexity
2. **Test Thoroughly**: Validate customizations with diverse test data
3. **Monitor Performance**: Track classification accuracy and analysis quality
4. **Document Changes**: Keep clear documentation of customizations
5. **Version Control**: Use Git to track changes to custom code
6. **Regular Updates**: Periodically review and update intent keywords and metrics