# html-anything 集成分析报告

**日期：** 2026-05-20
**作者：** 元师 (Architect)
**状态：** 调研完成，方案已确认

---

## 一、项目概述

GitHub 上名为 "html-anything" 的重要项目有两个：

### 1.1 nexu-io/html-anything（⭐ 3,949）

> "The agentic HTML editor — your local AI agent writes the HTML, you ship it."

- **定位：** 面向 AI Agent 的 HTML 编辑器（Next.js 16 Web 应用）
- **核心能力：**
  - 75 个设计技能模板（magazine / deck / poster / tweet / prototype / data report 等 9 种产出表面）
  - 自动检测 8 种 coding agent CLI（Claude Code、Cursor、Codex、Gemini CLI 等）
  - 沙箱化 iframe 预览
  - 一键导出：WeChat、X、知乎、HTML、PNG
  - **零 API Key**: 复用用户本地已登录的 agent 会话
- **技术栈：** Next.js 16，pnpm workspace，TypeScript
- **License:** Apache 2.0

### 1.2 clockless-org/html-anything（⭐ 63）

> "Turn any file into a beautiful, interactive, shareable HTML."

- **定位：** 面向 AI Agent 的 SKILL.md（Claude Code 等 agent 的技能文件）
- **核心能力：**
  - 60 种数据源解析（CSV、PDF、DOCX、聊天记录、日志、Notion、Kindle 摘录等）
  - 17 种设计系统（dark dashboard、minimal clean、interactive report 等）
  - 自动路由：根据输入类型自动选配最佳样式
  - 单文件 .html 输出（离线可用，可分享）
- **安装方式：** `npx skills add clockless-org/html-anything` 或 `git clone`
- **本质：** 一个 prompt template 集合 + 样式文件，注入 agent 的上下文
- **技术栈：** JavaScript，纯 prompt + HTML/CSS 模板
- **License:** MIT-0

---

## 二、Market Cognition 博客现状

```
/opt/projects/blog/
├── _config.yml          # Jekyll 配置，markdown: kramdown
├── Gemfile               # github-pages + jekyll-feed + jekyll-seo-tag
├── _layouts/
│   ├── default.html      # 基础 HTML 框架 (zh-CN, Georgia 字体)
│   └── post.html         # 文章详情页布局
├── _posts/               # 55 篇 Markdown 文章
├── css/style.css         # 手工 CSS，暖色调主题
├── assets/               # 静态资源（音频等）
├── scripts/
│   └── strip_md.py       # Markdown 处理脚本
├── docs/
│   └── retrospectives/   # 镜师复盘报告
└── index.html            # 首页
```

- **框架：** Jekyll + GitHub Pages (kramdown 渲染)
- **内容格式：** Markdown (.md) 放在 `_posts/`，含 YAML frontmatter
- **已有 audio 嵌入：** 部分文章使用 `<audio controls>` 标签嵌入音频
- **约束：** 纯静态站点，无服务端运行时

---

## 三、集成可行性分析

### 3.1 nexu-io/html-anything → ✗ 不适合直接集成

| 维度 | 评估 |
|------|------|
| 架构匹配度 | ❌ 它是 Web 应用（需 Node.js 运行），博客是静态站点 |
| 依赖复杂度 | ❌ 需要 Next.js 16 + pnpm + browser 运行时 |
| GitHub Pages 兼容 | ❌ 无法在 GitHub Pages 上运行服务端 |
| 集成方式 | 仅可作为「写作辅助工具」——由 Agent 在本地用它生成 HTML 片段，再手动粘贴到博客 |

**结论：** 不宜作为博客基础架构的一部分。但可作为 **Agent 写作流水线中的「生成环节」**——让 Agent 启动 html-anything 的 Next.js 服务，通过其 API 生成精美的 HTML 内容卡片，提取后嵌入博客���

### 3.2 clockless-org/html-anything → ✓ 可作为 Agent Skill 集成

| 维度 | 评估 |
|------|------|
| 架构匹配度 | ✅ 纯 prompt template + HTML/CSS，无服务端依赖 |
| 依赖复杂度 | ✅ 无 Node.js 运行时依赖，只需 agent 能渲染 HTML |
| GitHub Pages 兼容 | ✅ 生成的 HTML 可直接嵌入博客 |
| 集成方式 | 作为 blog-publishing skill 的「富格式渲染」子功能 |

**核心价值：**
- 当 Agent 撰写博客时，可将数据密集段落（表格、对比、数据卡片）渲染为精美的 HTML 片段
- 生成的 HTML 是自包含的单文件，可直接作为 `_includes/` 组件嵌入 Jekyll
- 不改变现有 Markdown 工作流

### 3.3 对 Jekyll 博客的具体集成方案

```
_workflow:
  原始数据/分析结果
      ↓ (clockless-org/html-anything skill)
  自包含 HTML 片段（styled infobox/card/chart）
      ↓ (存入 _includes/rich/)
  Jekyll 文章中的 {% include rich/data-card.html %}
      ↓ (GitHub Pages build)
  最终发布页面
```

**具体落地：**
1. 在 blog 的 `_includes/rich/` 目录存放生成的 HTML 片段
2. Jekyll posts 中通过 `{% include rich/xxx.html %}` 引入
3. 不影响现有 `_posts/*.md` 的写作流程
4. 新 posts 可选择性使用富 HTML 组件增强可读性蛥

---

## 四、推荐方案

### 方案 A：「最简集成」— clockless-org 作为 Agent Skill（推荐）

**投入：** 极低
**收益：**
- Agent 生成博客时自动将数据密集内容渲染为精美 HTML
- 表格/对比/数据卡片视觉效果大幅提升
- 零运行时依赖，完全兼容 GitHub Pages

**实施步骤：**
1. 在 blog 仓库创建 `_includes/rich/` 目录和 `.gitkeep`
2. 创建 CKEDIT `blog-publishing` skill（或更新已有 skill），加入 clockless-org/html-anything 作为子 prompt
3. 修改 Agent 的博客撰写 prompt：对数据密集型段落自动触发 html-anything 渲染
4. 创建 `_layouts/rich-post.html` 作为需要富 HTML 组件的文章布局（可选）
5. 写一篇 demo 文章验证效果

### 方案 B：「辅助工具」— nexu-io 作为独立创作工具

**投入：** 中等（需要安装 Node.js 环境）
**收益：** 可产出杂志/海报/数据报告等多种格式的精美 HTML
**限制：** 不能自动集成到 Jekyll 构建流程

**实施步骤：**
1. 在开发环境安装 nexu-io/html-anything
2. 作为 Agent 工具链的一个可选环节
3. 产出物手动提取并嵌入博客 (同方案A的嵌入方式)

### 建议

**先实施方案 A，方案 B 作为远期增强。**

---

## 五、blog-publishing skill 更新计划

需创建/更新以下 skill 内容：

```markdown
# blog-publishing skill 结构
- 核心流程：研究 → 撰写 → 格式增强 → 发布
- 新增模块：「富格式渲染」
  - 触发条件：内容含表格、多列数据对比、统计卡片、时间线
  - 处理方式：调用 clockless-org/html-anything prompt 生成 HTML 片段
  - 输出位置：_includes/rich/<post-slug>-<component>.html
  - Jekyll 引用：{% include rich/<post-slug>-<component>.html %}
- 约束：HTML 片段必须自包含（内联 CSS），不依赖外部 CDN（除 Google Fonts）
```

---

## 六、风险与注意事项

1. **HTML 片段膨胀：** 过多富 HTML 组件会使页面体积增大。建议每篇文章最多 去打-3 个富组件
2. **GitHub Pages 安全限制：** 自定义 HTML 不能包含 JS（会被 GitHub Pages 剥离或阻止）
3. **响应式：** 生成的 HTML 需适配博客的 720px max-width 阅读宽度
4. **字体一致性：** 需确保富组件使用的字体与博客主题 (Georgia/Noto Serif SC) 一致
5. **clockless-org 项目维护状态：** ⭐63 的小项目，需关注长期维护情况

---

**结论：推荐采用 clockless-org/html-anything 作为 Agent skill 层集成，方案可行且有明确收益，建议立即实施。**
