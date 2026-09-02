# pickled-fish · 泡菜鱼

macOS **微信本机导出** + **可插拔心理学/情感/关系/社交知识库** + **文件系统 RAG 编排**。

> **先读 [DISCLAIMER.md](DISCLAIMER.md)。** 非官方 · 仅限本人数据 · 情感建议非专业咨询 · 风险自负。

## 架构

```
wechat-export → chat.txt → local-chat 统计
                              ↓
                         kb-rag 选包
                              ↓
        psych-foundations 地图 / 理论包 / 实操包 / custom
```

| 层 | 路径 |
|----|------|
| 总控 | [SKILL.md](SKILL.md) |
| RAG 编排 | [skills/kb-rag](skills/kb-rag/) |
| 知识总目录 | [knowledge/REGISTRY.md](knowledge/REGISTRY.md) |
| 导出 | [skills/wechat-mac-export](skills/wechat-mac-export/) |

## 已整合知识域（摘要）

- **依恋 / ECR-R**：attachment-ecr、dating-master、lovelab、chatrel  
- **Gottman / 伴侣互动**：lovelab、chatrel、rel-consult  
- **NVC / 沟通谈判**：nvc、howtotalk（13 框架）  
- **Sternberg / Knapp / 社交渗透**：chatrel docs  
- **中文恋爱实操**：qingsheng、partner  
- **课程地图**：psych-foundations（理论 → pack 路由）  

完整表与可选远端包见 REGISTRY。安装远端：

```bash
bash scripts/add-pack.sh psych-summaries https://github.com/cognitivetech/Psychology-Summaries
```

## 安装

```bash
git clone https://github.com/lnuxe/pickled-fish.git ~/.cursor/skills/pickled-fish
bash ~/.cursor/skills/pickled-fish/scripts/install-skills.sh
```

## 许可与致谢

[LICENSE](LICENSE) · [NOTICE](NOTICE) · [DISCLAIMER](DISCLAIMER.md)
