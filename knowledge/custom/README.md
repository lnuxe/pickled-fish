# Custom knowledge packs

把你自己的笔记、公司话术规范、私有案例摘要放这里。

```bash
# 从 Git 安装远端包到 custom/
bash scripts/add-pack.sh my-pack https://github.com/org/repo

# 或复制模板
cp -R knowledge/packs/_template knowledge/custom/my-pack
```

每个包必须有 `PACK.md`。含隐私的包请加入本地 ignore，勿推送公开仓库。

建议在包内维护 `index.md`（目录摘要），便于 kb-rag 渐进读取。
