#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pyobo
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
    o = pyobo(myobo)

new_vars = []

## read df 
for index, row in df.iterrows():
    ## get row info
    varID = row["Variable ID"].strip()
    varName = row["Variable label"].strip()
    varDef  = row["Variable description"].strip()
    varSyn  = row["Variable name"].strip()
    varSyn_other = row["Variable synonyms"].strip()
    varCreator  = str(row["Scientist"]).strip()
    traitID  = str(row["Trait ID"]).strip()
    traitName  = row["Trait name"].strip().lower()
    traitClass  = row["Trait class"].strip()
    traitDef  = row["Trait description"].strip()
    traitSyn = row["Main trait abbreviation"].strip()
    #traitXref  = row["Trait Xref"].strip()
    methodID = row["Method ID"].strip()
    methodName  = row["Method name"].strip().lower()
    methodClass  = row["Method class"].strip()
    methodDef  = row["Method description"].strip()
    #formula  = row["Formula"].strip()
    #methodXref  = row["Method reference"].strip()
    scaleID  = str(row["Scale ID"]).strip()
    scaleName  = row["Scale name"].strip()
    scaleClass  = row["Scale class"].strip()
    
    ## create obo term
    variable = o.Term(varID)           # Create new Term with given ID (returns ref to created obj)
    variable["name"] = varName
    variable["def"] = '"'+varDef.replace('"','')+'" []'
    #variable["creator"] = varCreator ## does not work
    #variable["relationship"] = ["variable_of", traitID] ##does not work
    #variable["relationship"] = ["variable_of", methodID]##does not work
    #variable["relationship"] = []"variable_of", scaleID]##does not work
    for term in o.getTerms():
        #for i in range(len(term["is_a"])):
        if "variables" in str(term["name"]).lower():
            var_classID = str(term["id"]).split(": ")[1]
            
    var_trait = "relationship: variable_of "+ traitID +" ! "+traitName +"\n"
    var_method = "relationship: variable_of "+ methodID +" ! "+methodName +"\n"
    var_scale = "relationship: variable_of "+ scaleID +" ! "+scaleName +"\n"
    
    var_class = "is_a: " + var_classID +" ! Variables"
    
    var_namespace = "namespace: SweetpotatoTrait"
    
    var_name_def = str(variable).split("\n")
    var_name_def.insert(3,var_namespace)
    
    var_syn = ""
    if(varSyn):
        var_syn = 'synonym: "'+varSyn+'" EXACT []'
    if(varSyn_other):
        for s in varSyn_other.split(","):
            var_syn += '\nsynonym: "'+s+'" EXACT []'
    
    str_var = "\n".join(var_name_def)+"\n"+var_syn+"\n"+var_class+"\n"+var_trait+var_method+var_scale
    
    
    ##create trait term
    trait = o.Term(traitID)
    trait["name"] = traitName
    trait["def"] = '"'+traitDef.replace('"','')+'" []'
    #trait["is_a"] = traitClass ## does not work
    ##look for trait class ID - should be already created.
    
    for term in o.getTerms():
        #for i in range(len(term["is_a"])):
        if traitClass.lower().replace(" ", "_") in str(term["name"]).lower():
            trait_classID = str(term["id"]).split(": ")[1]
            
    trait_class = "is_a: "+ trait_classID +" ! "+ traitClass+"\n"
    
    trait_namespace = "namespace: SweetpotatoTrait"
    
    trait_name_def = str(trait).split("\n")
    trait_name_def.insert(3,trait_namespace)
    
    trait_syn = ""
    if(traitSyn):
        trait_syn = 'synonym: "'+traitSyn+'" EXACT []'
    
    str_trait = "\n".join(trait_name_def)+"\n"+trait_syn+"\n"+trait_class
    
    ## create method term
    method = o.Term(methodID)
    method["name"] = methodName
    method["def"] = '"'+methodDef.replace('"','')+'" []'
    ##look for method class ID - should be already created.
    method_classID=""
    for term in o.getTerms():
        #for i in range(len(term["is_a"])):
        if "name: "+methodClass.lower() == str(term["name"]).lower():
            method_classID = str(term["id"]).split(": ")[1]
    
    method_class = "is_a: " + method_classID +" ! "+ methodClass+"\n"
    
    method_namespace = "namespace: SweetpotatoMethod"
    
    method_name_def = str(method).split("\n")
    method_name_def.insert(3,method_namespace)
    
    trait_method = "relationship: method_of "+ traitID +" ! "+ traitName +"\n"
    
    str_method = "\n".join(method_name_def) +"\n"+ method_class + "\n"+ trait_method
    
    ## create scale term
    scale = o.Term(scaleID)
    scale["name"] = scaleName
    ##look for method class ID - should be already created.
    for term in o.getTerms():
        #for i in range(len(term["is_a"])):
        if scaleClass.lower() in str(term["name"]).lower():
            scale_classID = str(term["id"]).split(": ")[1]
    
    scale_class = "is_a: "+ scale_classID +" ! "+ scaleClass+"\n"
    
    scale_namespace = "namespace: SweetpotatoScale"
    
    scale_name_def = str(scale).split("\n")
    scale_name_def.insert(3,scale_namespace)
    
    scale_method = "relationship: scale_of "+ methodID +" ! "+ methodName +"\n"
    
    str_scale = "\n".join(scale_name_def)+"\n"+scale_class+"\n"+ scale_method
    
    #print(str_scale)
    #print(str_method)
    #print(str_trait)  
    #print(str_var)
    
    new_vars.append(str_var)
    new_vars.append(str_trait)
    new_vars.append(str_method)
    new_vars.append(str_scale)

## sort new_vars
new_vars.sort()
#print(new_vars)

## add the term in the file
new_obo = "format-version: 1.2\ndate: 12:02:2018 19:35\nsaved-by: vagrant\nauto-generated-by: OBO-Edit 2.3.1\ndefault-namespace: SweetpotatoDefault\n"
new_obo += "\n[Term]\n"
new_obo += "id: CO_331:0000000\n"
new_obo += "name: CGIAR sweetpotato trait ontology\n"
new_obo += "namespace: SweetpotatoTrait\n"
new_obo += 'def: "A controlled vocabulary to describe each trait as a distinguishable, characteristic, quality or phenotypic feature of a developing or mature sweetpotato plant." []\n'


for term in o.getTerms():
    term_id = term["id"]
    #new_obo += "\n" + str(term)+"\n"
    #try:
        #if (str(term["id"]) < new_vars[0]):
            #new_obo += "\n" + str(term)+"\n"
        #else:
            #new_obo += "\n" + str(term)+new_vars[0]+"\n"
            #del new_vars[0]
    #except:
        #new_obo += "\n" + str(term)+"\n"
        #next
        
new_obo += "\n" + '\n'.join(new_vars)

new_obo += "[Term]\n"
new_obo += "id: CO_331:1000001\n"
new_obo += "name: Methods\n"
new_obo += "namespace: SweetpotatoMethod\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000002\n"
new_obo += "name: Scales\n"
new_obo += "namespace: SweetpotatoScale\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000003\n"
new_obo += "name: Variables\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000004\n"
new_obo += "name: Abiotic_stress_trait\n"
new_obo += "namespace: SweetpotatoTrait\n"
new_obo += "is_a: CO_331:0000000 ! CGIAR sweetpotato trait ontology\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000005\n"
new_obo += "name: Biotic_stress_trait\n"
new_obo += "namespace: SweetpotatoTrait\n"
new_obo += "is_a: CO_331:0000000 ! CGIAR sweetpotato trait ontology\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000007\n"
new_obo += "name: Quality_trait\n"
new_obo += "namespace: SweetpotatoTrait\n"
new_obo += "is_a: CO_331:0000000 ! CGIAR sweetpotato trait ontology\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000008\n"
new_obo += "name: Agronomic_trait\n"
new_obo += "namespace: SweetpotatoTrait\n"
new_obo += "is_a: CO_331:0000000 ! CGIAR sweetpotato trait ontology\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000009\n"
new_obo += "name: Biochemical_trait\n"
new_obo += "namespace: SweetpotatoTrait\n"
new_obo += "is_a: CO_331:0000000 ! CGIAR sweetpotato trait ontology\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000010\n"
new_obo += "name: Morphological_trait\n"
new_obo += "namespace: SweetpotatoTrait\n"
new_obo += "is_a: CO_331:0000000 ! CGIAR sweetpotato trait ontology\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000011\n"
new_obo += "name: Measurement\n"
new_obo += "namespace: SweetpotatoMethod\n"
new_obo += "is_a: CO_331:1000001 ! Methods\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000012\n"
new_obo += "name: Counting\n"
new_obo += "namespace: SweetpotatoMethod\n"
new_obo += "is_a: CO_331:1000001 ! Methods\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000013\n"
new_obo += "name: Computation\n"
new_obo += "namespace: SweetpotatoMethod\n"
new_obo += "is_a: CO_331:1000001 ! Methods\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000014\n"
new_obo += "name: Estimation\n"
new_obo += "namespace: SweetpotatoMethod\n"
new_obo += "is_a: CO_331:1000001 ! Methods\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000015\n"
new_obo += "name: Ordinal\n"
new_obo += "namespace: SweetpotatoScale\n"
new_obo += "is_a: CO_331:1000002 ! Scales\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000019\n"
new_obo += "name: Numerical\n"
new_obo += "namespace: SweetpotatoScale\n"
new_obo += "is_a: CO_331:1000002 ! Scales\n"
new_obo += "\n"
new_obo += "[Term]\n"
new_obo += "id: CO_331:1000030\n"
new_obo += "name: Nominal\n"
new_obo += "namespace: SweetpotatoScale\n"
new_obo += "is_a: CO_331:1000002 ! Scales\n"
new_obo += "\n"

new_obo += "[Typedef]\n"
new_obo += "id: method_of\n"
new_obo += "name: method_of\n"
new_obo += "\n"
new_obo += "[Typedef]\n"
new_obo += "id: scale_of\n"
new_obo += "name: scale_of\n"
new_obo += "\n"
new_obo += "[Typedef]\n"
new_obo += "id: variable_of\n"
new_obo += "name: variable_of\n"
#print('\n'.join(new_vars) ) 

#print(new_obo)


outputfile = args.output_path.strip()
file_obo = open(outputfile,"w", encoding="utf-8") 
file_obo.writelines(new_obo) 
file_obo.close()