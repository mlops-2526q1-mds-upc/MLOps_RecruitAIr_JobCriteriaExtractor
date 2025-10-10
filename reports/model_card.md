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

Dataset card for job skills: https://github.com/mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor/blob/main/reports/dataset_card_jobs.md

Dataset card for recruitment: https://github.com/mlops-2526q1-mds-upc/MLOps_RecruitAIr_JobCriteriaExtractor/blob/main/reports/dataset_card_recruitment.md


### Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

#### Preprocessing [optional]

{{ preprocessing | default("[More Information Needed]", true)}}


#### Training Hyperparameters

- **Training regime:** {{ training_regime | default("[More Information Needed]", true)}} <!--fp32, fp16 mixed precision, bf16 mixed precision, bf16 non-mixed precision, fp16 non-mixed precision, fp8 mixed precision -->

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

{{ testing_factors | default("[More Information Needed]", true)}}

#### Metrics

<!-- These are the evaluation metrics being used, ideally with a description of why. -->

{{ testing_metrics | default("[More Information Needed]", true)}}

### Results

{{ results | default("[More Information Needed]", true)}}

#### Summary

{{ results_summary | default("", true) }}

## Model Examination [optional]

<!-- Relevant interpretability work for the model goes here -->

{{ model_examination | default("[More Information Needed]", true)}}

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

