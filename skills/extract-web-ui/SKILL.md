---
name: extract-web-ui
description: 从指定网站页面抓取 CSS/内联样式并生成同风格的 UI 设计速览 Markdown（{网站名}-STYLE.md）。
metadata:
  short-description: 快速提取网页 UI 风格指南
---

# Extract Web UI

> 用途：用户提供网址（可附带页面说明，如“首页”），该技能自动抓取 HTML、关联 CSS，提炼颜色、字体、字号、按钮/卡片/表单等风格要点，输出 `{网站名称}-STYLE.md` 到当前工作目录。

## 使用参数
- `url`（必填）：目标页面 URL。
- `page`（可选）：页面描述，默认“首页”。写入文件头便于标注范围。

## 操作流程
1) **拉取页面**：`curl -sSL "$url" -o /tmp/extract_ui_page.html`（必要时请求提权）。  
2) **解析 CSS 链接**：从 HTML 中提取 `<link rel="stylesheet">` 与 `/_next/static/css/*.css` 等路径；补全相对路径为绝对 URL。  
3) **下载样式**：对每个 CSS 链接执行 `curl -sSL` 保存至 `/tmp/extract_ui_*.css`。同时抽取 HTML 内联 `<style>` 写入 `/tmp/extract_ui_inline.css`。  
4) **风格分析要点**（汇总逻辑，可用脚本/人工快速概括）：  
   - 色彩：统计十六进制颜色出现频次，挑核心品牌色/背景/文本/强调色。  
   - 字体：收集 `@font-face` 与 `font-family` 常用组合；记录字号/行高/字重及响应式断点。  
   - 组件：按钮、链接、输入、卡片、Chip、阴影、圆角、间距、outline/focus、hover 变化。  
   - 布局：常用断点、最大宽度、栅格/间距、全局 box-sizing。  
   - 动效：transition/transform/animation 样式。  
5) **生成文件**：文件名 `{域名去 www 前缀}-STYLE.md`，首段注明抓取日期、页面范围、来源 URL。内容用中文要点化，便于复用。  
6) **清理**：无需删除 /tmp 缓存，后续复用可覆盖。  

## 输出格式建议
- 标题：`# {Site} {Page} UI 设计风格速览`  
- 分节：品牌气质、色彩、字体、字号层级、组件（按钮/链接/表单/卡片/Toast 等）、布局与断点、交互动效、使用建议。  
- 尽量用简短要点，给出关键色值/尺寸/圆角/描边厚度。  

## 复用提示
- 如域名包含路径，文件名用主域名，例如 `motherduck.com-STYLE.md`。  
- 若页面强依赖 JS 才注入样式，可提示用户提供静态导出或允许使用带渲染的抓取方式（当前默认 curl）。  

