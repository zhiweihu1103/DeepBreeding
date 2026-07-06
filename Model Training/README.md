## 1. Installation

```bash
Download DeepBreeding_Model_Train.zip and extract it to the specified folder.
cd DeepBreeding_Model_Train

conda create -n deepbreeding_model_train python=3.11 -y
conda activate deepbreeding_model_train

pip install -e ".[torch,metrics]" --no-build-isolation
```

Check whether the installation is successful:

```bash
llamafactory-cli version
```

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

## 3. Prepare Dataset

Create a training file under the `data/` directory. You can use the datasets located under the path `Supplemental Information/Datasets/Datasets for Different Figures`.

An example data format is shown below:

```json
[
{
  "system": "You are an expert assistant in breeding and plant genetics.\n    Your role is to answer multiple-choice questions accurately and objectively.\n    Your behavior guidelines:\n    - Be concise, factual, and decisive\n    - Select exactly one answer option\n    - Support your decision with factual, verifiable claims that could stand alone for fact-checking\n    ",
  "instruction": "Please answer the question according to the instructions below:\n    1. Read the question and options.\n    2. Select the single best answer choice.\n    3. Produce a list of affirmative, decontextualized scientific claims that support your answer.\n    - Each claim should be accurate, standalone, and fact-checkable.\n    - Number each claim.\n    ",
  "input": "### In-Context Examples:\n    ### Question: Which gene is commonly associated with drought tolerance in millet?\n    ### Options:\n    A. WRKY1\n    B. DREB2A\n    C. PHYB\n    D. GA20ox\n    ### Answer: B\n    ### Claims:\n    1. DREB2A is a transcription factor that regulates genes involved in plant stress responses.\n    2. DREB2A enhances drought tolerance by activating drought-responsive pathways.\n    3. WRKY1 and PHYB are not primarily associated with drought tolerance in millet.\n    ### Question: Which gene plays a major role in salt tolerance in foxtail millet?\n    ### Options:\n    A. HKT1\n    B. PPDK\n    C. PHYTOCHROME C\n    D. SWEET4\n    ### Answer: A\n    ### Claims:\n    1. HKT1 encodes a sodium transporter that maintains ion homeostasis under salt stress.\n    2. HKT1 improves salt tolerance by reducing toxic Na⁺ accumulation in plant tissues.\n    3. PPDK and PHYTOCHROME C are not known to be primary regulators of salt tolerance in foxtail millet.\n    ### Question: Which protein is primarily involved in regulating drought-induced ABA signaling in maize?\n    ### Options:\n    A. HY5\n    B. SnRK2.6\n    C. SOC1\n    D. PPDK\n    ### Answer: B\n    ### Claims:\n    1. SnRK2.6 is a central kinase activated by drought-induced ABA signaling.\n    2. It phosphorylates downstream transcription factors to promote drought-responsive gene expression.\n    3. HY5 and SOC1 mainly regulate photomorphogenesis and flowering, not drought-induced ABA signaling.\n    Now answer the following question:\n    ### Question: According to previous studies, which domain is characteristic of IPT in Zea mays?\n    ### Options:\nA. JRL, dirigent\nB. B3, Aux/IAA\nC. AP2 domain\nD. isopentenyltransferase domain",
  "output": "### Answer: D\n    ### Claims:\n    1. IPT (isopentenyltransferase) is the key enzyme in cytokinin biosynthesis that catalyzes the first committed step.\n2. The IPT gene family in plants contains conserved isopentenyltransferase catalytic domains.\n3. In Zea mays, IPT genes have been identified and characterized with isopentenyltransferase domains.\n4. The isopentenyltransferase domain is responsible for transferring isopentenyl groups to AMP/ADP or ATP in cytokinin biosynthesis.\n5. Jacalin-related lectin domains and dirigent domains are associated with pathogen defense and lignin biosynthesis, not cytokinin biosynthesis.\n6. B3 DNA-binding domains and Aux/IAA dimerization domains are characteristic of transcription factors like ARF and Aux/IAA proteins.\n7. AP2 domains are found in AP2/ERF transcription factors involved in various stress responses and development."
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

## 4. Register Dataset

Edit `data/dataset_info.json` and add the following content:

```json
"crop_test": {
  "file_name": "xxx.jsonl",
  "columns": {
    "prompt": "instruction",
    "query": "input",
    "response": "output",
    "system": "system"
  }
}
```

- `crop_test` is the dataset name selected in WebUI during fine-tuning.
- `xxx.jsonl` is your jsonl data, which can be found in `Supplemental Information/Datasets/Datasets for Different Figures`.


## 5. Fine-tuning with WebUI
Open the following address in the browser:

```text
http://127.0.0.1:7860/
```

Set the following options in WebUI:

| Option          | Value                                                         |
| --------------- | ------------------------------------------------------------- |
| Model Name      | `Qwen2.5-3B-Instruct`                                         |
| Model Path      | `benchmark_model_weights/Qwen2.5-3B-Instruct` |
| Stage           | `sft`                                                         |
| Finetuning Type | `lora`                                                        |
| Chat Template   | `qwen`                                                        |
| Dataset         | `crop_test`                                                  |
| Epoch           | `3`                                                           |
| LoRA Rank       | `8`                                                           |
| LoRA Alpha      | `16`                                                          |
| LoRA+ LR Ratio  | `16`                                                          |
| Output Dir      | `saves/Qwen2.5-3B-Instruct/lora/crop_test`                        |

After completing the configuration, click `Start` to begin fine-tuning.

## 6. API Inference after Fine-tuning

Create an inference configuration file:

```bash
vim crop_inference.yaml
```

Add the following content:

```yaml
model_name_or_path: benchmark_model_weights/Qwen2.5-3B-Instruct
adapter_name_or_path: saves/Qwen2.5-3B-Instruct/lora/crop_test
template: qwen
finetuning_type: lora
trust_remote_code: true
```

Start the API service:

```bash
API_PORT=8000 CUDA_VISIBLE_DEVICES=0 llamafactory-cli api crop_inference.yaml
```
