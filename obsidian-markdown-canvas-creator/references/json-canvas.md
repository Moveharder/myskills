# JSON Canvas 规范

## 文件结构

```json
{
  "nodes": [],
  "edges": []
}
```

## Nodes (节点)

### 必需字段
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 16位十六进制唯一ID |
| type | string | text / file / link / group |
| x | integer | X坐标 |
| y | integer | Y坐标 |
| width | integer | 宽度(px) |
| height | integer | 高度(px) |

### Text Node
```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# 标题\n\n内容支持 **Markdown**"
}
```

### File Node
```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "path/to/file.png"
}
```

### Link Node
```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 1000,
  "y": 0,
  "width": 400,
  "height": 200,
  "url": "https://example.com"
}
```

### Group Node (容器)
```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 1000,
  "height": 600,
  "label": "分组标题",
  "color": "4"
}
```

### Color 颜色
| 预设 | 颜色 |
|------|------|
| "1" | 红 |
| "2" | 橙 |
| "3" | 黄 |
| "4" | 绿 |
| "5" | 青 |
| "6" | 紫 |

或使用 hex: `"#FF0000"`

## Edges (连线)

### 必需字段
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一ID |
| fromNode | string | 源节点ID |
| toNode | string | 目标节点ID |

### 可选字段
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| fromSide | string | - | top/right/bottom/left |
| toSide | string | - | top/right/bottom/left |
| fromEnd | string | "none" | none/arrow |
| toEnd | string | "arrow" | none/arrow |
| label | string | - | 连线标签 |
| color | string | - | 颜色 |

```json
{
  "id": "0123456789abcdef",
  "fromNode": "节点A",
  "fromSide": "right",
  "toNode": "节点B",
  "toSide": "left",
  "label": "包含关系",
  "toEnd": "arrow"
}
```

## 布局指南

### 坐标系
- X 增加向右，Y 增加向下
- 坐标可负数（画布无限延伸）
- 建议对齐网格（10 或 20 的倍数）

### 间距建议
- 节点间距: 50-100px
- 组内边距: 20-50px

### 尺寸参考
| 节点类型 | 宽度 | 高度 |
|----------|------|------|
| 小型文本 | 200-300 | 80-150 |
| 中型文本 | 300-450 | 150-300 |
| 大型文本 | 400-600 | 300-500 |

### 推荐布局

**三栏式布局**:
```
     [标题]
    /    |    \
[左栏] [中栏] [右栏]
    \    |    /
     [底部汇总]
```

**层级式布局**:
```
   [标题]
      |
  [一级内容]
  /    |    \
[二级] [二级] [二级]
```

## ID 生成

16位十六进制（64位随机值）:
```
6f0ad84f44ce9c01
a3b2c1d0e9f8a7b6
```

## 验证清单

1. ✅ 所有 ID 唯一
2. ✅ 每条 edge 的 fromNode/toNode 指向存在的节点
3. ✅ type 为 text/file/link/group 之一
4. ✅ side 值为 top/right/bottom/left 之一
5. ✅ end 值为 none/arrow 之一
6. ✅ JSON 可正常解析
