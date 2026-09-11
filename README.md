<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/readme/hero.svg">
    <img src="./assets/readme/hero.svg" width="100%" alt="drawioer — 用自然语言描述，AI 生成可编辑的 draw.io 图表">
  </picture>
</p>

<p align="center">
  <b>drawioer</b> 是一个 Qoder Agent 技能，通过 AI 将自然语言描述直接转换为可编辑的 <a href="https://www.diagrams.net/">draw.io</a> 图表（.drawio 格式）——无需手动布局，无需切换工具，输出文件可在 diagrams.net 中继续修改。
</p>

<p align="center">
  <a href="#-什么是-drawioer">什么是 drawioer</a> ·
  <a href="#-核心优势">核心优势</a> ·
  <a href="#-设计理念">设计理念</a> ·
  <a href="#-工作流程">工作流程</a> ·
  <a href="#-适用场景">适用场景</a> ·
  <a href="#-目录结构">目录结构</a>
</p>

---

## 🎯 什么是 drawioer

drawioer 是一个 **AI 驱动的 draw.io 图表生成引擎**。你只需用自然语言描述想要的图表，它会：

1. 生成规范的 **mxGraph XML**，写入 `.drawio` 文件
2. 通过 **静态校验器** 自动检查布局问题（重叠、箭头穿透、间距异常）
3. 启动 **本地预览服务**，在浏览器中实时查看

最终交付的是**原生 `.drawio` 文件**——不是一张截图，而是一个你可以随时打开继续编辑的矢量图表。

## ✨ 核心优势

- **描述即生成** — 说清楚你要什么，AI 自动完成布局、对齐和连接
- **可编辑的交付物** — 输出 `.drawio` 格式，可在 diagrams.net 中继续修改
- **质量内建** — 静态校验器在出图前发现重叠、箭头穿透、间距异常等问题
- **迭代友好** — 先交付初稿，再按反馈逐步精修
- **与 draw.io 生态兼容** — 支持所有 draw.io 原生特性：泳道图、层级分组、自定义样式、内联图标

## 💡 设计理念

```
自然语言描述
       ↓
  AI 理解并生成 mxGraph XML → 写入 .drawio
       ↓
   静态校验（重叠 / 箭头 / 间距）
       ↓
   本地预览服务
       ↓
   反馈调整 → 再次校验
       ↓
   交付 .drawio 文件
```

**先交付，再精修。** 第一版通过基础检查后立即给你看，不让你在黑盒等待中空转。后续按反馈逐步调整，直到你满意为止。

## 🔄 工作流程

1. **描述** — 在对话中用自然语言描述你想要的图表
2. **生成** — AI 生成 mxGraph XML，写入 `.drawio` 文件
3. **预览** — 启动本地预览服务，在浏览器中实时查看
4. **校验** — 静态校验器自动检查布局问题
5. **迭代** — 反馈调整 → 再次校验，直到满意
6. **交付** — 输出 `.drawio` 文件

## 📋 适用场景

- **系统架构图、流程图、泳道图**
- **技术文档 / API 文档插图**
- **方法模型图、时序图、ER 图**
- **快速原型与方案沟通**

## 📦 目录结构

```
drawioer/
├── SKILL.md                    # Agent 技能定义（调用入口）
├── README.md                   # 本文件
├── CHANGELOG.md                # 版本日志
├── VERSION
├── assets/
│   ├── readme/                 # README 视觉素材
│   └── icons/tabler/outline/   # Tabler 开源图标库（MIT）
├── scripts/
│   ├── preflight.py            # 环境预检
│   ├── render_png.py           # 截图导出（可选）
│   ├── validate_drawio.py      # 结构校验
│   ├── validate_visual_quality.py  # 视觉质量校验
│   ├── serve_drawio_preview.py # 本地预览服务
│   └── make_drawio_preview.py  # 预览页生成
└── references/
    ├── drawio-workflow.md      # 完整工作流参考
    ├── xml-authoring.md        # mxGraph XML 编写指南
    ├── xml-preflight.md        # XML 预检规则
    ├── primitive-icons.md      # 内置图标
    ├── self-supervision-and-intake.md
    └── style-extraction.md     # 风格提取方法
```

## 📄 许可

本项目参考了 [drawio-diagram-builder-skill](https://github.com/Will-hxw/drawio-diagram-builder-skill) 的设计思路，进行了定制化重构和功能增强。图标资源使用 [Tabler Icons](https://tabler-icons.io/)（MIT 许可）。