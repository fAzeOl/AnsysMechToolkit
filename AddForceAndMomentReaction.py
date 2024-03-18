"""
Author: Filipe Azevedo
Title: Add Force and Moment Reaction
Version: v1 
Created: 2024/02

Ansys version: 2021R2

## Description

This script automates the process of adding Force and Moment Reaction from contacts in Ansys Mechanical. 
Contacts are filtered based on a search parameter placed at the end of each contact's name.

## How to Use

1. Change the 'analysisNum' variable to specify the analysis you want to add the reaction to.
2. Define a search parameter to filter the contacts.
3. Run the script.


"""
#-----------------------------------------------------------------------------------------------------------------------------------#

analysesNum = 0
searchParm = "!"

#-----------------------------------------------------------------------------------------------------------------------------------#

#General
model = ExtAPI.DataModel.Project.Model
connections = model.Connections
analyses = model.Analyses[analysesNum]
solution = analyses.Solution
contactType = DataModelObjectCategory.ContactRegion

#Get list of contacts
contactList = []
for contact in connections.GetChildren(contactType,True):
    contactList.append(contact)

#Filter contacts by searchParm
contactListFiltered = []
for contact in contactList:
    if contact.Name.EndsWith(searchParm):
        contactListFiltered.append(contact)

#Add Force and Moment Reaction
for contact in contactListFiltered:
    #Add force reaction and change name
    force = solution.AddForceReaction()
    force.ContactRegionSelection = contact
    force.Name = "Force Reaction | " + contact.Name

    #Add moment reaction, set summation Point to Orientation System and Changes Name
    moment = solution.AddMomentReaction()
    moment.ContactRegionSelection = contact
    moment.Summation = MomentsAtSummationPointType.OrientationSystem
    moment.Name = "Moment Reaction | " + contact.Name
    
#Group all together
solution.GroupAllSimilarChildren()