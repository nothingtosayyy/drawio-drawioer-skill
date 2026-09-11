<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/readme/hero.svg">
    <img src="./assets/readme/hero.svg" width="100%" alt="drawioer — 用自然语言描述，AI 生成可编辑的 draw.io 科研图表">
  </picture>
</p>

<p align="center">
  <b>drawioer</b> 是一个 Qoder Agent 技能，通过 AI 将自然语言描述直接转换为可编辑的 <a href="https://www.diagrams.net/">draw.io</a> 科研图表（.drawio 格式）——无需手动布局，无需切换工具，输出文件可在 diagrams.net 中继续修改。
</p>

<p align="center">
  <a href="#-什么是-drawioer">什么是 drawioer</a> ·
  <a href="#-核心优势">核心优势</a> ·
  <a href="#-快速开始">快速开始</a> ·
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
4. 用 **无头浏览器** 一键导出 PNG 截图，视口自动适配

最终交付的是**原生 `.drawio` 文件**——不是一张截图，而是一个你可以随时打开继续编辑的矢量图表。

## ✨ 核心优势

与其他制图方式相比，drawioer 的独特之处：

| | drawioer | 手动拖拽 draw.io | 截图/其他工具 |
|---|---|---|---|
| **输入方式** | 自然语言描述 → 自动生成 | 手动拖拽、对齐、调色 | 专业绘图软件 / 截图拼接 |
| **输出格式** | `.drawio`（完全可编辑） | `.drawio` | 静态图片，修改需重制 |
| **迭代方式** | 描述修改 → AI 自动调整 | 手动逐个元素调整 | 全部重做 |
| **质量保障** | 静态校验器 + 自动截图预览 | 肉眼检查 | 无 |
| **图表类型** | 流程图 / 泳道图 / 架构图 / 论文配图 | 全部 | 取决于工具 |
| **学习成本** | 描述即可 | 需熟悉 UI 和布局技巧 | 因工具而异 |

**核心差异：** drawioer 把制图从「操作型工作」变成了「描述型工作」——你说出想要什么，它负责布局、对齐、校验和出图。

## 🚀 快速开始

```bash
# 1. 一键环境检测
python <skill-dir>/scripts/preflight.py

# 2. 在对话中描述你的图表（AI 自动生成 .drawio 文件）

# 3. 本地预览
python <skill-dir>/scripts/serve_drawio_preview.py <file>.drawio --port 8765

# 4. 截图导出（视口自动适配）
python <skill-dir>/scripts/render_png.py <file>.drawio

# 5. 静态布局校验
python <skill-dir>/scripts/validate_drawio.py <file>.drawio
```

> 支持所有主流的 draw.io 图表类型：流程图、系统架构图、泳道图、模型方法图、ER 图、时序图……

## 🔄 工作流程

```
用户描述需求
       ↓
  AI 生成 mxGraph XML → 写入 .drawio 文件
       ↓
   静态校验（重叠 / 箭头 / 间距）
       ↓
   本地预览服务 / 一键截图导出
       ↓
   用户反馈 → AI 自动调整 → 再次校验
       ↓
      ✅ 交付可编辑的 .drawio + 截图
```

**迭代理念：** 支持多轮反馈调整。采用"先交付初稿，再逐步精修"的策略——第一版通过基础检查后立即给你看，后续按反馈精细调整，不做无意义的黑盒等待。

## 📋 适用场景

- **科研论文配图** — 方法架构图、模型流程图、实验 pipeline、系统概览
- **技术文档插图** — 系统架构图、网络拓扑、部署架构
- **会议演示素材** — 泳道图、时序图、流程图
- **方法复现与对比** — 参照已有论文图片复现，提取风格并适配

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
│   ├── preflight.py            # 环境预检（Python/浏览器/网络）
│   ├── render_png.py           # 无头浏览器截图（自动适配视口）
│   ├── validate_drawio.py      # 结构校验
│   ├── validate_visual_quality.py  # 视觉质量校验（快速/全量模式）
│   ├── serve_drawio_preview.py # 本地预览服务
│   └── make_drawio_preview.py  # 预览页生成
└── references/
    ├── drawio-workflow.md      # 完整工作流参考
    ├── xml-authoring.md        # mxGraph XML 编写指南
    ├── xml-preflight.md        # XML 预检规则
    ├── primitive-icons.md      # 内置图标（矩形/菱形/圆形等）
    ├── self-supervision-and-intake.md  # 自检与任务接收
    └── style-extraction.md     # 风格提取方法
```

## ⚙️ 环境要求

| 组件 | 用途 | 缺失时 |
|---|---|---|
| Python 3.8+ | 运行校验/预览/截图脚本 | 手动编写 XML，跳过自动校验 |
| Edge 或 Chrome | 截图导出 | 只用预览服务，手动截图 |
| 网络 | 加载 viewer.diagrams.net | XML 编写正常，预览/截图不可用 |
| diagrams.net 桌面版 | 手动精细编辑 | 可选，非必需 |

## 📄 许可

本项目参考了 [drawio-diagram-builder-skill](https://github.com/Will-hxw/drawio-diagram-builder-skill) 的设计思路，进行了定制化重构和功能增强。图标资源使用 [Tabler Icons](https://tabler-icons.io/)（MIT 许可）。