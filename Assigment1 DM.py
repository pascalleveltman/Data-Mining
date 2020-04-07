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

pd.set_option('display.max_columns', 30)

prep_DF = convert_to_data_frame(preparedData)
print(prep_DF.loc[:, ' "sms" '])

# for pID in patientIDs:
#     smspid = prep_DF[pID][:]['"sms"']
#     print(smspid)
