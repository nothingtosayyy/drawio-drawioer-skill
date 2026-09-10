# drawio-diagram-builder

> 仓库：`drawio-drawioer-skill` ｜ 技能名：`drawio-diagram-builder` ｜ 版本：**0.5.0**（本地定制版）

面向 AI Agent 的 **diagrams.net / draw.io 图表构建技能**：把需求描述、论文、代码仓库或参考图，变成**可编辑**的 `.drawio` 图表；流程按任务规模自动缩放 —— 先交付初稿、再按需完善。

> **本仓库是本地定制版**，由上游 [drawio-diagram-builder-skill](https://github.com/Will-hxw/drawio-diagram-builder-skill)（v0.4.1）重写而来，修复了“无上限迭代 + 一刀切硬门禁”导致小任务陷入“执行 → 检查”死循环的问题。完整改动明细见 [CHANGELOG.md](CHANGELOG.md)。

## 核心设计

| 原则 | 说明 |
|---|---|
| **先交付，再完善** | 初稿通过快检后立即交付（文件 + 预览链接），不把首次亮相埋在完整审查循环后面（draft-first 为默认策略） |
| **检查强度分阶段** | 草案期只跑快检（重叠 / 箭头穿框 / 严重文字溢出）；**定稿时才全检**，输出 P0/P1/P2 问题清单供用户勾选修复 |
| **入口阻断门** | Step 0 Intake 必须先问清：保真级别（L1 结构 / L2 布局 / L3 像素）、迭代预算、交付物、交付策略；未获答复（或明确委托）不得开工，L3 永不静默默认 |
| **分级门禁** | L1 / L2 / L3 各自适用哪些门禁由 Gate Matrix 单点定义；配额机制（凑缺陷数、自评分卡硬门槛）全部废除 |
| **预算化收敛** | 至多 N 轮（L1=1 / L2=2 / L3=3，可自定义），达标即停；预算耗尽时带“差距清单”交付 |
| **用户持有控制权** | 每个接触点（初稿交付 / 进度汇报 / 最终交付）都用用户语言明示当前可用的具体指令（如“定稿 / 做终检”） |
| **优雅降级** | 缺 Python / 浏览器自动化 / 联网 / 读图能力时降级运行，而不是中止 |

## 工作流一览

```
Step 0  Intake（阻断门：一次问清 4 项）
   ↓
规划（先定义每条连线语义；有参考图先提取风格）
   ↓
编写 XML
   ↓
快检 --quick ──► 本地预览（默认 8765 端口）
   ↓
初稿交付（draft-first：快检通过立即交付 + 明示可用指令）
   ↓
草案期迭代（仅重跑快检）
   ↓
【定稿阶段】完整预检 + 截图审查（L3 加一轮红队）→ P0/P1/P2 问题清单 → 用户勾选修复
   ↓
最终交付（文件 + 截图 + 对比图 + 问题清单 + 差距清单）
```

## 目录结构

```
.
├── SKILL.md           技能主文件：核心原则、Step 0 Intake、门禁矩阵、标准工作流、失败降级
├── VERSION            当前版本号（0.5.0 本地定制版）
├── CHANGELOG.md       变更记录：相对上游 v0.4.1 的完整改动明细
├── agents/            接口声明：面向 Agent 客户端的显示名与默认提示词  → agents/README.md
├── assets/            内置资源：图标库（Tabler MIT）+ 风格参考图        → assets/README.md
├── references/        按需加载的参考文档（8 份）                        → references/README.md
└── scripts/           Python 工具链（预检 / 结构校验 / 交付物检查 / 预览 / 版本比对）→ scripts/README.md
```

## 环境要求

| 依赖 | 用途 | 缺失时 |
|---|---|---|
| Python 3.7+ | 预览与校验脚本 | 手写 XML，跳过脚本检查并说明 |
| 浏览器自动化（Playwright MCP / Puppeteer MCP 等） | 截图审查 | 降级：静态预检 + 请用户目视预览 |
| 读图能力 | 参考图风格提取与保真对比 | 请用户提供色值；声明无法验证像素级保真 |
| 联网 | 预览需嵌入 `embed.diagrams.net` | 仅 XML 编写可用，预览不可用 |

## 安装

将本仓库目录克隆 / 复制到 Agent 的技能目录即可（例如 Qoder 等支持 SKILL.md 规范的客户端）：

```
~/.agents/skills/drawio-diagram-builder/
```

> ⚠️ 从上游仓库重装会覆盖本地定制内容，请先合并再安装。

## 版本

- 当前版本：**0.5.0**（2026-09-10 本地定制版）
- 变更明细：[CHANGELOG.md](CHANGELOG.md)

## 致谢

- 上游项目：[Will-hxw/drawio-diagram-builder-skill](https://github.com/Will-hxw/drawio-diagram-builder-skill)
- 图标资源：[Tabler Icons](https://tabler.io/icons)（MIT 许可），清单见 `assets/icons/ICON-MANIFEST.md`
