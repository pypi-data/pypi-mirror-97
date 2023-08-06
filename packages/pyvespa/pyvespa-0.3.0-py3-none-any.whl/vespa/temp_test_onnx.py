#! /usr/bin/env python3

import os
import torch
import onnxruntime as ort
import transformers
import transformers.convert_graph_to_onnx as onnx_convert
from pathlib import Path


if __name__ == "__main__":
    os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
    # Test transformers
    tokenizer = transformers.BertTokenizer.from_pretrained(
        "google/bert_uncased_L-2_H-128_A-2"
    )
    model = transformers.BertForSequenceClassification.from_pretrained(
        "google/bert_uncased_L-2_H-128_A-2"
    )
    inputs = tokenizer("this is a query", "this is a document", return_tensors="pt")
    print(inputs)
    hf_outputs = model(**inputs)
    # Test onnx runtime
    pipeline = transformers.Pipeline(model=model, tokenizer=tokenizer)
    onnx_convert.convert_pytorch(
        model, opset=11, output=Path("test.onnx"), use_external_format=False
    )
    m = ort.InferenceSession("test.onnx")
    model_inputs = {
        "input_ids": inputs["input_ids"].numpy(),
        "token_type_ids": inputs["token_type_ids"].numpy(),
        "attention_mask": inputs["attention_mask"].numpy(),
    }
    ort_outputs = m.run(input_feed=model_inputs, output_names=["output_0"])
    print(hf_outputs)
    print(ort_outputs)
