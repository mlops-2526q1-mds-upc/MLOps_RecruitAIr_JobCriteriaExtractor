import pandas as pd
from sklearn.model_selection import train_test_split

from recruitair.config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR, SEED, TRAIN_SPLIT, VALIDATION_SPLIT

def split_data():
    """
    Split the cleaned data into train, validation, and test sets and save them to the 'data/processed' directory.

    The split is done in the ratio of TRAIN_SPLIT, VALIDATION_SPLIT, and the remainder as test.
    The random seed is set to ensure reproducibility.
    """
    df = pd.read_parquet(INTERIM_DATA_DIR / "preprocessed_resumes.parquet")

    # First split into train and remaining
    train_df, remaining_df = train_test_split(
        df,
        train_size=TRAIN_SPLIT,
        random_state=SEED,
        shuffle=True
    )

    # Compute validation proportion relative to remaining
    validation_ratio = VALIDATION_SPLIT / (1 - TRAIN_SPLIT)
    validation_df, test_df = train_test_split(
        remaining_df,
        train_size=validation_ratio,
        random_state=SEED,
        shuffle=True
    )

    # Save to Parquet
    train_df.to_parquet(PROCESSED_DATA_DIR / "train.parquet", index=False)
    validation_df.to_parquet(PROCESSED_DATA_DIR / "validation.parquet", index=False)
    test_df.to_parquet(PROCESSED_DATA_DIR / "test.parquet", index=False)

if __name__ == "__main__":
    split_data()
