# Model Notes & Trade-offs

## Selected Models

### 1. Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- **Why**: Extremely fast, small footprint (~80MB), and sufficient for clustering technical logs.
- **Trade-off**: Lower semantic nuance than `e5-large` or OpenAI embeddings, but runs on CPU effortlessly.

### 2. Generation: `google/flan-t5-small`
- **Why**: Good instruction following for its size (80M params). Can run locally without GPU.
- **Trade-off**: Summaries can be brief or generic.
- **Recommendation**: Upgrade to `flan-t5-large` or use OpenAI/Claude API for production-grade summaries.

### 3. Sentiment: `distilbert-base-uncased-finetuned-sst-2-english`
- **Why**: Standard for sentiment, faster than large BERT models.
- **Fallback**: `TextBlob` (rule-based) used if model loading fails.

## Trade-offs Summary

| Feature | Local (Current) | Cloud API (OpenAI/Claude) |
|---------|----------------|---------------------------|
| **Latency** | Low (no network) | Medium (network RTT) |
| **Cost** | Free (Compute only) | Per-token cost |
| **Privacy** | High (Data stays local) | Medium (Data sent to API) |
| **Quality** | Basic/Good | Excellent |

## Configuration
Set `MODEL_MODE` in `.env`:
- `local`: Force local models.
- `huggingface_api`: Use HF Inference API (requires key).
- `auto`: Try local, fallback to API (Default).
