# excel2json
Convert Excel into JSON, using defined names.

## Install
### Linux or MacOS
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install excel2jsonfile
```
### Windows
Check stackoverflow to find out how to create a virtual environment on Windows.

## Run it
```python
from excelform2json.excel2json.excel2json import Excel2JSON
ref_excel2json = Excel2JSON(configuration_file="resources/config/excelform2json_config.json")
result = ref_excel2json.main(excel_file="input/excels/Test1.xlsx")
print("result:", result)
```
## Contribute

* Clone this repository
* run the following to get the referenced git repositories
    ```shell
    git submodule init
    git submodule update
    ```