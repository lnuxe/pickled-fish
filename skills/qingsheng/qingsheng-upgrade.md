# /qingsheng-upgrade — 升级情圣技能

升级 qingsheng-skill 到最新版本。

## 触发方式

用户说 `/qingsheng-upgrade` 或"升级情圣技能"时执行本流程。

---

## 执行步骤

### Step 1：检测安装位置和类型

按优先级查找安装目录：

```
~/.cursor/skills/qingsheng-skill/     ← Cursor global git repo（优先）
~/.cursor/skills/qingsheng/           ← Cursor deployed skill
~/.claude/skills/qingsheng-skill/     ← Claude Code global
.claude/skills/qingsheng-skill/       ← Claude Code local（项目级）
```

用 Bash 工具：
```bash
# 检测 Cursor git repo
ls ~/.cursor/skills/qingsheng-skill/.git 2>/dev/null && echo "cursor-git"
# 检测 Cursor deployed
ls ~/.cursor/skills/qingsheng/VERSION 2>/dev/null && echo "cursor-deployed"
# 检测 Claude global
ls ~/.claude/skills/qingsheng-skill/VERSION 2>/dev/null && echo "claude-global"
# 检测 Claude local
ls .claude/skills/qingsheng-skill/VERSION 2>/dev/null && echo "claude-local"
```

### Step 2：读取当前版本

```bash
cat ~/.cursor/skills/qingsheng/VERSION 2>/dev/null \
  || cat ~/.claude/skills/qingsheng-skill/VERSION 2>/dev/null \
  || echo "unknown"
```

### Step 3：检查远端最新版本

```bash
curl -fsSL https://raw.githubusercontent.com/tomwong001/qingsheng-skill/main/VERSION 2>/dev/null
```

如果当前版本 == 远端版本：告知用户已是最新，结束。

### Step 4：执行升级

**Cursor Git 管理的安装（~/.cursor/skills/qingsheng-skill/.git 存在）**：
```bash
git -C ~/.cursor/skills/qingsheng-skill pull --ff-only
cp -r ~/.cursor/skills/qingsheng-skill/skill/* ~/.cursor/skills/qingsheng/
cp ~/.cursor/skills/qingsheng-skill/VERSION ~/.cursor/skills/qingsheng/
cp ~/.cursor/skills/qingsheng-skill/CHANGELOG.md ~/.cursor/skills/qingsheng/ 2>/dev/null || true
# 同步子命令 skills
for subcmd in 展示面 挽回 换一个 自动 急; do
  cp ~/.cursor/skills/qingsheng-skill/skill/${subcmd}.md ~/.cursor/skills/${subcmd}/SKILL.md
done
cp ~/.cursor/skills/qingsheng-skill/skill/qingsheng-upgrade.md ~/.cursor/skills/qingsheng-upgrade/SKILL.md
```

**Claude Code Git 管理的安装（有 .git 目录）**：
```bash
git -C ~/.claude/skills/qingsheng-skill pull --ff-only
```

**Vendored 安装（无 .git）**：
```bash
# 下载最新 tarball 并替换 skill/ 目录
TMP=$(mktemp -d)
curl -fsSL https://github.com/tomwong001/qingsheng-skill/archive/refs/heads/main.tar.gz \
  | tar -xz -C "$TMP" --strip-components=1
# Cursor 路径
if [ -d ~/.cursor/skills/qingsheng ]; then
  cp -r "$TMP/skill/"* ~/.cursor/skills/qingsheng/
  cp "$TMP/VERSION" ~/.cursor/skills/qingsheng/
  cp "$TMP/CHANGELOG.md" ~/.cursor/skills/qingsheng/ 2>/dev/null || true
fi
# Claude 路径
if [ -d ~/.claude/skills/qingsheng-skill ]; then
  cp -r "$TMP/skill/"* ~/.claude/skills/qingsheng-skill/skill/
  cp "$TMP/VERSION" ~/.claude/skills/qingsheng-skill/
  cp "$TMP/CHANGELOG.md" ~/.claude/skills/qingsheng-skill/ 2>/dev/null || true
fi
rm -rf "$TMP"
```

### Step 5：读取 CHANGELOG，汇报改动

```bash
cat ~/.cursor/skills/qingsheng/CHANGELOG.md 2>/dev/null | head -60 \
  || cat ~/.claude/skills/qingsheng-skill/CHANGELOG.md 2>/dev/null | head -60
```

从 CHANGELOG 中提取本次升级的变更，用中文 3-5 条 bullet 告知用户。

### Step 6：更新版本记录

```bash
cat ~/.cursor/skills/qingsheng/VERSION 2>/dev/null \
  || cat ~/.claude/skills/qingsheng-skill/VERSION 2>/dev/null \
  > ~/.qingsheng/installed-version
date -u +%s > ~/.qingsheng/last-update-check
```

---

## 输出格式

```
✅ 情圣技能已升级：v{旧版本} → v{新版本}

本次更新：
• [变更1]
• [变更2]
• [变更3]
```

---

## 平台兼容性

- **macOS / Linux**：`~/.claude/skills/`，路径用 `$HOME`
- **Windows (MINGW/MSYS/WSL)**：
  - MINGW/MSYS：`$APPDATA/.claude/skills/`
  - WSL：使用 Linux 路径 `~/.claude/skills/`
  - 用 `uname -s` 检测：`MINGW*|MSYS*|CYGWIN*` → Windows 原生

检测 Windows：
```bash
case "$(uname -s 2>/dev/null)" in
  MINGW*|MSYS*|CYGWIN*) INSTALL_DIR="$APPDATA/.claude/skills/qingsheng-skill" ;;
  *) INSTALL_DIR="$HOME/.claude/skills/qingsheng-skill" ;;
esac
```

---

## 异常处理

| 情况 | 处理 |
|------|------|
| 找不到安装目录 | 提示运行 `bash setup` 重新安装 |
| curl 失败 / 无网络 | 告知网络问题，跳过 |
| git pull 有冲突 | `git stash && git pull --ff-only` |
| 版本文件损坏 | 强制重新下载 |
