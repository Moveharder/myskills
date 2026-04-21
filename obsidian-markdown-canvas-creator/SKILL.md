---
name: obsidian-markdown-canvas-creator
description: 创建 Obsidian 友好的 Markdown 文档和 JSON Canvas 可视化文件。用于当用户要求研究/分析某主题并输出到 Obsidian 时，如："生成一份关于xx主题的分析/研究"、"研究一下xxx"、"帮我收集xxx的资料"。同时输出 Markdown (.md) 和 Canvas (.canvas) 两种格式。
---

# Obsidian Markdown & Canvas Creator

## 概述

将用户指定的研究主题同时输出为：
- **Markdown 文档**: Obsidian 友好格式，含 frontmatter、wikilinks、callouts、表格
- **JSON Canvas**: 知识图谱可视化，节点自动连线、布局合理

## 触发场景

用户说以下类似的话时使用此 skill：
- "生成一份关于xx主题的分析/研究，同时输出为markdown和Canvas保存到obsidian中"
- "研究一下xxx，结果输出到obsidian中"
- "帮我收集/整理 xxx 的资料，存到 Obsidian"
- 任何需要同时生成 Markdown 和 Canvas 文件的研究任务

## 输出路径

```
/AI/{目录}/{主题}.md
/AI/{目录}/{主题}.canvas
```

- **默认目录**: `/AI/{topic}/`（当用户未指定时）
- **自定义目录**: `/AI/{用户指定目录}/`（当用户指定了目录时）

## 核心流程

### Step 1: 加载依赖 Skills

```markdown
使用 skill tool 加载:
- obsidian-markdown: 生成 Obsidian Markdown 文件
- json-canvas: 生成 JSON Canvas 可视化文件
```

### Step 2: 解析主题和目录

从用户请求中提取：
- **主题**: 用户要研究的内容
- **目录**: 用户是否指定了保存目录

### Step 3: 信息收集（如需要）

```bash
使用 websearch 工具搜索相关信息:
- 官方资料/新闻
- 行业报告/数据
- 维基百科/百科类内容
```

### Step 4: 创建目录结构

```bash
mkdir -p "/AI/{目录}"
```

### Step 5: 生成 Markdown 文件

**文件路径**: `/AI/{目录}/{主题}.md`

**必须包含**:
1. YAML frontmatter (title, date, tags, aliases)
2. 标题层级结构 (##, ###)
3. wikilinks `[[note]]` 连接相关概念
4. callouts `> [!tip]` 等突出重点
5. 表格整理结构化数据
6. tags 标签

**参考模板**:
```markdown
---
title: {主题}
date: {当前日期 YYYY-MM-DD}
tags:
  - {tag1}
  - {tag2}
aliases:
  - {别名}
---

# {主题}

> [!info] 简介
> 1-2 句话概述主题

## 核心内容

### 1. {子标题}

内容...

### 2. {子标题}

内容...

## 相关链接

- [[相关主题1]]
- [[相关主题2]]

---
*数据来源: ...*
```

### Step 6: 生成 Canvas 文件

**文件路径**: `/AI/{目录}/{主题}.canvas`

**结构规范**:
```json
{
  "nodes": [
    {
      "id": "{16位hex ID}",
      "type": "text",
      "x": 400,
      "y": 30,
      "width": 400,
      "height": 120,
      "color": "5",
      "text": "# {主题}\n\n副标题/简介"
    },
    // ... 其他节点
  ],
  "edges": [
    {
      "id": "{16位hex ID}",
      "fromNode": "{源节点ID}",
      "fromSide": "bottom",
      "toNode": "{目标节点ID}",
      "toSide": "top",
      "label": "{关系描述}"
    },
    // ... 其他连线
  ]
}
```

**节点规划原则**:
- 标题节点 (y: 30-50)
- 内容节点 (y: 200-400)
- 关联节点 (y: 500-700)
- 间距: 50-100px
- 节点宽度: 280-450px
- 高度: 根据内容调整

**布局模板**:
```
     [标题节点]
          |
    ┌─────┼─────┐
    ↓     ↓     ↓
[内容1] [内容2] [内容3]
    |     |     |
    └─────┼─────┘
          ↓
     [关联节点]
```

## ID 生成规则

使用 16 位十六进制字符串（如 `6f0ad84f44ce9c01`），每节点唯一。

## 数据获取策略

| 主题类型 | 数据来源 |
|----------|----------|
| 公司财报 | 官网 investor relations、Yahoo Finance、PR Newswire |
| 人物 | 维基百科、LinkedIn、官方 biography |
| 技术概念 | 官方文档、GitHub、Wikipedia |
| 产品 | 官网、TechCrunch、评测网站 |
| 通用 | Wikipedia、WebSearch |

## 完成后

向用户报告：
1. 创建的文件路径
2. 核心内容概要
3. Canvas 包含的节点数量

## References

- [obsidian-markdown 规范](references/obsidian-markdown.md)
- [json-canvas 规范](references/json-canvas.md)
