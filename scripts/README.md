# scripts/ — Python 工具链

技能自带的 6 个脚本（要求 Python 3.7+，已针对 Windows 控制台做 UTF-8 输出处理）。

| 脚本 | 用途 | 关键参数 |
|---|---|---|
| `validate_visual_quality.py` | 渲染前静态预检：箭头-方框碰撞、文字溢出风险、间距、配色、装饰、密度 | `--quick`（草案期快检：仅显示级硬伤）；`--waive <rule>`（将指定 FAIL 降级为非阻塞 WAIVED，需记录理由）；`--json` / `--strict` / `--rules` |
| `validate_drawio.py` | 交付前结构校验（可用于 CI） | `--strict`、`--json` |
| `validate_replication_artifacts.py` | 复刻任务交付物完整性检查（按保真级别） | `<workdir> --level L1\|L2\|L3 [--require-screenshot-review]` |
| `serve_drawio_preview.py` | 本地短 URL 预览服务（经 postMessage 把 XML 载入 diagrams.net） | `<file>.drawio --port 8765` |
| `make_drawio_preview.py` | 生成独立预览 HTML（可配合 `python -m http.server` 使用） | `<file>.drawio --out <preview.html>` |
| `check_skill_update.py` | 本地版本与上游比对（本仓库为定制版，会提示覆盖风险） | `--skill-dir <dir> --latest-version <ver>` |

## 常用命令

```powershell
# 草案期快检（只查显示级硬伤：重叠 / 箭头穿框 / 严重文字溢出）
python scripts/validate_visual_quality.py diagram.drawio --quick

# 定稿期全检
python scripts/validate_visual_quality.py diagram.drawio

# 结构校验
python scripts/validate_drawio.py diagram.drawio

# 本地预览（打开后等待 3-5 秒等待 diagrams.net 渲染）
python scripts/serve_drawio_preview.py diagram.drawio --port 8765
# → http://127.0.0.1:8765/drawio-preview.html?rev=1
```

## 注意事项

- 预览 HTML 在生成时即内嵌 XML：**每次修改 XML 后需重新生成预览**，并递增 `?rev=N` 以绕过缓存。
- 截图作为审查证据时：只截画布区域、图表占比 ≥80%，整窗截图无效。
- 具体规则名与规则列表可用 `--rules` 查看；豁免（`--waive`）只改变阻塞性，不隐藏问题，理由仍需记录在缺陷日志中。
