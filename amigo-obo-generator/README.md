# amigo-obo-generator.py

usage: `python amigo-obo-generator.py [-h] crop_name input_path output_path`

Generate Amigo-friendly OBO file.

###### positional arguments:
- `crop_name`    Crop name for use in Amigo
- `input_path`   Input OBO Path
- `output_path`  Output OBO Path

###### optional arguments:
-  `-h`, `--help`   show this help message and exit

# td-generator.py

usage: `python amigo-obo-generator.py [-h] empty_template input_path output_path`

Generate Trait Dictionary from OBO file.

###### positional arguments:
- `crop_name`    Empty trait dictionary template (from CO website) Path
- `input_path`   Input OBO Path
- `output_path`  Output Excel Path

###### optional arguments:
-  `-h`, `--help`   show this help message and exit

# sp-obo-generator.py

usage: `python amigo-obo-generator.py [-h] current_obo input_path output_path`

Generate OBO file from current OBO file and new data stored in TD.

###### positional arguments:
- `crop_name`    Current obo file Path
- `input_path`   Input Excel Path
- `output_path`  Output OBO Path

###### optional arguments:
-  `-h`, `--help`   show this help message and exit
