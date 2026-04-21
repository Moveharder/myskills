# Obsidian Markdown 规范

## Frontmatter (必需)

```yaml
---
title: 文档标题
date: 2026-03-26
tags:
  - tag1
  - tag2
aliases:
  - 别名1
  - 别名2
---
```

## 常用语法

### 标题
```markdown
# 一级标题
## 二级标题
### 三级标题
```

### 链接
```markdown
[[note]]                           # wikilink
[[note|显示文本]]                   # 带别名
[[note#heading]]                   # 链接到标题
```

### Callouts
```markdown
> [!note] 基本提示
> [!tip] 技巧
> [!warning] 警告
> [!info] 信息
> [!example] 示例
> [!quote] 引用
> [!faq]- 可折叠
```

### 表格
```markdown
| 列1 | 列2 | 列3 |
|------|------|------|
| 内容 | 内容 | 内容 |
```

### 列表
```markdown
- 无序列表
- [ ] 待办事项
- [x] 已完成

1. 有序列表
2. 第二项
```

### 高亮和格式化
```markdown
==高亮文本==
**粗体**
*斜体*
`代码`
```

### 代码块
````markdown
```python
def hello():
    print("Hello")
```
````

### 嵌入
```markdown
![[其他笔记]]      # 嵌入笔记
![[image.png|300]] # 嵌入图片（带宽度）
```

## 标签规则

```markdown
#tag                    # 单标签
#nested/tag             # 嵌套标签
#tag-with-dashes        # 带连字符
```

标签可包含：字母、数字（首字符不能是数字）、下划线、连字符、斜杠。

## 数学公式

```markdown
行内: $e^{i\pi} + 1 = 0$

块级:
$$
\frac{a}{b} = c
$$
```

## 脚注

```markdown
正文[^1]

[^1]: 脚注内容
```
