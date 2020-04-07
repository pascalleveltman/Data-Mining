import numpy as np
from numpy import cov
import sys
import pandas as pd

np.set_printoptions(threshold=sys.maxsize)  # show full table
np.seterr(divide='ignore', invalid='ignore')  # no warnings

END_DATE_ELEMENT = 10 # day from date
FILE_NAME = "/Users/pascalleveltman/Downloads/Data Mining/dataset_mood_smartphone.csv"

def read_data():
    with open(FILE_NAME) as file:
        data_matrix = np.array([np.array(line.rstrip('\n').split(',')) for line in file])
    return data_matrix

def calculate_mean_scores(preparedData):
    preparedData[0] = preparedData[0] / preparedData[amountOfAttributes]
    preparedData[14] = preparedData[14] / preparedData[amountOfAttributes + 1]
    preparedData[15] = preparedData[15] / preparedData[amountOfAttributes + 2]
    preparedData[16] = preparedData[16] / preparedData[amountOfAttributes + 3]
    return preparedData

def fill_in_data(preparedData):
    for row in dataMatrix[1:]:
        indexAttribute = int(np.where(attributes == row[3])[0])
        indexPatient = int(np.where(patientIDs == row[1])[0])  # index patient from 0
        indexDate = int(np.where(days == row[2][0:END_DATE_ELEMENT])[0])
        if row[4] != 'NA':
            preparedData[indexAttribute][indexPatient][indexDate] += float(row[4])
            if row[3] in scoreAttributes:
                indexScoreAttributes = int(np.where(scoreAttributes == row[3])[0])  # 1st 2nd 3rd 4th score attribute?
                preparedData[amountOfAttributes + indexScoreAttributes][indexPatient][
                    indexDate] += 1  # amount of score attributes to take mean later
    preparedData = calculate_mean_scores(preparedData)
    return preparedData

def create_prepared_data():
    preparedData = np.zeros((amountOfAttributes + amountOfScoreAttributes, amountOfPatients, amountOfDays))
    preparedData = fill_in_data(preparedData)
    # we don't need the last 4 columns anymore
    preparedData = preparedData[0:amountOfAttributes]
    return(preparedData)

def convert_to_data_frame(preparedData):
    preparedData = np.swapaxes(preparedData, 0, 2)
    index = pd.MultiIndex.from_tuples([], names=('Patient ID', 'Day'))
    preparedDataFrame = pd.DataFrame(index=index, columns=attributes)

    for patient in range(amountOfPatients):
        for day in range(amountOfDays):
            indexNew = pd.MultiIndex.from_tuples([(patientIDs[patient], days[day])], names=('Patient ID', 'Day'))
            rowAddition = pd.DataFrame(index=indexNew, columns=attributes, data=[preparedData[day][patient]])
            preparedDataFrame = pd.concat([preparedDataFrame, rowAddition])
    return preparedDataFrame

dataMatrix = read_data()

days = np.unique([element[0:END_DATE_ELEMENT] for element in dataMatrix[1:, 2]])
patientIDs = np.unique(dataMatrix[1:, 1])
attributes = np.unique(dataMatrix[1:, 3])
scoreAttributeNames = attributes[0], attributes[14], attributes[15], attributes[16]
scoreAttributes = np.asarray(scoreAttributeNames)

amountOfAttributes = len(attributes)  # 19 attributes
amountOfPatients = len(patientIDs)   # 27 patients
amountOfDays = len(days)  # 113 days
amountOfScoreAttributes = len(scoreAttributes)  #4

preparedData = create_prepared_data()

# Some notes to self
pd.set_option('display.max_columns', 30)
prep_DF = convert_to_data_frame(preparedData)
columnnames = prep_DF.columns
mood_index = 16
n_obs = 3051

# See what the missing data is
print("Observations left if no NaN of 3051")
for i in range(columnnames.shape[0]):
    array = prep_DF.loc[:, [columnnames[i]]]
    array = array.dropna()
    # array = array[(array.T != 0).any()]
    print(columnnames[i], ":", array.shape[0])

# See correlation between variables
select = prep_DF.loc[:, [columnnames[17], columnnames[16]]]
select = select.dropna()
# select = select[(select.T != 0).any()]
# print(select.shape[0])
corselect = select.corr()
print(corselect)
# And correlation between whole dataset
corDF = prep_DF.dropna()
corDF.corr()

# Make new dataframe,
new_DF = prep_DF.loc[:, [columnnames[0], columnnames[14], columnnames[15], columnnames[16], columnnames[17]]]
new_DF["work"] = prep_DF[columnnames[4]] + prep_DF[columnnames[6]] # finance and office
new_DF["social"] = prep_DF[columnnames[8]] + prep_DF[columnnames[9]] # social and travel
new_DF["speaking"] = prep_DF[columnnames[18]] + prep_DF[columnnames[13]] + prep_DF[columnnames[2]] # sms call communication
new_DF["play"] = prep_DF[columnnames[3]] + prep_DF[columnnames[5]] # entertainment and game
new_DF["total"] = new_DF["work"] + new_DF["social"] + new_DF["speaking"] + new_DF["play"] # just to check the screen time
print(new_DF)
