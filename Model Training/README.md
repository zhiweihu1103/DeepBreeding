# Model Training Tutorial

## 1. Installation

Clone the LLaMA-Factory repository and install the required dependencies:

```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory

conda create -n model_train python=3.11 -y
conda activate model_train

pip install -e ".[torch,metrics]" --no-build-isolation
```

Check whether the installation is successful:

```bash
llamafactory-cli version
```

---

## 2. Start WebUI

```bash
export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1

CUDA_VISIBLE_DEVICES=0 llamafactory-cli webui
```

Open the following address in the browser:

```text
http://127.0.0.1:7860/
```

If the WebUI cannot be accessed, check whether port `7860` is blocked by the firewall or security group.

---

## 3. Prepare Dataset

Create a training file under the `data/` directory:

```bash
vim data/test.json
```

An example data format is shown below:

```json
[
  {
    "system": "You are an expert assistant in breeding and plant genetics.",
    "instruction": "Please answer the multiple-choice question and provide supporting claims.",
    "input": "### Question: In the species Avena sativa, which gene contains C2H2 zinc finger, WRKY DNA-binding domain, and C2HC zinc finger domains?\n### Options:\nA. AsWRKY\nB. AsMYB2R\nC. AsNAC\nD. AsTCP",
    "output": "### Answer: A\n### Claims:\n1. WRKY transcription factors contain conserved WRKY DNA-binding domains.\n2. AsWRKY is a WRKY transcription factor identified in Avena sativa.",
    "history": []
  }
]
```

Field descriptions:

| Field         | Meaning              |
| ------------- | -------------------- |
| `system`      | System prompt        |
| `instruction` | Task instruction     |
| `input`       | Question and options |
| `output`      | Target answer        |
| `history`     | Dialogue history     |

---

## 4. Register Dataset

Edit `data/dataset_info.json` and add the following content:

```json
"grain_test": {
  "file_name": "test.json",
  "columns": {
    "prompt": "instruction",
    "query": "input",
    "response": "output",
    "system": "system",
    "history": "history"
  }
}
```

Here, `grain_test` is the dataset name selected in WebUI during fine-tuning.

---

## 5. Fine-tuning with WebUI

Set the following options in WebUI:

| Option          | Value                                                         |
| --------------- | ------------------------------------------------------------- |
| Model Name      | `Qwen2.5-3B-Instruct`                                         |
| Model Path      | `/data/Users/hzw/benchmark_model_weights/Qwen2.5-3B-Instruct` |
| Stage           | `sft`                                                         |
| Finetuning Type | `lora`                                                        |
| Chat Template   | `qwen`                                                        |
| Dataset         | `grain_test`                                                  |
| Epoch           | `3`                                                           |
| LoRA Rank       | `8`                                                           |
| LoRA Alpha      | `16`                                                          |
| LoRA+ LR Ratio  | `16`                                                          |
| Output Dir      | `saves/Qwen2.5-3B-Instruct/lora/grain`                        |

After completing the configuration, click `Start` to begin fine-tuning.

---

## 6. API Inference after Fine-tuning

Create an inference configuration file:

```bash
vim examples/inference/grain_inference.yaml
```

Add the following content:

```yaml
model_name_or_path: /data/Users/hzw/benchmark_model_weights/Qwen2.5-3B-Instruct
adapter_name_or_path: /data/Users/hzw/reproduce_code/sxau_benchmark/LLaMA-Factory/saves/Qwen2.5-3B-Instruct/lora/grain
template: qwen
finetuning_type: lora
trust_remote_code: true
```

Start the API service:

```bash
API_PORT=8000 CUDA_VISIBLE_DEVICES=0 llamafactory-cli api examples/inference/grain_inference.yaml
```

The API endpoint is:

```text
http://115.24.15.13:8000/v1
```

---

## 7. Python Inference Example

```python
from openai import OpenAI

base_url = "http://115.24.15.13:8000/v1"
model = "/data/Users/hzw/benchmark_model_weights/Qwen2.5-3B-Instruct"

client = OpenAI(api_key="0", base_url=base_url)

system_content = "You are an expert assistant in breeding and plant genetics."

user_content = """Please answer the following multiple-choice question.

### Question: In the species Avena sativa, which gene contains C2H2 zinc finger, WRKY DNA-binding domain, and C2HC zinc finger domains?
### Options:
A. AsWRKY
B. AsMYB2R
C. AsNAC
D. AsTCP
"""

messages = [
    {"role": "system", "content": system_content},
    {"role": "user", "content": user_content}
]

result = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.0,
    max_tokens=512
)

print(result.choices[0].message.content)
```
