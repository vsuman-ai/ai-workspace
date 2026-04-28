### Architecture summary

```
Request
  ↓
Proto/API layer
  ↓
BertweetSentimentService
  ↓
Tokenizer
  ↓
input_ids + attention_mask
  ↓
Triton gRPC Client
  ↓
Triton Server
  ↓
ONNX Runtime Backend
  ↓
logits
  ↓
softmax + label mapping
  ↓
Response
```