# drawioer

通过 AI 生成可直接编辑的 [draw.io](https://www.diagrams.net/) 科研图表（.drawio 格式），支持流程图、系统架构图、泳道图、模型方法图等多种类型。

## 核心能力

- **AI 生成 drawio 文件**：从自然语言描述生成规范的 mxGraph XML
- **本地预览**：通过 `serve_drawio_preview.py` 启动本地 Web 服务，在浏览器中实时查看
- **自动截图**：`render_png.py` 利用无头浏览器自动导出 PNG，视口自适应
- **静态校验**：`validate_drawio.py` 检查重叠、对齐、间距等常见布局问题
- **环境检测**：`preflight.py` 一站式检查 Python、浏览器、网络等前置依赖
- **泳道图支持**：正确处理嵌套坐标与容器关系，消除误报

## 快速开始

```bash
# 1. 环境检测
python <skill-dir>/scripts/preflight.py

# 2. 生成图表（AI 会直接在对话中产出 .drawio 文件）

# 3. 预览
python <skill-dir>/scripts/serve_drawio_preview.py <file>.drawio --port 8765

# 4. 截图导出
python <skill-dir>/scripts/render_png.py <file>.drawio

# 5. 静态校验
python <skill-dir>/scripts/validate_drawio.py <file>.drawio
```

## 工作流程

1. **需求输入**：描述图表主题、类型、结构、风格偏好
2. **AI 生成**：Agent 生成 mxGraph XML 写入 `.drawio` 文件
3. **校验反馈**：静态校验器快速检查布局问题，Agent 自动修复
4. **预览交付**：启动本地预览或截图导出，确认无误后交付

## 目录结构

```
drawioer/
├── SKILL.md              # Agent 技能定义
├── README.md
├── CHANGELOG.md
├── VERSION
├── scripts/
│   ├── preflight.py             # 环境检测
│   ├── render_png.py            # 无头浏览器截图
│   ├── validate_drawio.py       # 静态布局校验
│   ├── serve_drawio_preview.py  # 本地预览服务
│   └── make_drawio_preview.py   # 预览页生成
├── references/
│   ├── drawio-workflow.md       # 完整工作流说明
│   ├── xml-authoring.md         # mxGraph XML 编写指南
│   ├── xml-preflight.md         # XML 预检规则
│   ├── primitive-icons.md       # 基础图标库
│   ├── self-supervision-and-intake.md
│   └── style-extraction.md      # 风格提取指南
└── assets/icons/
    └── tabler/outline/          # Tabler 开源图标（SVG）
```

## 要求

- Python 3.8+
- Microsoft Edge 或 Chrome（用于截图导出）
- 可选：diagrams.net 桌面版（用于手动编辑）

## 参考

本项目的 `scripts/` 和 `references/` 目录参考了 [drawio-diagram-builder-skill](https://github.com/Will-hxw/drawio-diagram-builder-skill) 的设计思路。