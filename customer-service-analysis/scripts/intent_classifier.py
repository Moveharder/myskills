"""
Intent Classifier Module
Domain-specific intent classification for customer service questions
"""

def classify_fitness_intent(question):
    """
    Classify customer questions into intent categories for fitness center domain
    
    Args:
        question (str): Customer question text
        
    Returns:
        str: Intent category
    """
    question = str(question).lower().strip()
    
    # Membership services
    if any(keyword in question for keyword in ['月卡', '周卡', '年卡', '卡', '办理', '退款', '使用', '规则', '多人', '停卡', '续费', '绑定']):
        return '会员卡服务'
    
    # Equipment usage
    elif any(keyword in question for keyword in ['器械', '哑铃', '跑步机', '史密斯', '插片式', '自行车', '卷腹机器', '卡扣']):
        return '器械使用'
    
    # Basic facilities
    elif any(keyword in question for keyword in ['淋浴', '卫生间', '更衣室', '放衣服', '篮子', '饮水', '洗澡']):
        return '基础配套'
    
    # Environment control
    elif any(keyword in question for keyword in ['空调', '温度', '热', '冷']):
        return '环境控制'
    
    # Lost items
    elif any(keyword in question for keyword in ['遗失', '丢失', '东西', '物品', '拉在店里', '丢在店里', '落在店里']):
        return '物品遗失'
    
    # Entry services
    elif any(keyword in question for keyword in ['扫码', '入场', '进店', '进去', '参观']):
        return '入场服务'
    
    # Business hours
    elif any(keyword in question for keyword in ['营业时间', '几点']):
        return '营业服务'
    
    # Payment related
    elif any(keyword in question for keyword in ['团购券', '美团', '大众点评']):
        return '支付相关'
    
    # Customer service requests
    elif any(keyword in question for keyword in ['人工客服', '人工', '投诉', '投诉建议', '报修']):
        return '客服需求'
    
    # Technical issues
    elif any(keyword in question for keyword in ['投屏', '电视', '网络', 'wifi', '停电', 'keep']):
        return '技术问题'
    
    # Casual interactions
    elif any(keyword in question for keyword in ['你好', '在吗', '聊天', '哈哈', '呵呵']):
        return '闲聊互动'
    
    # Other inquiries
    else:
        return '其他咨询'

def get_intent_color_mapping():
    """
    Get color mapping for different intent categories
    
    Returns:
        dict: Intent to color mapping
    """
    return {
        '会员卡服务': '#FF6B6B',
        '器械使用': '#4ECDC4', 
        '基础配套': '#45B7D1',
        '环境控制': '#96CEB4',
        '物品遗失': '#FFEAA7',
        '入场服务': '#DDA0DD',
        '营业服务': '#FFA07A',
        '支付相关': '#98D8C8',
        '客服需求': '#F7DC6F',
        '技术问题': '#BB8FCE',
        '闲聊互动': '#85C1E2',
        '其他咨询': '#F8B739'
    }

def get_all_intent_categories():
    """
    Get list of all intent categories
    
    Returns:
        list: All intent categories
    """
    return [
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