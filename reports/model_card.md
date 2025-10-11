---
# For reference on model card metadata, see the spec: https://github.com/huggingface/hub-docs/blob/main/modelcard.md?plain=1
# Doc / guide: https://huggingface.co/docs/hub/model-cards
{{ card_data }}
---

# Model Card for RecruitAIr_JobCriteriaExtractor
The model extracts from a job offer the relevant skills, experiences, and other applicant requirements that recruiters are seeking. It transforms unstructured job descriptions into structured, machine-readable criteria that can be used to assess applicant suitability.

## Model Details

### Model Description

RecruitAIr_JobCriteriaExtractor is an LLM-based system for analyzing job offers and extracting structured hiring criteria. It leverages a local Ollama model (dolphin3) and a versioned MLflow prompt template. The model takes a job description as input and returns a list of key criteria(required skills, preferred skills, experience levels...), each with a title (e.g., "Python Programming"), description (a recruiter-friendly explanation of the requirement), and importance score (importance for the role).

- **Developed by:** Alfonso Brown (github: abrownglez (https://github.com/abrowng)), Tania González (github: taaniagonzaalez (https://github.com/taaniagonzaalez)), Virginia Nicosia (github: viiirgi(https://github.com/viiiiirgi)), Marc Parcerisa (github: AimboParce (https://github.com/AimbotParce)), Daniel Reverter (github: danirc2 (https://github.com/danirc2))
- **Funded by :** Alfonso Brown, Tania González, Virginia Nicosia, Marc Parcerisa, Daniel Reverter
- **Shared by :** Alfonso Brown, Tania González, Virginia Nicosia, Marc Parcerisa, Daniel Reverter
- **Model type:** Large language model for information extraction
- **Language(s) (NLP):** English
- **License:** MIT
- **Finetuned From Model:** dolphin3 (via Ollama)

### Model Sources

- **Repository:** git@github.com:mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor.git

## Uses

<!-- Address questions around how the model is intended to be used, including the foreseeable users of the model and those affected by the model. -->

### Direct Use

<!-- This section is for the model use without fine-tuning or plugging into a larger ecosystem/app. -->
Intended for structured extraction of hiring criteria directly from English job postings. Typical users include HR analytics engineers, talent acquisition researchers, and data scientists building automated resume–job matching systems.

### Downstream Use 
<!-- This section is for the model use when fine-tuned for a task, or when plugged into a larger ecosystem/app -->

- Feeding structured criteria into RecruitAIr_CriteriaEvaluator to match and rank applicants.
- Supporting explainable AI in recruitment by displaying transparent criteria to score mappings.
- Enabling recruiters to refine weights or edit extracted criteria.

### Out-of-Scope Use

<!-- This section addresses misuse, malicious use, and uses that the model will not work well for. -->

- Using the model as a fully automated hiring decision-maker since it is not intended to replace human judgment.
- Applying it to non-English job descriptions since the model is currently trained only on English.
- Extracting sensitive personal or demographic attributes since the model is not designed for this and could introduce bias.
- Not suitable for generating or rewriting job descriptions.

## Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->

- Bias in Job Descriptions: if job postings are written with biased or exclusionary language, the model may replicate these biases in the extracted criteria (e.g., gendered language or cultural preferences).
-   Domain Limitations: performance may degrade in highly specialized domains (e.g., legal, medical, or academic job postings) where terminology differs from standard datasets.
-   False Negatives/Positives: the model may miss some relevant criteria (false negatives) or extract irrelevant phrases (false positives).
-   Weight Assignment: while the AI assigns weights, recruiters must review them to ensure they align with human judgment.

### Recommendations

<!-- This section is meant to convey recommendations with respect to the bias, risk, and technical limitations. -->

Users should always review extracted criteria before applying them in candidate evaluations and the recruiters should adjust criterion weights when necessary to reflect actual job priorities and mitigate bias.

## How to Get Started with the Model

Use the code below to get started with the model.

```python
from recruitair.job_offers.extract_criteria import extract_key_criteria_from_job_offer

job_offer_text = """
We are seeking a Data Scientist with strong experience in Python, SQL, and machine learning.
Knowledge of cloud platforms (AWS, GCP, or Azure) and excellent analytical skills are required.
"""

criteria = extract_key_criteria_from_job_offer(job_offer_text)

for c in criteria.key_criteria:
    print(f"{c.title} ({c.importance}): {c.description}")

```
## Training Details

### Training Data

<!-- This should link to a Dataset Card, perhaps with a short stub of information on what the training data is all about as well as documentation related to data pre-processing or additional filtering. -->

The model was not trained from scratch; it is an instruction-tuned model (dolphin3) applied with structured prompts to extract criteria.
However, custom datasets were used for prompt engineering and evaluation.

- Hugging Face: HF_RESUME_SCORE_DETAILS_REPO (custom dataset of resume–criteria scoring pairs) Preprocessing converted multiple JSON sources into a unified JSONL format containing job descriptions and criteria lists.

- Kaggle: 
     -batuhanmutlu/job-skill-set (https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set)
     -surendra365/recruitement-dataset (https://www.kaggle.com/datasets/surendra365/recruitement-dataset)

Dataset card for job skills: https://github.com/mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor/blob/main/reports/dataset_card_jobs.md

Dataset card for recruitment: https://github.com/mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor/blob/main/reports/dataset_card_recruitment.md

Dataset card for resume scores: https://github.com/mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor/blob/main/reports/dataset_card_resume-score-details.md


### Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

#### Preprocessing 

1. Download datasets from Kaggle and Hugging Face.
2. Parse JSON files (match_X.json, mismatch_X.json).
3. Normalize into job_description and criteria pairs.
4. Convert JSONL to tabular CSV for modeling.

#### Training Hyperparameters 
- Training regime: fp32 precision
- Optimizer: Adam
- Loss: Cross-entropy
- Epochs: 10
- Validation split: 0.2  <!--fp32, fp16 mixed precision, bf16 mixed precision, bf16 non-mixed precision, fp16 non-mixed precision, fp8 mixed precision -->

## Evaluation

<!-- This section describes the evaluation protocols and provides the results. -->

### Testing Data, Factors & Metrics

#### Testing Data

<!-- This should link to a Dataset Card if possible. -->

Held-out subset from the processed dataset representing unseen job offers.

#### Factors

<!-- These are the things the evaluation is disaggregating by, e.g., subpopulations or domains. -->

Evaluated on: job domain (tech, finance, marketing), description length (short, medium, long) and complexity (number of distinct criteria)

#### Metrics

<!-- These are the evaluation metrics being used, ideally with a description of why. -->

- Precision:	% of extracted criteria that match human-annotated ground truth
- Recall:	% of true criteria successfully extracted
- F1-score:	Harmonic mean of precision and recall

### Results

Model training and evaluation are in progress. Results will be reported in the next delivery.

#### Summary

Planned evaluation aims to assess both precision and recall. Results pending.

## Model Examination

<!-- Relevant interpretability work for the model goes here -->

Model interpretability and attention visualization are planned for later milestones to better understand how the model focuses on skill- and experience-related information.

## Environmental Impact

<!-- Total emissions (in grams of CO2eq) and additional considerations, such as electricity usage, go here. Edit the suggested text below accordingly -->

Carbon emissions can be estimated using CodeCarbon

- **Hardware Type:** {{ hardware_type | default("[More Information Needed]", true)}}
- **Hours used:** {{ hours_used | default("[More Information Needed]", true)}}
- **Cloud Provider:** {{ cloud_provider | default("[More Information Needed]", true)}}
- **Compute Region:** {{ cloud_region | default("[More Information Needed]", true)}}
- **Carbon Emitted:** {{ co2_emitted | default("[More Information Needed]", true)}}

## Technical Specifications

### Model Architecture and Objective

A structured-output LLM pipeline using ChatOllama(model="dolphin3").
Objective: extract a list of criteria from job text following a schema defined in KeyCriteriaResponse.

### Compute Infrastructure

Developed and executed locally using Python 3.11 and the Ollama runtime.

#### Hardware
GPU: NVIDIA GeForce RTX3060

#### Software
- Python 3.11
- ollama / langchain-ollama
- mlflow-genai
- pandas
- loguru
- typer
- tqdm


## Model Card Authors 

Alfonso Brown, Tania González, Virginia Nicosia, Marc Parcerisa, Daniel Reverter

## Model Card Contact
For any doubt or question you can write to any member of the RecruitAIr team:
- Alfonso Brown: alfonso.brown@estudiantat.upc.edu
- Tania González: tania.gonzalez@estudiantat.upc.edu
- Virginia Nicosia: virginia.nicosia@estudiantat.upc.edu
- Marc Parcerisa: marc.parcerisa@estudiantat.upc.edu
- Daniel Reverter: daniel.reverter@estudiantat.upc.edu