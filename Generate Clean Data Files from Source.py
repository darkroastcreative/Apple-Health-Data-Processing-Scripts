import logging
from datetime import datetime
from logging import Logger, basicConfig, getLogger

import pandas as pd
from pandas import DataFrame

import envconfig


def get_file_name_friendly_timestamp() -> str:
    """
    Obtains the current date and time and returns a string representing that
    point in time as a file name-friendly (timestamp) string.
    """
    return datetime.now().strftime('%Y%m%dT%H%M%S')


# Declare and initialize a string representing a timestamp that can be used in
# export files. This variable is used to ensure timestamps are consistent
# across all files this script generates in a given execution.
timestamp_string: str = get_file_name_friendly_timestamp()

# Declare, initialize, and configure a Logger object to log script events.
logger: Logger = getLogger(name='Generate Clean Data Files from Source')
basicConfig(filename=f'Generate Clean Data Files from Source {timestamp_string}.log', encoding='utf-8',
            filemode='w', level=logging.INFO, format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')

logger.info('Starting.')

# Read in the raw XML data file from Apple Health.
logger.info('Reading in source data file.')
df: DataFrame = pd.read_xml(path_or_buffer=envconfig.HEALTH_DATA_SOURCE_PATH)
logger.info('Source data file read. Resulting DataFrame shape: {df.shape}')

# Drop columns that I don't really care about right now. I'm doing this
# primarily for performance reasons.
logger.info('Dropping unnecessary columns.')
df = df.drop(columns=['HKCharacteristicTypeIdentifierDateOfBirth', 'HKCharacteristicTypeIdentifierBiologicalSex', 'HKCharacteristicTypeIdentifierFitzpatrickSkinType', 'HKCharacteristicTypeIdentifierBloodType', 'HKCharacteristicTypeIdentifierCardioFitnessMedicationsUse', 'workoutActivityType',
             'WorkoutStatistics', 'WorkoutRoute', 'WorkoutEvent', 'activeEnergyBurned', 'activeEnergyBurnedGoal', 'activeEnergyBurnedUnit', 'appleMoveTime', 'appleMoveTimeGoal', 'appleExerciseTime', 'appleExerciseTimeGoal', 'appleStandHours', 'appleStandHoursGoal', 'RightEye', 'LeftEye'])
logger.info('Unnecessary columns dropped.')

# TODO: Add step in the process to rename the remaining columns to more useful things.

# Export a copy of the cleaned data as a CSV file.
logger.info('Exporting cleaned data as CSV file.')
df.to_csv(
    path_or_buf=f'Apple Health {timestamp_string} Cleaned.csv', index=False)
logger.info('CSV file exported.')

# If envconfig's DATA_SAMPLE_SIZE is set to a value greater than zero
# (indicating desire for a data sample), proceed to generate the sample.
if envconfig.DATA_SAMPLE_SIZE > 0:
    logger.info('Creating data sample file.')
    df = df.sample(envconfig.DATA_SAMPLE_SIZE)
    df.to_csv(
        path_or_buf=f'Apple Health {timestamp_string} Cleaned Sample.csv', index=False)
    logger.info('Data sample file created.')
else:
    logger.info('Skipping data sample creation due to DATA_SAMPLE_SIZE setting.')

logger.info('Completed.')
