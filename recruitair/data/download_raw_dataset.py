import kagglehub
from kagglehub import KaggleDatasetAdapter

from recruitair.config import RAW_DATA_DIR

def download_dataset():
    """
    Download the dataset from Kaggle and save it to the 'data/raw' directory.
    """

    skill_set_file = f"{RAW_DATA_DIR}/job-skill-set.csv"
    recruitment_file = f"{RAW_DATA_DIR}/recruitment.csv"

    df_job_skill_set = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "batuhanmutlu/job-skill-set",
        "all_job_post.csv",
    )
    df_recruitment = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "surendra365/recruitement-dataset",
        "job_applicant_dataset.csv",
    )

    df_job_skill_set.to_csv(skill_set_file)
    df_recruitment.to_csv(recruitment_file)


if __name__ == "__main__":
    download_dataset()
