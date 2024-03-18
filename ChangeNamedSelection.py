"""
Author: Filipe Azevedo
Title: Change Named Selection
Version: v1 
Created: 2024/02

Ansys version: 2021R2

## Description

This script automates the process of changing the name of Named Selections based on the folder's name and a provided suffix. 
For example, if the folder name is "folderExample" and the suffix is "_ex", the script will rename the Named Selections 
within that folder to "folderExample_ex1", "folderExample_ex2", and so on.

## How to Use

1. While creating Named Selections, group them together and change the folder name accordingly.
2. Change the variable 'suffix' to the desired suffix you want to add to the Named Selections.
3. Run the script.


"""
#-----------------------------------------------------------------------------------------------------------------------------------#

suffix = "_CS"

#-----------------------------------------------------------------------------------------------------------------------------------#

#General
selections = ExtAPI.DataModel.Project.Model.NamedSelections
treeObj = DataModelObjectCategory.TreeGroupingFolder
nsObj = DataModelObjectCategory.NamedSelection
treeACT = Ansys.ACT.Automation.Mechanical.TreeGroupingFolder
nsACT = Ansys.ACT.Automation.Mechanical.NamedSelection
folderId = {}
folderNames = []
folderCounter = 0
namedSelectionCounter = 1

#gets total number of folders and named selections in Tree
numTotal = len(selections.GetChildren(treeObj, True)) + len(selections.GetChildren(nsObj, True))

for i in range(0,numTotal):
    
    # Selects folder
    if selections.Children[i].GetType().Equals(treeACT):
        folder = selections.Children[i]
        folderNames.append(folder.Name)
        id = folder.ObjectId
        folderId[folder.Name] = id
        
    # Selects Named Selections
    elif selections.Children[i].GetType().Equals(nsACT):
        namedSelection = selections.Children[i]
        id = namedSelection.ObjectId
        
        # Verifies if selected Named Selections corresponds to the current folder or not
        if id < folderId.get(folderNames[folderCounter]):
            namedSelection.Name = "{}{}{}".format(folderNames[folderCounter],suffix,namedSelectionCounter)
            namedSelectionCounter = namedSelectionCounter + 1
        
        #If not, new folder is selected
        else:
            if len(folderNames) != folderCounter:
                folderCounter = folderCounter + 1
            namedSelectionCounter = 1
            namedSelection.Name = "{}_CS{}".format(folderNames[folderCounter],namedSelectionCounter)
            namedSelectionCounter = namedSelectionCounter + 1


