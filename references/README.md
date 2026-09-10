# references/ — 参考文档

按需加载的细则文档。`SKILL.md` 只保留原则与流程主干，具体规范分散在本目录，使用时按场景加载对应文件。

| 文件 | 说明 |
|---|---|
| `drawio-workflow.md` | 端到端工作流细则：Intake → 规划 → 预检 → 迭代循环 → 交付 |
| `self-supervision-and-intake.md` | 任务分诊（Intake）、审查分区、退出纪律 |
| `reference-replication-protocol.md` | 参考图复刻协议：各保真级别（L1/L2/L3）的复刻要求与交付物 |
| `xml-preflight.md` | 预检规则详解（重叠、箭头碰撞、文字溢出、间距、配色等） |
| `xml-authoring.md` | XML 编写模式：几何布局、样式、可编辑图元写法 |
| `style-extraction.md` | 从参考图提取风格契约（色板、字体、圆角、层级） |
| `topconf-paper-style.md` | 顶会论文图风格规范 |
| `primitive-icons.md` | 可编辑图标配方：用基本图元拼出图标，避免位图 |

## 加载建议

| 场景 | 建议加载 |
|---|---|
| 复刻 / 风格匹配任务 | `reference-replication-protocol.md` + `style-extraction.md` |
| 每轮预检与收敛判断 | `xml-preflight.md` + `self-supervision-and-intake.md` |
| 编写 / 修复 XML 时 | `xml-authoring.md` + `primitive-icons.md` |
| 论文图风格任务 | `topconf-paper-style.md` |
