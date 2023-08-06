#! /usr/bin/env python3

import os
import onnxruntime as ort
import transformers
from torch.onnx import export


def export_to_onnx(model, output_path, dummy_input) -> None:

    input_names = ["input_ids", "token_type_ids", "attention_mask"]
    output_names = ["logits"]
    export(
        model,
        (
            dummy_input["input_ids"],
            dummy_input["token_type_ids"],
            dummy_input["attention_mask"],
        ),
        output_path,
        input_names=input_names,
        output_names=output_names,
        verbose=False,
        opset_version=11,
    )


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
    model_inputs = {
        "input_ids": inputs["input_ids"].numpy(),
        "token_type_ids": inputs["token_type_ids"].numpy(),
        "attention_mask": inputs["attention_mask"].numpy(),
    }
    hf_outputs = model(**inputs)
    # Test onnx runtime
    export_to_onnx(model, "test_model.onnx", inputs)
    m = ort.InferenceSession("test_model.onnx")
    ort_outputs = m.run(input_feed=model_inputs, output_names=["logits"])
    print(hf_outputs)
    print(ort_outputs)
