#!/usr/bin/env python3

import argparse
from pathlib import Path
import pyobo

parser = argparse.ArgumentParser(description='Generate Amigo-friendly OBO file.')
parser.add_argument('crop_name', type=str, help='Crop name for use in Amigo')
parser.add_argument('input_path', type=Path, help='Input OBO Path')
parser.add_argument('output_path', type=Path, help='Output OBO Path')
args = parser.parse_args()


### open RTB master obo file
with args.input_path.open() as myobo:
    o = pyobo(myobo)

### open the current amigo file - will only add what change?
    
##### save the amigo file
outputfile = args.output_path.open('w')

crop = args.crop_name.strip() + " "
#### remove auto-generated-by default-namespace and namespace-id-rule
del o.header["auto-generated-by"]
del o.header["default-namespace"]
del o.header["namespace-id-rule"]

outputfile.writelines(str(o.header))
outputfile.writelines("\n\n")


for term in o.getTerms():
    ### remove is-a
    for i in range(len(term["is_a"])):
        del term["is_a"][i-1]
        
    ## make variables as subclass of traits
    if "variable_of" in str(term["relationship"]):
        for i in range(len(term["relationship"])):
            trait = str(term["relationship"][i-1]).split(" ")[2] ##CO ID
            name = str(term["relationship"][i-1]).split("! ")[1]
            
            ## if trait a trait,add is_a
            if("namespace" in o[trait]):
                if("trait" in str(o[trait]["namespace"])):
                    term["is_a"].add(trait + "! " + name)               
        
    ### format name
    if("namespace" in term):
            if "trait" in str(term["namespace"]).lower():
                if "variable_of" in str(term["relationship"]):
                    ### don't add crop in the name if the name starts with the crop name
                    if(str(term["name"]).split("name: ")[1].lower().startswith(crop)):
                        term["name"] = str(term["name"]).lower().split("name: ")[1]+ " variable"
                    else:
                        term["name"] = crop + str(term["name"]).lower().split("name: ")[1]+ " variable"
                else:
                    ### don't add crop in the name if the name starts with the crop name
                    if(str(term["name"]).split("name: ")[1].lower().startswith(crop)):
                        term["name"] = str(term["name"]).lower().split("name: ")[1]+ " trait"
                    else:
                        term["name"] = crop + str(term["name"]).lower().split("name: ")[1]+ " trait"
            elif "method" in str(term["namespace"]).lower():
                term["name"] = crop + str(term["name"]).split("name: ")[1]+ " method"      
            elif "scale" in str(term["namespace"]).lower():
                term["name"] = crop + str(term["name"]).split("name: ")[1]+ " scale"
            
            del term["namespace"]
    #print(term)
    outputfile.writelines(str(term))
    outputfile.writelines("\n\n")


outputfile.close()
