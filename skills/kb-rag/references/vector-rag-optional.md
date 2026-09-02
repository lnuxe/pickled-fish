# Optional vector RAG

Default orchestration is **filesystem progressive disclosure** (no embeddings).  
If you need semantic search over a large private corpus:

## Suggested stack (local)

1. Keep markdown under `knowledge/custom/<id>/`  
2. Build embeddings with any local tool (e.g. llama-index / chroma / sqlite-vec) **on the user’s machine**  
3. Expose a script `knowledge/custom/<id>/scripts/search.py "query"` that prints top-k paths + snippets  
4. In `PACK.md` set:

```yaml
retrieval: script
search_script: scripts/search.py
```

5. kb-rag will: run the script → Read returned paths → answer  

## Rules

- Do not upload chat exports to hosted vector SaaS by default  
- Commit neither embedding DB nor API keys  
- Fallback: if script missing, use `rg` keyword search  
