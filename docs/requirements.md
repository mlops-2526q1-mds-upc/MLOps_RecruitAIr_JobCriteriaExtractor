RecruitAIr is an AI-based recruitment platform that, given a job description and several applications, ranks the applicants based on their suitability for the job.

## Functional Requirements of the Application

1. **Job offer registry:**
    - The system shall allow recruiters to create and store job offers with details such as job title, description, required skills, experience level, location, and salary range.
    - The system shall provide a user interface for employers to input and manage job offers.
    - The system shall validate the input data to ensure completeness and correctness before saving a job offer.
    - The system shall process job offers to translate the description, required skills, relevant skills, etc., into a structured format suitable for cross-checking with applicant data.

2. **Applicant management:**
    - The system shall allow recruiters to, given a job offer, input and store several applications with details such as applicant name, contact information, resume/CV, cover letter, and relevant skills.
    - The system shall provide a user interface for employers to input and manage applicant information for each job offer.
    - The system shall validate the input data to ensure completeness and correctness before saving an applicant's information.
    - The system shall take into account the privacy and security of applicant data, ensuring compliance with relevant data protection regulations, such as only storing sensitive data for as long as necessary.
    - The system shall allow applicants to opt out of data storage if they choose to withdraw their application.

3. **Applicant suitability and ranking:**
    - The system shall analyze all applications for a given job offer and, for each required skill or experience level (every relevant aspect of the job offer), check how well each applicant matches these criteria.
    - The system shall display all applicants for a given job offer in an extensive table, showing their details and how well they match each of the job requirements: one column per required skill, experience level, etc., with a numerical score between 0 and 10, with a single decimal point.
    - The system shall rank the applicants based on their overall suitability for the job, considering all factors, and computing some weighted average score.
    - The AI system shall choose the weights for each factor based on their importance for the specific job offer, which may vary between different job offers, and display them in a clear and understandable manner for the recruiter to modify if needed.
    - The system shall provide a user interface for recruiters to view the ranked list of applicants for each job offer.
    - The system shall allow recruiters to filter and sort the ranked list based on various criteria, such as skill match, experience level, or overall score.
    - The system shall provide detailed insights into how each applicant was evaluated, including which skills or experiences contributed most to their ranking.
    - The system shall allow recruiters to provide feedback on the ranking results to improve the AI model.


## Non-Functional Requirements of the Application

3. **Applicant suitability and ranking:**
    - Given a dataset with several applications and job offers, and their human-defined best match, the system shall rank the best match among the 10% top ranked applicants in at least 80% of the cases.


## Functional Requirements of the AI Systems

1. **Job offer processing:**
   - The AI system shall process the job offer's text to extract a list of all possible criteria, such as required skills, experience levels, and other relevant factors, and convert them into a structured format suitable for matching with applicant data.
   - The structured format shall include a title of the criterion, a weight (importance) for the specific job offer, and a clear and understandable description of the criterion that allows further processing and cross-checking with applicant data.

2. **Applicant requirement matching:**
   - The AI system shall receive an applicant's CV and data, as well as a job requirement's description (criterion), and return a numerical score between 0 and 1 (the front-end shall convert it to 0-10 with a single decimal point) indicating how well the applicant matches that specific requirement.

## Non-Functional Requirements of the AI Systems

1. **Job offer processing:**
   - The AI system in charge of processing job offers shall correctly identify and extract at least 90% of the relevant criteria from the job description in at least 90% of the cases, as deemed by a panel of recruitment experts.
   - The AI system shall assign weights to the extracted criteria that align with human judgment in at least 85% of the cases, as evaluated by a panel of recruitment experts.
   - The AI system shall generate clear and understandable descriptions for each extracted criterion, ensuring that at least 95% of the descriptions are deemed comprehensible by human recruiters.
   - The AI system shall process and return the structured format of a job offer within 5 seconds for 95% of job offers.

2. **Applicant requirement matching:**
    - The AI system in charge of matching applicants to job requirements shall achieve a mean absolute error of at most 0.5 in predicting the suitability score for individual criteria, as validated against a benchmark dataset with human-assigned scores.
    - The AI system shall ensure that the suitability scores are consistent and reliable, with a variance of less than 0.5 in repeated evaluations of the same applicant against the same criterion.
    - The AI system shall process and return the suitability score for an applicant against a single job requirement within 3 seconds for 95% of requests.