# FAME-Py
Python scripts for FAME models, generation of protobuf input files and conversion of protobuf output files.
Please visit the [FAME-Wiki](https://gitlab.com/fame2/fame-wiki/-/wikis/home) to get an explanation of FAME and its components.

# Installation

    pip install famepy

# Usage
FAME-Py currently offers two scripts "makeFameRunConfig" and "convertFameResults". 
Both are automatically installed with the package. 
The first one creates a protobuf file for FAME applications using YAML definition files and .csv files.
The latter one reads output files from FAME applications in protobuf format and converts them to .csv files.

## Make a FAME run configuration
Digests configuration files in YAML format, combines them with .csv files and creates a single input file for FAME applications in protobuf format.
Call structure:

    makeFameRunConfig <path/to/scenario.yaml>
    
You may also call the configuration builder from any Python script with

```python
from famepy.scripts.make_config import run as make_config

make_config("path/to/scenario.yaml")
```


### Scenario YAML
The "scenario.yaml" file contains all configuration options for a FAME-based simulation. 
It consists of the sections `RunConfig`, `GeneralProperties`, `Agents` and `Contracts`, all of them described below.

#### RunConfig
Specifies links to other input and output files. Structure:

```yaml
RunConfig:
  Schema: ./path/to/schema.yaml
  OutputFile: ./path/to/outputfile.pb
  LogFile: ./path/to/logfile.log
  ContractsPath: ./path/to/contract_folder/
```

Parameters:      
* `Schema` Path to Schema YAML file (see below). This file validates the inputs from this Scenario YAML.
* `OutputFile` Path to the output file to be created by makeFameRunConfig; the output file is in protobuf format (file ending ".pb")
* `LogFile` Path to log file - contains a log of the process 
* `ContractsPath`
  * Optional parameter
  * if present: "Contracts" section of all YAML files in that folder will be appended to the `Contracts` section in this file
  * files that begin with string "DISABLED_" will be ignored

#### GeneralProperties
Specifies FAME-specific properties of the simulation. Structure:

```yaml
GeneralProperties:
  runId: 1
  config:
    startTime: 2011-12-31_23:58:00
    stopTime: 2012-12-30_23:58:00
    randomSeed: 1
  outputParameters:
    outputInterval: 100
    outputProcess: 0
```

Parameters:
* `runId` an ID that can be given to the simulation; use at your discretion
* `startTime` time stamp in format YYYY-MM-DD_hh:mm:ss; first moment of the simulation.
* `stopTime` time stamp in format YYYY-MM-DD_hh:mm:ss; last moment of the simulation - i.e. simulation terminates after passing that time stamp
* `randomSeed` seed to initialise random number generation; each value leads to a unique series of random numbers.
* `outputInterval` number of simulation ticks in between write-to-disk events; may be used for performance optimisations; 
* `outputProcess` id of process that performs write-to-disk operations; leave at 0 to be compatible with single-processes;

#### Agents
Specifies all Agents to be created in the simulation in a list. Each Agent has its own entry. 
Structure:
```yaml
Agents:
  - Type: MyAgentWithInputs
    Id: 1
    Fields:
      MyEnumField: SAME_SHARES
      MyIntegerField: 2
      MyDoubleField: 4.2
      MyTimeSeriesField: "./path/to/time_series.csv"

  - Type: MyAgentWithoutInputs
    Id: 2
```


Agent Parameters:
* `Type` Mandatory; Java's simple class name of the agent to be created 
* `Id` Mandatory; simulation-unique id of this agent; if two agents have the same ID, the configuration process will stop. 
* `Fields` Optional; if the agent has any Input fields, specify them here in the format "FieldName: value"; please see input value table below

|FieldType  |value|
|-----------|-----|
|INTEGER |integer numeric value|
|DOUBLE|numeric value (integer or floating point)|
|ENUM|String(name of associated enum value)|
|TIME_SERIES|String representing path to .csv file|

The specified `Fields` for each agent must match the specified `Inputs` options in the linked Schema YAML (see below).

#### Contracts
Specifies all Contracts, i.e. repetitive bilateral transactions in between agents. Contracts are given as a list. 
The list may be sliced into several files: For your convenience, all files within the folder specified at `RunConfig: ContractsPath` are joined together.

```yaml
Contracts:
  - senderId: 1
    receiverId: 2 
    productName: ProductOfAgent_1
    firstDeliveryTime: -25
    deliveryIntervalInSteps: 3600

  - senderId: 2
    receiverId: 1
    productName: ProductOfAgent_2
    firstDeliveryTime: -22
    deliveryIntervalInSteps: 3600
```

Contract Parameters:
* `senderId` unique Id of agent sending the product
* `receiverId` unique Id of agent receiving the product
* `productName` name of the product to be sent
* `firstDeliveryTime` first time of delivery in format "seconds after the January 1st 2000, 00:00:00" 
* `deliveryIntervalInSteps` delay time in between deliveries in seconds

### Schema YAML
The "schema.yaml" file is used to validate the inputs of the "scenario.yaml". Currently, it specifies:
* which type of Agents can be created
* what type of input fields an Agent uses
* what type of Products an Agent can send in Contracts.

The "schema.yaml" consists of the sections `Header` and `AgentTypes`.

#### Header
The header specifies information about a FAME-based application for which input files are to be created. 
The idea here is to tie a schema.yaml to a specific version the application, ensuring a match between the inputs required by the application and those provided by the configs to be created. 

```yaml
Header:
  Project: MyProjectName
  RepoUrl: https://mygithosting.com/myProject
  CommitHash: abc123
```

* `Project` name of your project / FAME-based application
* `RepoUrl` URL of your project
* `CommitHash` hash of the commit / version of your project
 
#### AgentTypes
Here, each type of agent that can be created in your FAME-based application is listed, its input fields and its available Products for Contracts. 

```yaml
AgentTypes:
  <MyAgentWithInputs>:
    Inputs:
      <<MyInputFieldName>>:
        FieldType: enum
        Mandatory: true
        Values: [ 'AllowedValue1', 'AllowedValue2' ]
    Products: [ 'Product1' ]

  <MyAgentWithoutInputs>:
    Products: [ 'ProductA', 'ProductB' ]
```

* `<MyAgentName>` Java's simple class name of the Agent type; be sure to remove brackets <>
* `<<MyInputFieldName>>` Name of the input field as specified in the Java enum annotated with "@Input"; be sure to remove brackets <<>>
* `FieldType` data type of the input field; currently the types "INTEGER, DOUBLE, ENUM, TIME_SERIES" are supported
* `Mandatory` if true: the field is required for this agent
* `Values` optional parameter: if present defines a list of allowed values for this input field
* `Products` list of Products that this Agent can send in Contracts; derived from Java enum  annotated with "@Product"    
 
### CSV files
TIME_SERIES inputs are not directly fed into the Scenario YAML file.
Instead, TIME_SERIES reference a .csv file that can be stored some place else.
These .csv files follow a specific structure:
* They must contain exactly two columns.
* The first column must be a time stamp in form YYYY-MM-DD_hh:mm:ss
* The second column must be a numerical value (either integer or floating point)
* The separator of the two columns is a semicolon

Exemplary content of a valid .csv file:

    2012-01-01_00:00:00;400
    2013-01-01_00:00:00;720.5
    2014-01-01_00:00:00;650
    2015-01-01_00:00:00;99.27772
    2016-01-01_00:00:00;42
    2017-01-01_00:00:00;0.1

## Read FAME results
Takes an output file in protobuf format of FAME-based applications and converts it into files in .csv format.
An individual file for each type of Agent is created in a folder named after the protobuf input file.
Optionally, a list of Agent names can be added as second argument.
If present, only a subset of agents is extracted from the protobuf file. 
Call structure:

    convertFameResults ./path/to/protobuf_file.pb ['MyAgent1', 'MyAgent2']

You may also call the conversion script from any Python script with

```python
from famepy.scripts.convert_results import run as convert_results

convert_results("./path/to/protobuf_file.pb")
```

# Update protobuf definitions
In case updated versions of protobuf definitions from FAME-Protobuffer shall be used, simply update the files in folder protobuf_definitions: 
* Contract_pb2.py
* InputFile_pb2.py
* Services_pb2.py

Make sure to fix relative import of `Contract_pb2` in `InputFile_pb2.py`. This is a known but not closed issue from
Google protobuf compiler.

# Contribute
Please read the Contributors License Agreement (cla.txt), sign it and send it to fame@dlr.de before contributing. 
