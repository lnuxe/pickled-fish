# 安装指南 / Installation Guide

## Claude Code

### 项目级安装（推荐）

在你的 git 仓库根目录执行：

```bash
mkdir -p .claude/skills
git clone https://github.com/NatalieCao323/partner-skill .claude/skills/create-partner
```

安装完成后，在该项目的任意 Claude Code 会话中输入 `/create-partner` 即可启动。

### 全局安装

适用于所有项目：

```bash
git clone https://github.com/NatalieCao323/partner-skill ~/.claude/skills/create-partner
```

### 依赖

无需安装额外依赖。所有工具脚本仅使用 Python 3 标准库（`json`、`os`、`argparse`、`pathlib`、`shutil`、`datetime`）。

确认 Python 3 已安装：

```bash
python3 --version
```

---

## OpenClaw

### 手动安装

```bash
# 安装到全局 skills 目录
git clone https://github.com/NatalieCao323/partner-skill ~/.openclaw/workspace/skills/create-partner
```

安装完成后，在 OpenClaw 的 Skills 界面中找到 `create-partner` 并启用。

### 路径说明

OpenClaw 使用 `{baseDir}` 替代 Claude Code 的 `${CLAUDE_SKILL_DIR}`。SKILL.md 中的所有工具调用路径已自动适配，无需手动修改。

---

## 使用步骤

### 第一步：启动

```
/create-partner
```

### 第二步：回答 3 个问题

```
1. 花名/代号（必填）
   例：小明、M、我男朋友

2. 基本信息（可跳过）
   例：男 26岁 设计师

3. 性格画像（可跳过）
   例：INFP 天蝎座 焦虑型依恋 爱的语言是肯定话语
```

### 第三步：提供原材料

选择以下任意方式：

```
[A] 聊天记录导出文件（微信 TXT/JSON、iMessage、短信）
[B] 聊天截图（直接上传图片）
[C] 直接粘贴聊天内容
[D] 仅凭描述（无需任何文件）
```

### 第四步：确认并保存

AI 会生成关系健康报告预览，确认后保存到 `./partners/{slug}/` 目录。

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `/create-partner` | 创建新的现任 Skill |
| `/update-partner {slug}` | 追加新数据或纠正画像 |
| `/list-partners` | 列出所有已创建的现任 |
| `/versions {slug}` | 查看某个现任的版本历史 |
| `/rollback {slug} {version_id}` | 回滚到某个历史版本 |
| `/delete-partner {slug}` | 永久删除某个现任画像 |

---

## 常见问题

**Q: 只有文字描述，没有聊天记录，能用吗？**
A: 可以。选择方式 D，直接描述 ta 的性格和你们的互动模式，AI 会基于描述生成画像。

**Q: 支持哪些聊天记录格式？**
A: 微信导出的 TXT/JSON、iMessage 导出、短信备份文件，以及任何纯文本格式的聊天记录。

**Q: 生成的数据存在哪里？**
A: 存储在本地 `./partners/{slug}/` 目录下，不上传到任何服务器。

**Q: 可以同时管理多个现任吗？**
A: 可以。每个现任有独立的 slug，用 `/list-partners` 查看所有已创建的画像。

**Q: 如何更新画像？**
A: 用 `/update-partner {slug}` 追加新聊天记录，或直接告诉 AI "这不对，ta 其实是……" 进入纠错模式。
