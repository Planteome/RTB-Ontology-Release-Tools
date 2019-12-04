#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pyobo
import pandas as pd
import re

parser = argparse.ArgumentParser(description='Generate Excel File from OBO')
parser.add_argument('empty_template', type=str, help='empty Trait Dictionary')
parser.add_argument('input_path', type=Path, help='Input OBO Path')
parser.add_argument('output_path', type=str, help='Output Excel Path')
args = parser.parse_args()

## open TD
path = args.empty_template.strip()
df = pd.read_excel(io=path, sheet_name="Template for submission")

row_list = []

### open RTB master obo file
with args.input_path.open() as myobo:
    o = pyobo(myobo)

for term in o.getTerms():
    ### get the variables info
    if "variable_of" in str(term["relationship"]):
        ### get var info - need to split to get the values only!!
        ## var ID 
        varID = str(term["id"]).split(": ")[1]
        #print(varID)
        ## var name
        varName = str(term["name"]).split(": ")[1]
        #print(varName)
        ## var def
        varDef = ""
        if ('def' in term):
            varDef = str(term["def"]).split('"')[1].split('"')[0]
            #print(varDef)
        varSyn = []
        if('synonym' in term):
            for i in range(len(term["synonym"])):
                syn = str(term["synonym"][i-1]).split('"')[1].split('"')[0]
                varSyn.append(syn)
        #print(varSyn)
        varXref = ""
        if ('xref' in term):
            for itemValues in term["xref"]:
                varXref = str(itemValues).split(": ")[1] #.split("value='")[1].split("'")[0] ### ugly!
        #print(varXref)
        varCreator = ""
        if ('created_by' in term):
            varCreator = str(term["created_by"]).split(": ")[1]
            #print(varCreator)   
        varDate = ""
        if ('creation_date' in term):
            varDate = str(term["creation_date"]).split(": ")[1]
            #print(varDate)   
            
        ### in cassava, variables that are subclasses of farmer trait are PVS var.
        #### Needs to be added in the context of use 
        varContextOfUse = "Breeding trials"
        if ('is_a' in term):    
            for itemValues in term["is_a"]:
                varClass = str(itemValues).split("! ")[1]
                if "Farmer trait" in varClass:
                    varContextOfUse = "Farmer Trait"
            
        traitID = ""
        traitName = ""
        traitSyn = []
        traitDef = ""
        traitClass = ""
        traitXref = ""
        methodID = ""
        methodName = ""
        methodDef = ""
        methodClass = ""
        methodXref = ""
        scaleID = ""
        scaleName = ""
        scaleClass = ""
        scaleXref = ""
        categories = []
        
        for i in range(len(term["relationship"])): ### need to check that this is an variable_of
            if "variable_of" in str(term["relationship"][i-1]):
                element = str(term["relationship"][i-1]).split(" ")[2] ##CO ID
                name = str(term["relationship"][i-1]).split("! ")[1]


                if("namespace" in o[element]):
                    ##########################
                    ### get the trait info
                    ##########################
                    if("trait" in str(o[element]["namespace"]).lower()):
                        ##trait ID
                        traitID = str(o[element]["id"]).split(": ")[1]
                        #print(traitID)
                        #print(traitID.split(" ")[1]==element)
                        ## trait name
                        traitName = str(o[element]["name"]).split(": ")[1]
                        #print(traitName)
                        ## trait syn
                        
                        if('synonym' in o[element]):
                            for i in range(len(o[element]["synonym"])):
                                syn = str(o[element]["synonym"][i-1]).split('"')[1].split('"')[0]
                                traitSyn.append(syn)
                        #print(traitSyn)
                        ## trait def
                        
                        if ('def' in o[element]):
                            traitDef = str(o[element]["def"]).split('"')[1].split('"')[0]
                            #print(traitDef)
                        ## trait class
                        
                        for itemValues in o[element]["is_a"]:
                            traitClass = str(itemValues).split("! ")[1]
                        #print(traitClass) ## need to split to get the name
                        ### trait xref
                        
                        if ('xref' in o[element]):
                            for itemValues in o[element]["xref"]:
                                traitref = str(itemValues).split(": ")[1]
                        #print(traitXref)
                        
                    ###########################@    
                    ### get the method info
                    ############################
                    elif("method" in str(o[element]["namespace"]).lower()):
                        ##method ID
                        methodID = str(o[element]["id"]).split(": ")[1]
                        #print(methodID)
                        ## method name
                        methodName = str(o[element]["name"]).split(": ")[1]
                        #print(methodName)
                        ## method def
                        
                        if ('def' in o[element]):
                            methodDef = str(o[element]["def"]).split('"')[1].split('"')[0]
                            #print(methodDef)
                        ## method class
                       
                        for itemValues in o[element]["is_a"]:
                            methodClass = str(itemValues).split("! ")[1]
                        #print(methodClass) ## need to split to get the name
                        ### method xref
                        
                        if ('xref' in o[element]):
                            for itemValues in o[element]["xref"]:
                                methodref = str(itemValues).split(": ")[1]
                        #print(methodXref)
                        
                    #######################
                    ### get the scale info
                    ########################
                    elif("scale" in str(o[element]["namespace"]).lower()):
                        ##scale ID
                        scaleID = str(o[element]["id"]).split(": ")[1]
                        #print(scaleID)
                        ## scale name
                        scaleName = str(o[element]["name"]).split(": ")[1]
                        #print(scaleName)
                        ## scale type
                        
                        for itemValues in o[element]["is_a"]:
                            scaleClass = str(itemValues).split("! ")[1]
                        #print(scaleClass) ## need to split to get the name
                        ### method xref
                        
                        if ('xref' in o[element]):
                            for itemValues in o[element]["xref"]:
                                scaleXref = str(itemValues).split(": ")[1]
                        #print(scaleXref)
                        ### get the scale categories
                        
                        if("pt scale" in scaleName):
                            regex = r"""[0-9] ?= ?[a-z -]+"""
                            categories= re.compile(regex, flags=re.IGNORECASE).findall(varDef)
                            #print(categories)
                        
                else:
                    print(element)
    
        df = df.append({'Variable ID' : varID , 
                    "Variable name": varName,
                    "Variable synonyms": ','.join(varSyn), 
                    "Variable description": varDef, 
                    "Context of use": varContextOfUse, 
                    "Growth stage": "", "Variable status": "Recommended",
                    "Variable Xref": varXref,
                    "Institution": "IITA", 
                    "Scientist": varCreator, 
                    "Date": varDate, 
                    "Language": "EN", 
                    "Crop": "Cassava", 
                    "Trait ID": traitID, 
                    "Trait name": traitName, "Trait class": traitClass, 
                    "Trait description": traitDef, 
                    "Trait synonyms": ','.join(traitSyn), 
                    "Main trait abbreviation": "", 
                    "Alternative trait abbreviations": "", 
                    "Entity": "", "Attribute": "", 
                    "Trait status": "Recommended", 
                    "Trait Xref": traitXref, 
                    "Method ID": methodID, 
                    "Method name": methodName, 
                    "Method class": methodClass, 
                    "Method description": methodDef, 
                    "Formula": "", 
                    "Method reference": methodXref, 
                    "Scale ID": scaleID, 
                    "Scale name": scaleName, 
                    "Scale class": scaleClass, 
                    "Decimal places": "", 
                    "Lower limit": "", 
                    "Upper limit": "", 
                    "Scale Xref": scaleXref, 
                    "Category 1": '\t'.join(categories)} , ignore_index=True)
    
#### print    
#print(df)
### remove duplicated rows
df = df.drop_duplicates()

# Create a Pandas Excel writer using XlsxWriter as the engine.
outputfile = args.output_path.strip()
writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()    
