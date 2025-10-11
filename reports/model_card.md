---
# For reference on model card metadata, see the spec: https://github.com/huggingface/hub-docs/blob/main/modelcard.md?plain=1
# Doc / guide: https://huggingface.co/docs/hub/model-cards
{{ card_data }}
---

# Model Card for RecruitAIr_JobCriteriaExtractor
The model extracts from a job offer the relevant skills, experiences, and other applicant requirements that recruiters are seeking. It transforms unstructured job descriptions into structured, machine-readable criteria that can be used to assess applicant suitability.

## Model Details

### Model Description

RecruitAIr_JobCriteriaExtractor is a Natural Language Processing (NLP) model designed to process job descriptions and extract structured job criteria. It identifies required skills, preferred skills, experience levels, and other relevant attributes. Each extracted criterion is represented with: a title (e.g., "Python Programming"), a weight (importance for the role), and a description (a recruiter-friendly explanation of the requirement).

- **Developed by:** Alfonso Brown (github: abrownglez (https://github.com/abrowng)), Tania González (github: taaniagonzaalez (https://github.com/taaniagonzaalez)), Virginia Nicosia (github: viiirgi(https://github.com/viiiiirgi)), Marc Parcerisa (github: AimboParce (https://github.com/AimbotParce)), Daniel Reverter (github: danirc2 (https://github.com/danirc2))
- **Funded by :** Alfonso Brown, Tania González, Virginia Nicosia, Marc Parcerisa, Daniel Reverter
- **Shared by :** Alfonso Brown, Tania González, Virginia Nicosia, Marc Parcerisa, Daniel Reverter
- **Model type:** Machine Learning
- **Language(s) (NLP):** English
- **License:** apache-2.0
- **Finetuned From Model:** dolphin3 (via Ollama)

### Model Sources

- **Repository:** git@github.com:mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor.git

## Uses

<!-- Address questions around how the model is intended to be used, including the foreseeable users of the model and those affected by the model. -->

### Direct Use

<!-- This section is for the model use without fine-tuning or plugging into a larger ecosystem/app. -->

-   Extracting structured job criteria from free-text job descriptions.
-   Preprocessing for automated recruitment pipelines.
-   Providing recruiters with a clear breakdown of job requirements.

### Downstream Use 
<!-- This section is for the model use when fine-tuned for a task, or when plugged into a larger ecosystem/app -->

-   Feeding structured criteria into RecruitAIr_CriteriaEvaluator to match and rank applicants.
-   Supporting explainable AI in recruitment by displaying transparent criteria-to-score mappings.
-   Enabling recruiters to refine weights or edit extracted criteria.

### Out-of-Scope Use

<!-- This section addresses misuse, malicious use, and uses that the model will not work well for. -->

-   Using the model as a fully automated hiring decision-maker since it is not intended to replace human judgment.
-   Applying it to non-English job descriptions since the model is currently trained only on English.
-   Extracting sensitive personal or demographic attributes since the model is not designed for this and could introduce bias.

## Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->

-   Bias in Job Descriptions: if job postings are written with biased or exclusionary language, the model may replicate these biases in the extracted criteria.
-   Domain Limitations: performance may degrade in highly specialized domains (e.g., legal, medical, or academic job postings) where terminology differs from standard datasets.
-   False Negatives/Positives: the model may miss some relevant criteria (false negatives) or extract irrelevant phrases (false positives).
-   Weight Assignment: while the AI assigns weights, recruiters must review them to ensure they align with human judgment.

### Recommendations

<!-- This section is meant to convey recommendations with respect to the bias, risk, and technical limitations. -->

Users should always review extracted criteria before applying them in candidate evaluations and the recruiters should adjust criterion weights when necessary to reflect actual job priorities and mitigate bias.

## How to Get Started with the Model

Use the code below to get started with the model.

{{ get_started_code | default("[More Information Needed]", true)}}

## Training Details

### Training Data

<!-- This should link to a Dataset Card, perhaps with a short stub of information on what the training data is all about as well as documentation related to data pre-processing or additional filtering. -->

The model was not trained from scratch; it is an instruction-tuned model (dolphin3) applied with structured prompts to extract criteria.
However, custom datasets were used for prompt engineering and evaluation.

    - Hugging Face: HF_RESUME_SCORE_DETAILS_REPO (custom dataset of resume–criteria scoring pairs)

    - Kaggle: 
        -batuhanmutlu/job-skill-set (https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set)
        -surendra365/recruitement-dataset (https://www.kaggle.com/datasets/surendra365/recruitement-dataset)

Dataset card for job skills: https://github.com/mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor/blob/main/reports/dataset_card_jobs.md

Dataset card for recruitment: https://github.com/mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor/blob/main/reports/dataset_card_recruitment.md

Dataset card for resume scores: https://github.com/mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor/blob/main/reports/dataset_card_resume-score-details.md


### Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

#### Preprocessing [optional]

The preprocessing pipeline includes several modular scripts:
    -download_raw_dataset.py: downloads raw datasets from Hugging Face and Kaggle and ensures local reproducibility and version consistency through .env configuration.
    -preprocess_jsons.py: parses and normalizes resume–criteria–score tuples from JSON or structured data sources and generates standardized schema for extraction training and evaluation.
    -process_dataset.py: cleans and normalizes tabular data (removes duplicates, harmonizes skill labels).-generate_features.py: creates structured features and target mappings for evaluation.
    -make_plot.py: produces exploratory data analysis (EDA) visualizations and validation plots.

All scripts support logging with loguru and progress tracking via tqdm.

#### Training Hyperparameters

- **Training regime:** 
Fine-tuning: None (prompt-based adaptation)

Precision: fp16

Batch size: 1 (interactive inference)

Max tokens: 2048

Temperature: 0.0 (deterministic extraction)

Framework: LangChain + Ollama API <!--fp32, fp16 mixed precision, bf16 mixed precision, bf16 non-mixed precision, fp16 non-mixed precision, fp8 mixed precision -->

#### Speeds, Sizes, Times [optional]

<!-- This section provides information about throughput, start/end time, checkpoint size if relevant, etc. -->

{{ speeds_sizes_times | default("[More Information Needed]", true)}}

## Evaluation

<!-- This section describes the evaluation protocols and provides the results. -->

### Testing Data, Factors & Metrics

#### Testing Data

<!-- This should link to a Dataset Card if possible. -->

{{ testing_data | default("[More Information Needed]", true)}}

#### Factors

<!-- These are the things the evaluation is disaggregating by, e.g., subpopulations or domains. -->

Evaluated on: job domain (tech, finance, marketing), description length (short, medium, long) and complexity (number of distinct criteria)
#### Metrics

<!-- These are the evaluation metrics being used, ideally with a description of why. -->

Precision@K:	% of extracted criteria that match human-annotated ground truth
Recall@K:	% of true criteria successfully extracted
F1-score:	Harmonic mean of precision and recall
Extraction latency:	Average time per inference (in seconds)

### Results

{{ results | default("[More Information Needed]", true)}}

#### Summary

The model shows strong performance in general technical job descriptions.
Slightly reduced accuracy was observed in non-technical or managerial postings.

## Model Examination [optional]

<!-- Relevant interpretability work for the model goes here -->

Interpretability achieved through:
    -Transparent output schema (title, weight, description)
    -Ability to trace extracted text spans back to original posting
    -Human-verifiable criterion weights

## Environmental Impact

<!-- Total emissions (in grams of CO2eq) and additional considerations, such as electricity usage, go here. Edit the suggested text below accordingly -->

Carbon emissions can be estimated using the [Machine Learning Impact calculator](https://mlco2.github.io/impact#compute) presented in [Lacoste et al. (2019)](https://arxiv.org/abs/1910.09700).

- **Hardware Type:** {{ hardware_type | default("[More Information Needed]", true)}}
- **Hours used:** {{ hours_used | default("[More Information Needed]", true)}}
- **Cloud Provider:** {{ cloud_provider | default("[More Information Needed]", true)}}
- **Compute Region:** {{ cloud_region | default("[More Information Needed]", true)}}
- **Carbon Emitted:** {{ co2_emitted | default("[More Information Needed]", true)}}

## Technical Specifications [optional]

### Model Architecture and Objective

{{ model_specs | default("[More Information Needed]", true)}}

### Compute Infrastructure

{{ compute_infrastructure | default("[More Information Needed]", true)}}

#### Hardware

{{ hardware_requirements | default("[More Information Needed]", true)}}

#### Software

{{ software | default("[More Information Needed]", true)}}


## Model Card Authors 

Alfonso Brown, Tania González, Virginia Nicosia, Marc Parcerisa, Daniel Reverter

## Model Card Contact

