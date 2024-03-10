# The desired number of records to be included in the "sample" file exported
# by the "Generate Clean Data Files from Source" script. If no sample sample
# file is desired, set this value to 0 (or less than 0).
DATA_SAMPLE_SIZE: int = 1000

# File path to "export.xml" from the targeted (uncompressed) Apple Health data
# export.
HEALTH_DATA_SOURCE_PATH: str = r'/home/david/Sync/apple_health_export/export.xml'

# The desired types of health data to include. If this list is empty, all
# available sample types will be included.
TARGETED_SAMPLE_TYPES: list = ['HKCategoryTypeIdentifierSleepAnalysis', 'HKQuantityTypeIdentifierOxygenSaturation']
