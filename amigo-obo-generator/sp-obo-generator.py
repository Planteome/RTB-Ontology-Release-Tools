#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pronto import Ontology
import pronto
import pandas as pd
import re

parser = argparse.ArgumentParser(description='Generate OBO File from TD')
parser.add_argument('current_obo', type=Path, help='current obo file')
parser.add_argument('input_path', type=str, help='Input Excel Path')
parser.add_argument('output_path', type=str, help='Output OBO Path')
args = parser.parse_args()

#### get template
path = args.input_path.strip()
df = pd.read_excel(io=path, sheet_name="Template for submission")

### open RTB master obo file
with args.current_obo.open() as myobo:
    o = Ontology(myobo.name)

new_vars = []

##replace all na to empty string
df.fillna('', inplace=True)

## get all the custom properties that already exist in the obo file
variableOf = o.get_relationship('variable_of')
methodOf = o.get_relationship('method_of')
scaleOf = o.get_relationship('scale_of')

## read df 
for index, row in df.iterrows():
    ## get row info
    varID = row["Variable ID"].strip()
    varName = row["Variable name"].strip()
    varDef  = row["Variable description"].strip()
    varSyn  = row["Variable synonyms"].strip()
    #varSyn_other = row["Variable synonyms"].strip()
    varCreator  = str(row["Scientist"]).strip()
    varCreationDate  = str(row["Date"]).strip()
    varCrop  = str(row["Crop"]).strip()
    traitID  = str(row["Trait ID"]).strip()
    traitName  = row["Trait name"].strip().lower()
    traitClass  = row["Trait class"].strip()
    traitDef  = row["Trait description"].strip()
    traitSyn = row["Main trait abbreviation"].strip()
    traitXref  = row["Trait Xref"].strip()
    methodID = row["Method ID"].strip()
    methodName  = row["Method name"].strip().lower()
    methodClass  = row["Method class"].strip()
    methodDef  = row["Method description"].strip()
    #formula  = row["Formula"].strip()
    methodXref  = row["Method reference"].strip()
    scaleID  = str(row["Scale ID"]).strip()
    scaleName  = row["Scale name"].strip()
    scaleClass  = row["Scale class"].strip()
    
    ## create variable term
    variable = o.create_term(varID) # Create new Term with given ID
    variable.name = varName
    variable.definition = pronto.Definition(varDef)
    variable.created_by = varCreator
    ##variable.creation_date = varCreationDate ## since dates are entrered using different format, hard to parse with datetime ## TODO

    if not traitID in o.terms():
        o.create_term(traitID)
    if not methodID in o.terms():
        o.create_term(methodID)
    if not scaleID in o.terms():
        o.create_term(scaleID)

    variable.relationships = {variableOf: {o[traitID], o[methodID], o[scaleID]}}
    
    try :
        variable.superclasses().add(o["Variable"])  
    except: 
        ### id is numerical
        ### superclasses should already be in ontolgy
        varClass = next((x for x in o.terms() if x.name == "Variable"), None)
        if varClass is not None:
            variable.superclasses().add(varClass)
        else:
            print("Variable class not added for term:"+variable.name)

    
    variable.namespace = varCrop+"Trait" 
    
    if varSyn:
        for vs in varSyn.split(","):
            variable.add_synonym(vs, scope='EXACT')  
        
    
    ##create trait term
    trait = o.get_term(traitID)
    trait.name = traitName
    trait.definition = pronto.Definition(traitDef)
    try :
        trait.superclasses().add(o[traitClass])  
    except: 
        ### id is numerical
        ### superclasses should already be in ontolgy
        traitC = next((x for x in o.terms() if x.name == traitClass), None)
        if traitC is not None:
            trait.superclasses().add(traitC)
        else:
            traitC = next((x for x in o.terms() if x.name == traitClass+"_trait"), None)
            if traitC is not None:
                trait.superclasses().add(traitC)
            else:
                print("Trait class not added for term:"+trait.name)
    
    trait.namespace = varCrop+"Trait" 

    if traitSyn:
        for ts in traitSyn.split(","):
            trait.add_synonym(ts, scope='EXACT')  
    
    
    ## create method term
    method = o.get_term(methodID)
    method.name = methodName
    method.definition = pronto.Definition(methodDef)
    ##look for method class ID - should be already created.
    try :
        method.superclasses().add(o[methodClass])  
    except: 
        ### id is numerical
        ### superclasses should already be in ontolgy
        methodC = next((x for x in o.terms() if x.name == methodClass), None)
        if methodC is not None:
            method.superclasses().add(methodC)
        else:
            print("Method class not added for term:"+method.name)
    
    method.namespace = varCrop+"Method"
    
    method.relationships = {methodOf: {o[traitID]}}
    
    ## create scale term
    scale = o.get_term(scaleID)
    scale.name = scaleName
    # look for scale id
    try :
        scale.superclasses().add(o[scaleClass])  
    except: 
        ### id is numerical
        ### superclasses should already be in ontolgy
        scaleC = next((x for x in o.terms() if x.name == scaleClass), None)
        if scaleC is not None:
            scale.superclasses().add(scaleC)
        else:
            print("Scale class not added for term:"+scale.name)
    
    scale.namespace = varCrop+"Scale"
    
    scale.relationships = {scaleOf: {o[methodID]}}

outputfile = args.output_path.strip()    
with open(outputfile, "wb") as f:
    o.dump(f, format="obo")
