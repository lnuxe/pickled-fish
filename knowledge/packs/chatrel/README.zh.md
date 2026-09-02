# ChatRel · 关系对话心理学分析工具

### **[🚀 在线 Demo（不需要安装直接看）→](https://ruanflux.github.io/chatrel/)**


**把 7 个经过实证研究的心理学框架应用到你和伴侣的聊天记录上。全本地、不联网。支持中英文。**

[English README](README.md) · [方法论](docs/methodology.md) · [局限](docs/limitations.md) · [数据格式](docs/schema.md)

---

大多数聊天分析工具给你的就是词云、情感曲线、热力图。ChatRel 反过来：它把你和伴侣几个月对话里真实产生的互动信号，对接到关系学者们实际研究了 40 多年的框架上：

| 框架 | 度量内容 | 核心文献 |
|---|---|---|
| **Sternberg 三元爱情** | 亲密 × 激情 × 承诺 三可分离维度 | Sternberg (1986) |
| **Knapp 关系阶段** | 10 阶段模型 (开端 → 结合, 分化 → 终止) | Knapp (1978) |
| **ECR-R 依恋** | 焦虑 × 回避双维度, 映射到 Bartholomew 四分类 | Fraley et al. (2000); Bartholomew & Horowitz (1991) |
| **Gottman 5:1 + 四骑士** | 正负情感比; 批评/蔑视/防御/筑墙密度 | Gottman (1994) |
| **社会渗透** | 自我披露从表层到核心三层 | Altman & Taylor (1973) |
| **临界减速预警 (EWS)** | 方差与自相关上升作为相变前兆 | Scheffer et al. (2009) |
| **LIWC 中文代理** | 功能词 / 认知 / 情感过程代理词典 | Pennebaker et al. |

**输出**: 7 份联动的交互 HTML 报告 (Plotly) + 精选记忆书 + 总门户。全部在你的机器上完成, 数据不外发。

## 截图

`docs/screenshots/` 下是基于 `sample_data/` 合成数据生成的 demo 图。

## 安装

```bash
git clone https://github.com/ruanflux/chatrel.git
cd chatrel
pip install -e .
```

需要 Python 3.10+。依赖: `jieba`、`snownlp`、`pandas`、`numpy`、`plotly`。

## 体验 (不需要真实数据)

```bash
chatrel sample --out sample_data/synthetic_couple.json
chatrel analyze sample_data/synthetic_couple.json --out ./output
start ./output/index.html
```

这会生成一份约 2000 条、90 天的虚构情侣对话 (包含所有分析器寻找的信号), 然后跑完完整流水线。`output/` 里全是基于假数据的结果, 可随意截图。

## 接入真实数据

ChatRel 读取标准聊天 JSON ([docs/schema.md](docs/schema.md)):

```json
{
  "me_name": "Alex",
  "partner_name": "Sam",
  "messages": [
    {"ts": 1700000000, "role": "me", "text": "在吗", "type": "text"},
    {"ts": 1700000010, "role": "partner", "text": "在"}
  ]
}
```

### 转换适配器

* **Telegram**: Telegram Desktop → 设置 → 高级 → 导出数据 → JSON, 然后
  ```bash
  python -m chatrel.adapters.telegram result.json --out chat.json
  ```
* **微信**: ChatRel **不内置**微信解密。请查看 [`src/chatrel/adapters/wechat.py`](src/chatrel/adapters/wechat.py), 里面说明了用外部工具 (如 `ylytdeng/wechat-decrypt` 或 `PyWxDump`) 解密后如何用 ChatRel 的 helper 读取。
* **通用 CSV/JSON**: `python -m chatrel.adapters.generic path.csv --out chat.json`

自己写适配器也很简单 —— 只要最终返回一个 `chatrel.schema.Chat` 即可。

## CLI

```bash
chatrel sample                      # 生成合成 demo 数据
chatrel analyze chat.json --out ./output
                                    # 跑所有分析器 + 总门户
chatrel depth      chat.json        # Sternberg + Knapp + IDS
chatrel attachment chat.json        # ECR-R + Gottman + 12 周预测
chatrel conflict   chat.json        # 冲突-修复事件
chatrel external   chat.json        # 挖墙脚/抗性分析
chatrel memory     chat.json        # 关系记忆书
chatrel portal --out ./output       # 仅重建门户
```

所有子命令支持 `--out` (默认 `./output`) 和 `--no-html` (只产出 JSON, 不渲染)。

## 输出一览

每个分析器在输出目录写一份 `metrics_*.json`, 对应的 renderer 把 JSON 转成交互式 HTML。七种产出:

| 文件 | 内容 |
|---|---|
| `depth_metrics.json` + `depth_report.html` | 每周信号时序 · Sternberg 三维分数 · Knapp 阶段锚点 · 综合 IDS · 里程碑 · 私有语言 |
| `attachment_forecast.json` + `attachment_forecast_report.html` | ECR-R 分数 · Bartholomew 分类 · 配对类型 · 12 周 3 情景预测 · Gottman 正负比 · 四骑士 · 临界减速预警 |
| `conflict_events.json` + `conflict_report.html` | 冲突窗口 + 发起者/峰值/首次道歉/恢复情况 · 月度趋势 · 修复模式 |
| `resilience_metrics.json` + `resilience_report.html` | 威胁暴露 · 排他/信任/我们感密度 · 2 小时响应风格 · 综合抗性指数 · 共度应激 |
| `memory_book_data.json` + `memory_book.html` | 10 章自动精选: 第一次 / 最甜 / 最深剖白 / 私有语言 / 大日子 / 角色代表作, 客户端搜索 |
| `index.html` | 总门户, 链接上面全部 |

## 隐私

**ChatRel 全本地处理, 零网络请求。**

* 聊天 JSON 永远不离开你的机器。
* 生成的 HTML 是独立文件; Plotly 在浏览器打开时从 CDN 加载 (想完全离线改 `renderers/common.py`)。
* `.gitignore` 拦截所有 chat 数据和生成报告的误提交。**推送前请先查一遍**。
* 仓库里**唯一**的 demo 数据是合成数据, 真实对话请永远不要提交。

## 伦理

你在分析一个没看过你词典的真实的人。一些工具无法强制但应自律的点:

* 指标是**代理信号**, 不是诊断。不要跟别人说 Ta "是" 焦虑-先占型。
* 依恋"类型"是维度的、情境的、会随安全环境变化的。2D 散点只是起点, 不是标签。
* 预测是阻尼线性外推 + 均值回归, **不是**概率预测。不要告诉别人 "咱们六周后会分手"。
* 真要和伴侣讨论发现, 请讨论**模式** (谁更常道歉、仪式频率什么时候下降), 不要讨论分数。

## 贡献

* 欢迎其它语言的词典 (英/日/西/...)。
* 欢迎其它平台的适配器 (WhatsApp、iMessage、Discord)。
* 有专家标注的 ground-truth 评估集会极大提升效度验证, 欢迎合作。

## License

MIT © ChatRel contributors.

## 致谢

基于: [jieba](https://github.com/fxsjy/jieba), [SnowNLP](https://github.com/isnowfy/snownlp), [Plotly](https://plotly.com/python/)。心理学框架引用见 [`docs/methodology.md`](docs/methodology.md)。
