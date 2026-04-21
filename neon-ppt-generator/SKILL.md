---
name: neon-ppt-generator
description: Generate neon electronic style web-based presentations using Reveal.js. Use when user asks to create presentations, PPT, or slides with neon/cyberpunk/electronic style, or mentions "霓虹电子风格PPT", "流行电子风格PPT", "赛博朋克风格演示". Creates HTML-based presentations with gradient neon colors, dark backgrounds, glowing effects, and interactive features.
---

# Neon PPT Generator

Generate web-based presentations with neon electronic (cyberpunk) style using Reveal.js framework.

## When to Use This Skill

Use this skill when the user requests:
- "生成一个霓虹电子风格PPT"
- "生成一个流行电子风格PPT"
- "生成一个赛博朋克风格的演示文稿"
- "根据这个内容生成霓虹风格的网页PPT"
- Any request for neon/cyberpunk/electronic styled presentations

## Design Features

The generated presentations include:
- **Neon gradient colors**: Cyan (#00f5ff), Pink (#ff00ff), Purple (#bf00ff)
- **Dark background**: Cyberpunk style with grid pattern
- **Glowing effects**: Text and border neon glow
- **Scan line animation**: Dynamic scanning effect
- **Interactive cards**: Hover effects with glow
- **Responsive design**: Desktop and mobile support

## Interactive Features

- Keyboard navigation (←→↑↓)
- Progress bar
- Fullscreen mode (F key)
- Thumbnail navigation (ESC key)
- Code syntax highlighting
- Smooth transitions

## Workflow

### 1. Gather Content

Ask the user for the content source:
- Markdown file path
- Text content
- Outline or bullet points

If the user provides a file path, read the file to extract content.

### 2. Plan Slide Structure

Based on the content, plan the slide structure:
- **Cover slide**: Title and subtitle
- **TOC slide**: Table of contents (optional)
- **Content slides**: Organize content into logical sections
- **End slide**: Summary or thank you

Each content section can have:
- Section title slide (with large section number)
- Content slides (with cards or bullet points)

### 3. Generate Files

Create the following directory structure:
```
output-directory/
├── index.html          # Main HTML file
├── css/
│   └── neon-theme.css  # Neon theme styles
└── README.md           # Usage instructions (optional)
```

#### 3.1 Copy Theme CSS

Copy the neon theme CSS from assets:
```
assets/neon-theme.css → output-directory/css/neon-theme.css
```

#### 3.2 Generate index.html

Use the HTML template from `assets/index-template.html` and replace:
- `{{TITLE}}` → Presentation title
- `{{SLIDES_CONTENT}}` → Generated slides HTML

### 4. Slide HTML Patterns

#### Cover Slide
```html
<section class="cover-slide">
    <div class="neon-title">Title</div>
    <div class="neon-subtitle">Subtitle</div>
    <div class="neon-tagline">Tagline</div>
    <div class="scan-line"></div>
</section>
```

#### Section Title Slide
```html
<section>
    <section class="section-title-slide">
        <div class="section-number">01</div>
        <h2>Section Title</h2>
        <div class="section-divider"></div>
    </section>
    
    <!-- Content slides follow -->
    <section class="content-slide">
        <h3>Slide Title</h3>
        <div class="content-grid">
            <div class="content-card">
                <div class="card-icon">📋</div>
                <div class="card-title">Card Title</div>
                <div class="card-content">
                    <p>Content here</p>
                    <p class="card-note">Note text</p>
                </div>
            </div>
        </div>
    </section>
</section>
```

#### Content Card (Full Width)
```html
<div class="content-card full-width">
    <div class="card-icon">🔧</div>
    <div class="card-title">Card Title</div>
    <div class="card-content">
        <p>Content here</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    </div>
</div>
```

#### Code Example
```html
<div class="code-example">
    <pre><code class="language-markdown"># Code here</code></pre>
</div>
```

#### End Slide
```html
<section class="end-slide">
    <div class="neon-title">Thank You</div>
    <div class="neon-subtitle">Subtitle</div>
    <div class="end-quote">"Quote"</div>
    <div class="scan-line"></div>
</section>
```

### 5. Output Location

Ask the user for output location, or use a sensible default:
- Same directory as source content
- Current working directory
- User-specified path

### 6. Provide Instructions

After generating files, inform the user:
- File location
- How to open (double-click index.html)
- Keyboard shortcuts
- Customization options

## Assets

This skill includes:

### assets/neon-theme.css
Complete neon electronic theme stylesheet with:
- CSS variables for neon colors
- Typography styles
- Slide layouts (cover, section, content, end)
- Card components
- Code highlighting
- Animations and transitions
- Responsive design
- Thumbnail navigation styles

### assets/index-template.html
HTML template with:
- Reveal.js setup
- Highlight.js integration
- Keyboard navigation
- Thumbnail navigation
- Placeholder variables: `{{TITLE}}`, `{{SLIDES_CONTENT}}`

## Best Practices

1. **Keep slides concise**: 3-5 bullet points per slide
2. **Use icons**: Add emoji icons to cards for visual appeal
3. **Group related content**: Use content-grid for 2-column layouts
4. **Add notes**: Use `.card-note` for important callouts
5. **Highlight code**: Use `<code>` tags for inline code, code blocks for examples
6. **Test in browser**: Always verify the generated HTML works correctly

## Example Usage

**User**: "根据这个文档生成一个霓虹电子风格PPT"

**Workflow**:
1. Read the document content
2. Extract title, sections, and key points
3. Plan slide structure (cover, TOC, sections, end)
4. Create output directory
5. Copy neon-theme.css
6. Generate index.html with slides
7. Provide usage instructions

**Output**: A complete web-based presentation ready to open in browser.
