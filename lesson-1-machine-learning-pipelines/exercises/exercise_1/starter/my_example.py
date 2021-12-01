import argparse
import wandb
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

def go(args):
    """
    Loads an artefact onto wandb
    """
    logger.info('Uploading the artifact')
    # create an artefact
    artefact = wandb.Artifact(name=args.artifact_name,
                            type=args.artifact_type,
                            description=args.artifact_description)

    # Upload to wandb
    run = wandb.init(job_type='Upload file',
                    project='Exercise 1')

    artefact.add_file('lesson-1-machine-learning-pipelines\exercises\exercise_1\starter\zen.txt',
                        name=args.artifact_name)

    run.log_artifact(artefact)

    run.finish()

if __name__ == '__main__':

    # Create parser object
    parser = argparse.ArgumentParser(description='Used to get arguments to be used for the go function')

    # Specify arguments
    parser.add_argument('--artifact_name', type=str, help='Takes name of artefact', required=True)
    parser.add_argument('--artifact_type', type=str, help='Takes type of artefact', required=True)
    parser.add_argument('--artifact_description',
                         type=str, 
                         help='Takes description of artefact',
                         required=False,
                         default='Uploading file')
    
    # Define args
    args = parser.parse_args()

    # Run function
    go(args)
    


