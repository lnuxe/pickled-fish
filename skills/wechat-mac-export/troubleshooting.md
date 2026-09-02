# 故障排查

## 内存扫密钥得到 `0 keys` / Found 0 encrypted DBs

**原因（WeChat 4.1.10+）**：进程内存往往不再缓存明文 DB key；内存扫描为空是常见现象。

另：在 `sudo` 下扫描时若出现 `User home: /var/root`，会扫不到用户目录下的数据库。

**处理**：改用 wcdb-key-tool `extract --decrypt`，不要反复跑内存扫密钥。

若仅需修正 HOME 再试（通常仍为 0 keys）：

```bash
sudo SUDO_USER="$USER" HOME="$HOME" \
  "$(npm root -g)/@walkerch/wxecho/py/find_all_keys_macos"
```

---

## `task_for_pid failed: 5`

微信未做 ad-hoc 重签名，或签名被更新覆盖。

```bash
sudo codesign --force --deep --sign - /Applications/WeChat.app
# 完全退出微信后重开
```

---

## wcdb extract 后目录属 root / permission denied

`~/decrypted` 常被写成 root 所有。

```bash
sudo cp -R ~/decrypted ~/wechat-decrypted
sudo chown -R "$(whoami)" ~/wechat-decrypted
```

查询时用 `~/wechat-decrypted`，不要直接读 root 库。

---

## `export` 找不到解密库 / 导出空

1. 确认工具 `config.json` 里 `decrypted_dir` → `~/wechat-decrypted`
2. 语法以当前 CLI 为准：常见为 `wxecho export "昵称"`（**不要**照搬过时的 `-n` 写法）
3. 昵称须与联系人显示名/备注一致 → 用 list 功能或 sqlite 查 `contact`

---

## 导出到错账号

机器上可能有多个 `wxid_*`。以 `message_0.db` **体积 + mtime** 选主号。

```bash
for d in ~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_*/db_storage; do
  echo "=== $d ==="
  du -sh "$d" 2>/dev/null
  ls -lt "$d/message/message_0.db" 2>/dev/null
done
```

---

## 关闭 SIP

部分 key-scan 工具要求关闭 SIP。本 skill **不推荐**为此关闭 SIP；优先 wcdb-key-tool。

---

## 微信更新后再次失败

更新可能覆盖 ad-hoc 签名并使旧解密库过期：

1. 重新 `codesign`
2. 再跑一次 `extract --decrypt`
3. 再 export

---

## 已有 passphrase、想重新解密

若 `~/.wcdb-key-tool/wechat-passphrase.json` 仍在，多数情况无需重登。子命令以 wcdb-key-tool 仓库 README 为准；失败则完整重跑 `extract --decrypt`。
