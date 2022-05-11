#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pronto import Ontology
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
    o = Ontology(myobo.name)

for term in o.terms():
    ### get the variables info
    if(sorted(term.relationships.keys())):
        if(sorted(term.relationships.keys())[0].name == "variable_of"):
            ### get var info - need to split to get the values only!!
            ## var ID 
            varID = term.id
            #print(varID)
            ## var name
            varName = term.name
            #print(varName)
            ## var def
            varDef = term.definition
            varSyn = []
            for s in term.synonyms:
                varSyn.append(s.description)
            #print(varSyn)
            varXref = []
            for x in term.xrefs:
                xref.append(x.description)
            #print(varXref)
            varCreator = term.created_by
            varDate = term.creation_date
                
            ### in cassava, variables that are subclasses of farmer trait are PVS var.
            #### Needs to be added in the context of use 
            # varContextOfUse = "Breeding trials"
            # if ('is_a' in term):    
            #     for itemValues in term["is_a"]:
            #         varClass = str(itemValues).split("! ")[1]
            #         if "Farmer trait" in varClass:
            #             varContextOfUse = "Farmer Trait"
                
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

            #print(term.relationships[o.get_relationship('variable_of')])
            for t in term.relationships[o.get_relationship('variable_of')]:
                if "Trait" in t.namespace:
                    ##trait ID
                    traitID = t.id
                    #print(traitID)

                    ## trait name
                    traitName = t.name
                    #print(traitName)

                    ## trait syn
                    for ts in t.synonyms:
                        traitSyn.append(ts.description)
                    #print(traitSyn)

                    ## trait def
                    traitDef = t.definition
                    #print(traitDef)
                    ## trait class
                    for tsc in t.superclasses(with_self=False, distance=1):
                        traitClass = tsc.name
                    #print(traitClass) 
                    ### trait xref
                    for tx in t.xrefs:
                        traitXref.append(tx.description)
                    #print(traitXref)
                elif "Method" in t.namespace:
                    ##method ID
                    methodID = t.id
                    #print(methodID)

                    ## method name
                    methodName = t.name
                    #print(methodName)

                    ## method def
                    methodDef = t.definition
                
                    ## method class
                    for tsc in t.superclasses(with_self=False, distance=1):
                        methodClass = tsc.name
                    #print(methodClass) 

                    ### method xref
                    for tx in t.xrefs:
                        methodXref.append(tx.description)
                    #print(methodXref)
                elif "Scale" in t.namespace: ## scale
                    ##scale ID
                    scaleID = t.id
                    #print(scaleID)

                    ## scale name
                    scaleName = t.name                    
                    #print(scaleName)

                    ## scale type
                    for tsc in t.superclasses(with_self=False, distance=1):
                        scaleClass = tsc.name
                    #print(scaleClass)

                    ### method xref
                    for tx in t.xrefs:
                        scaleXref.append(tx.description)
                    #print(scaleXref)

                    ### get the scale categories
                    if("pt scale" in scaleName):
                        regex = r"""[0-9] ?= ?[a-z -]+"""
                        categories= re.compile(regex, flags=re.IGNORECASE).findall(varDef)
                        #print(categories)
                else:
                    print("This variable is not formatted correctly: " + term)
        
            df = df.append({'Variable ID' : varID , 
                        "Variable name": varName,
                        "Variable synonyms": ','.join(varSyn), 
                        "Variable description": varDef, 
                        "Context of use": "",#varContextOfUse, 
                        "Growth stage": "", "Variable status": "Recommended",
                        "Variable Xref": ','.join(varXref), #varXref,
                        "Institution": "", 
                        "Scientist": varCreator, 
                        "Date": varDate, 
                        "Language": "EN", 
                        "Crop": "Yam", 
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
