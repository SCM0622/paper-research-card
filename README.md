# 论文调研卡片 skill

## 用途

把单篇或一批论文 PDF 整理为固定模板的中文调研卡片，保留研究问题、方法、实验条件、结果、局限、复现信息和证据页码。适合论文精读、组会准备及专题文献调研。不适用于全文翻译，也不会在缺少论文原文时生成事实性评价。

## 仓库结构

```text
paper-research-card/
├── SKILL.md                 # AI 执行规程、边界与防幻觉要求
├── references/
│   └── card-template.md     # 固定调研卡片模板
├── scripts/
│   └── extract_pdf.py       # 逐页提取文字并记录读取状态
├── example.md               # 实战报告入口
├── example.pdf              # 作者修改后的正式实战报告
└── README.md                # 安装与使用说明
```

## 安装到 Codex

将本文件夹复制到 Codex 用户技能目录 `~/.codex/skills/paper-research-card`，保留目录结构。如果配置了 `CODEX_HOME`，则使用该目录下的 `skills/paper-research-card`。如果目标目录已有同名技能，先备份，再决定是否更新。

Windows 默认位置为 `%USERPROFILE%\.codex\skills\paper-research-card`。确认该目录下直接包含 `SKILL.md`，不要额外嵌套一层同名文件夹。

## 使用

使用示例：`请用 $paper-research-card 把这份论文 PDF 整理成中文调研卡片。`
也支持：`把这个目录中的论文 PDF 批量整理为调研卡片，并生成索引。`

请同时附上 PDF 或给出实际文件路径。默认输出为工作区内的 `outputs/paper-cards/`；批量处理会附带成功、部分完成及失败状态索引。

固定模板位于 `references/card-template.md`，可按实验室需要修改。关键事实使用 `[PDF p.3，表2]` 标注物理页码，从 1 开始。

## 提取脚本

脚本依赖 Python 3 和 `pypdf`。先选择已有该依赖的 Python；Codex 桌面可查找捆绑运行时。独立环境可安装：

```powershell
python -m pip install pypdf
```

在仓库根目录运行（把输入路径替换为真实论文路径）：

```powershell
python scripts/extract_pdf.py "paper.pdf" "work/paper-pages.json"
```

输入必须为存在的 PDF，输出路径必须尚不存在。JSON 包含源文件路径、SHA-256、总页数、每页文字及状态。脚本只负责提取，不会自行调用模型或生成卡片。Codex 根据提取结果阅读原文、核验并填写模板。

扫描件需另用视觉读取或 OCR，脚本不提供 OCR。空白页和无可提取文字的页会标记为 `needs_visual_or_ocr`；加密且无法以空密码解锁的文件会报错。复杂图表和双栏排版需要回看原页核验。

## 质量与测试范围

已使用合成空白 PDF 验证：物理页码从 1 开始、空白页触发人工/视觉核验提示、已有输出不会被覆盖。这仅是脚本冒烟测试，不是科研实测。

官方 `quick_validate.py` 曾因测试环境缺少 PyYAML 未能运行完成；不能据此宣称已通过官方校验。真实论文的提取质量及卡片事实准确性应在 `example.md` 中据实记录。

## 作业报告

作者修改后的实战报告见 `example.pdf`；`example.md` 保留为报告入口，以对应作业要求的文件结构。公开仓库与邮件提交由使用者自行完成；发布前检查报告和截图中是否包含个人敏感信息或不宜公开的论文材料。

