# assets/ — 内置资源

本目录存放技能运行所需的静态资源，共两个子目录。

## icons/ — 内置图标库（102 个文件）

| 内容 | 说明 |
|---|---|
| `ICON-MANIFEST.md` | 图标清单：可用图标名与对应文件 |
| `tabler/outline/*.svg` | [Tabler Icons](https://tabler.io/icons)（MIT 许可）的 outline 风格 SVG，如 `api.svg`、`alert-triangle.svg`、`arrow-loop-right.svg` |

**用法**：绘制图表时优先从内置图标中选择，并以**可编辑图元**（draw.io shape / SVG path）方式嵌入 XML，避免使用位图。下载任何外部图标之前，先查 `ICON-MANIFEST.md` 与 `references/primitive-icons.md`。

## reference-images/ — 风格参考图（兜底素材）

| 内容 | 说明 |
|---|---|
| `REFERENCE-IMAGES.md` | 参考图清单与用途说明 |
| `topconf-*.png` | 4 张顶会论文风格的参考图（架构图、RL 流水线、知识挖掘流水线、记忆路由等），每张约 1 MB |

**用法**：当缺少用户参考图、又需要演示论文级图风格时，作为风格提取的兜底参考素材；仅在风格层面参考（色板、布局习惯、字体层级），不引用其中任何具体数据内容。
