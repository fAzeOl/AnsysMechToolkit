"""
Author: Filipe Azevedo
Title: Add Construction Surface
Version: v1 
Created: 2024/02

Ansys version: 2021R2

## Description

This script adds a Construction Surface to the model in Ansys Mechanical. 
The Construction Surface is added based on a specified Coordinate System with a search parameter at the start of the Coordinate System Name.

## How to Use

1. Select a search parameter at the start of the Coordinate System Name.
2. Run the script.


"""



#-----------------------------------------------------------------------------------------------------------------------------------#

searchParm = "!"

#-----------------------------------------------------------------------------------------------------------------------------------#

#General
model = ExtAPI.DataModel.Project.Model
csysModel = model.CoordinateSystems
conSurf = model.ConstructionGeometry
csysObj = Ansys.ACT.Automation.Mechanical.CoordinateSystem

#Get list of csys
csysIndex = []
for csys in range(0, csysModel.Children.Count):
    if csysModel.Children[csys].GetType().Equals(csysObj) and csysModel.Children[csys].Name.StartsWith(searchParm):
        csysIndex.append(csys)

#Add Surface
for csys in csysIndex:
    surf = conSurf.AddSurface()
    surfIndex = conSurf.Children.Count
    conSurf.Children[surfIndex-1].CoordinateSystem = csysModel.Children[csys]
