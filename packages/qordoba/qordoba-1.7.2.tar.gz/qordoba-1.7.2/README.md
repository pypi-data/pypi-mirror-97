# Q-CLI

[Build Status](http://jenkins)

[Documentation](https://dev.qordoba.com/docs/q-cli)


## Introduction
With the Q-CLI we at Qordoba provide our customers an easy to use command line tool to push and pull files to our platform.
The package can also be executed to localize existing projects.
During the execution of the Q-CLI, technical but understandable output will be printed to the console. i18n output files will be written to the users desktop directory 'Output_Qordoba'.

#### Use-Cases:
1. You are a Qordoba customer and want to transfer files via the command line tool between your local machine and the Qordoba platform
2. You want to be a Qordoba customer and need to localize your app. Executing the Q-CLI i18n commands will help you localize your app. After the localization process has finished, contact our Sales Department for further on-boarding. <hello@qordoba.com>


## Installation
It is built for Python >= 2.7 for Mac OS X and Linux.

### from source
1. Download
2. Unpack
3. cd into directory
4. pip intstall .

### from [python package index](https://pypi.python.org/pypi/qordoba)
1. pip install qordoba


## Execution
- init
- pull
- push
- delete
- status
- ls
- extract (branch StringExtractor)
- generate (branch StringExtractor)
- execute (branch StringExtractor)

##Extract
`qor i18n-extract -i input_dir -r report_dir -l customized_lexer`

The extract command pulls all the files from the given directory path and its subdirectories. 
Our lexer will parse your files and extract all the strings. The strings are saved in a generated JSON report.

report elements:
  * filename
  * string
  * start_line
  * end_line
  * code_snippet

!! The report can be edited (delete values, add) at this step. Not later.

##Generate
`qor i18n-generate -r report_dir -e report_key_dir`

The generate command will pick up your reports in the report_dir and generate new keys for every string by calling our API.
Keys are added to a new report which is stored in a new directory. The reason: while processing many reports there may occur connectivity issues. This way you know which reports have been processed.

Optional:
Flag `--existing_i18nfiles directory_path`. 
The generate command will look for JSON localization files in the directory_path and scan for existing keys or values.

report elements:
  * filename
  * string
  * start_line
  * end_line
  * code_snippet
  * generated_key
  * existing_key

##Execute
`qor i18n-execute -i input_dir -r report_key_dir -k key_format`

key format:
if keys should be replaced with a custom format, add it as a flag or within the configuration file.

The "KEY" characters will be replaced by the generated key within your report:

Option 1: 

add a custom key flag to execute the command: -k {{KEY}}

Option 2: 

add a custom key format in your configuration file ".i18n-ml.yml"

## Testing
 pytest

## Versioning
Q-CLI adheres to Semantic Versioning 2.0.0. If there is a violation of this scheme, report it as a bug. Specifically, if a patch or minor version is
released and breaks backward compatibility, that version should be immediately yanked and/or a new version should be immediately released that restores
compatibility. Any change that breaks the public API will only be introduced at a major-version release. As a result of this policy, you can (and should)
specify any dependency on Q-CLI by using the Pessimistic Version Constraint with two digits of precision.

## Licensing
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Qordobacode/i18next-plugin/blob/master/LICENSE.md) file for details
