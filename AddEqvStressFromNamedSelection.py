
"""
Author: Filipe Azevedo
Title: Add Eqv Stres from Named Selection
Version: v1 
Created: 2024/02

Ansys version: 2021R2

## Description

This script automates the process of adding Equivalent Stress to each Named Selection in the Model tree and for each time step in the analysis in Ansys Mechanical. 
It specifically targets Named Selections stored inside folders, and the Equivalent Stresses are organized into folders with the same name as the folder storing the Named Selection.

## How to Use

1. Change the 'analysisNum' variable to specify the analysis you want to add results to. Note: The sequence of analyses starts from 0.
2. Run the script.


"""

#-----------------------------------------------------------------------------------------------------------------------------------#

#Select Analysis
analysisNum = 0

#-----------------------------------------------------------------------------------------------------------------------------------#

#Global
model = ExtAPI.DataModel.Project.Model
analysis = ExtAPI.DataModel

#Timesteps
def getTimeSteps(analysisNum):
    time_stepsCount = model.Analyses[analysisNum].AnalysisSettings.InternalObject.NumberOfSteps
    return time_stepsCount

#Convert Named Selection to Element Selection
def convertToMeshData(namedSelection, currentAnalysis):
    f=namedSelection.Location.Ids
    meshData = model.Analyses[currentAnalysis].MeshData #ExtAPI.DataModel.Project.Model.Analyses[0].MeshData
    faceMesh = meshData.MeshRegionById(f[0])
    nodes=faceMesh.NodeIds
    faceMesh = meshData.MeshRegionById(f[0])
    faceElement = meshData.ElementIdsFromNodeIds(nodes)
    #faceElementId = meshData.Elements
    return faceElement

#Add Equivalent Stress based on Element Selection, time step and changes name
def addEqvStress(faceElement, timeStep, name):
    sm = ExtAPI.SelectionManager
    sm.ClearSelection()
    selectionInfo = sm.CreateSelectionInfo(SelectionTypeEnum.MeshElements)
    selectionInfo.Ids = faceElement
    sm.NewSelection(selectionInfo)
    rst = model.Analyses[analysisNum].Solution.AddEquivalentStress()
    rst.DisplayTime = Quantity("{} [sec]".format(timeStep))
    rst.Name = rst.Name + " | {} | t={}".format(name,timeStep)

#Number of Analysis
analysisCount = analysis.AnalysisList.Count
analysisList = []
for i in range(0, analysisCount):
    analysisList.append(i)


#Collecting Folder Names and Ids
it = 0
folderId = []
folderName = []
while True:
    if model.NamedSelections.Children[it].GetType().Equals(Ansys.ACT.Automation.Mechanical.TreeGroupingFolder):
        folder = model.NamedSelections.Children[it]
        id = folder.ObjectId
        folderId.append(id)
        folderName.append(folder.Name)
        it = it + 1
    else:
        break

#Creates EquivalentStress Results for each Named Selection
nsNum = model.NamedSelections.Children.Count
folderNum = range(0, it)
folderCount = 0
timeSteps = getTimeSteps(analysisNum)

for ns in range(it, nsNum): #ignores all folder, and starts from first named selection
    namedSelection = model.NamedSelections.Children[ns]
    id = namedSelection.ObjectId
    if id < folderId[folderCount]:
        faceElement = convertToMeshData(namedSelection, analysisNum)
        for time in range(1,timeSteps+1): #plots Equivalent Stress for all time steps in the analysis
            addEqvStress(faceElement, time, namedSelection.Name)
    else: #checks if id from named selection is greater than current id from folder. If so, it changes to next folder
        model.Analyses[analysisNum].Solution.GroupAllSimilarChildren() #groups all stress to a folder before plotting the next
        solutionNum = model.Analyses[analysisNum].Solution.Children.Count
        model.Analyses[analysisNum].Solution.Children[solutionNum-1].Name = folderName[folderCount] #changes name of folder 
        folderCount = folderCount + 1
        if folderCount == len(folderId): #no named selection outside folderes are considered
            break
        else:
            faceElement = convertToMeshData(namedSelection, 0)
            for time in range(1,timeSteps+1):
                addEqvStress(faceElement, time, namedSelection.Name)


