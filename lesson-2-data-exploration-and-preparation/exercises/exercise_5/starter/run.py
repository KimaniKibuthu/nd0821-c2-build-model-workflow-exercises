#!/usr/bin/env python
import argparse
import logging
import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    # Initialize the run
    run = wandb.init(project="exercise_5", job_type="process_data")

    # download the artifact to use
    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    #Open and do EDA
    logger.info("Cleaning data")
    data = pd.read_parquet(artifact.file())
    data.drop_dupicates().reset_index(drop=True, inplace=True)
    data['title'].fillna(value='', inplace=True)
    data['song_name'].fillna(value='', inplace=True)
    data['text_feature'] = data['title'] + ' ' + data['song_name']
    
    # Store artifact
    logger.info('Storing artifact')
    data.to_csv('preprocessed_data.csv', index=False)
    artifact=wandb.Artifact(name=args.artifact_name,
                            type=args.artifact_type,
                            description=args.artifact_description)
    artifact.add_file("preprocessed_data.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    go(args)
