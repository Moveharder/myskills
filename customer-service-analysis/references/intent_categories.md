# Intent Categories Reference

## Fitness Center Customer Service Intent Classification

This document provides a comprehensive reference for intent categories used in fitness center customer service analysis.

## Primary Intent Categories

### 1. 会员卡服务 (Membership Services)
**Description**: Questions related to membership cards, pricing, and membership management.

**Keywords**:
- 月卡, 周卡, 年卡, 卡
- 办理, 退款, 使用, 规则
- 多人, 停卡, 续费, 绑定

**Example Questions**:
- "月卡多少钱？"
- "怎么办理会员卡？"
- "可以退款吗？"

### 2. 器械使用 (Equipment Usage)
**Description**: Questions about fitness equipment usage, location, and operation.

**Keywords**:
- 器械, 哑铃, 跑步机
- 史密斯, 插片式, 自行车
- 卷腹机器, 卡扣

**Example Questions**:
- "哑铃在哪里？"
- "跑步机怎么用？"
- "史密斯机安全吗？"

### 3. 基础配套 (Basic Facilities)
**Description**: Questions about basic facilities and amenities.

**Keywords**:
- 淋浴, 卫生间, 更衣室
- 放衣服, 篮子, 饮水, 洗澡

**Example Questions**:
- "有淋浴吗？"
- "更衣室在哪里？"
- "提供储物篮吗？"

### 4. 环境控制 (Environment Control)
**Description**: Questions about temperature, air conditioning, and comfort.

**Keywords**:
- 空调, 温度, 热, 冷

**Example Questions**:
- "空调太冷了"
- "可以调温度吗？"

### 5. 物品遗失 (Lost Items)
**Description**: Reports and inquiries about lost personal items.

**Keywords**:
- 遗失, 丢失, 东西, 物品
- 拉在店里, 丢在店里, 落在店里

**Example Questions**:
- "我丢了手机"
- "有人看到我的水杯吗？"

### 6. 入场服务 (Entry Services)
**Description**: Questions about gym entry procedures and access.

**Keywords**:
- 扫码, 入场, 进店, 进去, 参观

**Example Questions**:
- "怎么扫码进店？"
- "可以带朋友参观吗？"

### 7. 营业服务 (Business Hours)
**Description**: Questions about operating hours and schedule.

**Keywords**:
- 营业时间, 几点

**Example Questions**:
- "几点开门？"
- "周末营业吗？"

### 8. 支付相关 (Payment Issues)
**Description**: Questions about payments, vouchers, and billing.

**Keywords**:
- 团购券, 美团, 大众点评

**Example Questions**:
- "美团券怎么用？"
- "可以支付宝吗？"

### 9. 客服需求 (Customer Service Requests)
**Description**: Requests for human customer service or special assistance.

**Keywords**:
- 人工客服, 人工, 投诉, 投诉建议, 报修

**Example Questions**:
- "我要投诉"
- "可以转人工吗？"

### 10. 技术问题 (Technical Issues)
**Description**: Technical problems with equipment or systems.

**Keywords**:
- 投屏, 电视, 网络, wifi, 停电, keep

**Example Questions**:
- "wifi密码是多少？"
- "电视坏了"

### 11. 闲聊互动 (Casual Interactions)
**Description**: Greetings and casual conversation.

**Keywords**:
- 你好, 在吗, 聊天, 哈哈, 呵呵

**Example Questions**:
- "你好"
- "在吗？"

### 12. 其他咨询 (Other Inquiries)
**Description**: Questions that don't fit into other categories.

**Keywords**: None specific - catch-all category.

**Example Questions**:
- "有什么活动吗？"
- "老板在吗？"

## Classification Algorithm

The intent classification uses a keyword-based matching approach:

1. **Lowercase conversion**: All text is converted to lowercase for consistent matching
2. **Keyword matching**: Each intent category has associated keywords
3. **Priority ordering**: Categories are checked in a specific order to ensure proper classification
4. **Fallback**: If no keywords match, the question is classified as "其他咨询"

## Customization Guidelines

To adapt this classification for different industries:

1. **Modify keywords**: Update keyword lists for industry-specific terminology
2. **Add categories**: Create new intent categories as needed
3. **Adjust priorities**: Reorder the classification logic for your specific use case
4. **Test accuracy**: Validate classification accuracy on sample data

## Performance Metrics

- **Accuracy**: Target >85% classification accuracy
- **Coverage**: Ensure >95% of questions are classified
- **Balance**: Aim for reasonably balanced category sizes
- **Actionability**: Categories should be actionable for business decisions