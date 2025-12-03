---
# For reference on dataset card metadata, see the spec: https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1
# Doc / guide: https://huggingface.co/docs/hub/datasets-cards
card_data: {{card_data}}
---

# Dataset Card for Job Skill

## Dataset Details

### Dataset Description

<!-- Provide a longer summary of what this dataset is. -->

The Job Skill Set Dataset is designed for use in machine learning projects related to job matching, skill extraction, and natural language processing tasks. The dataset includes detailed information about job roles, descriptions, and associated skill sets, enabling developers and researchers to build and evaluate models for career recommendation systems, resume parsing, and skill inference.

- **Owned by:** [Batuhan Mutlu](https://www.kaggle.com/batuhanmutlu)
- **Language(s) (NLP):** English
- **License:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

### Dataset Sources [optional]

<!-- Provide the basic links for the dataset. -->

- **Repository:** https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set

## Uses

<!-- Address questions around how the dataset is intended to be used. -->

This dataset is primarily used to sample a diverse range of job offers that serve as input during the model training and evaluation process. By including various job descriptions, roles, and requirements, the dataset helps create realistic scenarios that simulate how different types of job openings are matched with candidate applications. This enables the model to learn how to identify the most suitable applicants for each position, based on the specific demands and characteristics of each job offer.

### Direct Use

<!-- This section describes suitable use cases for the dataset. -->

This dataset is particularly useful for the following applications:

- Skill Extraction: Identifying and parsing skills from job descriptions.

- Job-Resume Matching: Matching job descriptions with potential candidate profiles.

- Recommendation Systems: Developing models that recommend jobs or training programs based on required skills.

- Natural Language Processing: Experimenting with text-based models in recruitment and career analytics.


## Dataset Structure

<!-- This section provides a description of the dataset fields, and additional information about the dataset structure such as criteria used to create the splits, relationships between data points, etc. -->

The dataset contains the following features:

- **job_id:** A unique identifier for each job posting.

- **category:** The category of the job, such as INFORMATION-TECHNOLOGY,BUSINESS-DEVELOPMENT,FINANCE,SALES or HR.

- **job_title:** The title of the job position.

- **job_description:** A detailed text description of the job, including responsibilities and qualifications.

- **job_skill_set:** A list of relevant skills(include hard and soft skills) associated with the job, extracted using RecAI APIs.

## Dataset Creation

### Curation Rationale

<!-- Motivation for the creation of this dataset. -->

### Source Data

<!-- This section describes the source data (e.g. news text and headlines, social media posts, translated sentences, ...). -->

This dataset was initially sourced from the Kaggle dataset titled [LinkedIn Job Postings](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) by Arshkon. The original job postings data has been enhanced by extracting skill sets using [RecAI API services](https://recai.tech/en). These APIs are designed for skill parsing, resume analysis, and other recruitment-related tasks.

#### Data Collection and Processing

<!-- This section describes the data collection and processing process such as data selection criteria, filtering and normalization methods, tools and libraries used, etc. -->
The raw data contained multiple JSON files (match_X.json, mismatch_X.json) with job descriptions and criteria dictionaries.

A preprocessing script consolidated these into a single JSONL file by:

1. Loading and parsing all valid JSON files.

2. Extracting the job_description, macro_dict, and micro_dict fields.

3. Merging both dictionaries into a unified list of {name, importance} pairs.

4. Writing each processed record as one JSON line with the structure:

{"job_description": "...", "criteria": [{"name": "leadership", "importance": 35}, ...]}

Invalid or unreadable files are skipped with warnings. The final output (preprocessed_jobs.jsonl) provides a clean, standardized format ready for training and evaluation.

## Citation

<!-- If there is a paper or blog post introducing the dataset, the APA and Bibtex information for that should go in this section. -->

**APA:**

Mutlu, B. (2024). job-skill-set. Kaggle. https://www.kaggle.com/dsv/10201355
 DOI: 10.34740/KAGGLE/DSV/10201355

