# Testery CLI

To install you must have Python 3 and pip installed, then run:

`pip install --upgrade testery`

#### Create Test Run

Starts a test run.

```
testery create-test-run --token <yourTesteryApiToken> --project <projectKeyFromTestery> --build-id <uniqueBuildIdOfYourChoice> --environment <environmentToBeTested> --wait-for-results
```

When set, `--fail-on-failure`, will return an exit code of 1 if there are test failures.

*Output Formats*

- teamcity
- pretty
- json
- appveyor
- octopus

#### Create Test Environment

Creates an environment where tests may be run.

```
testery create-environment --token <yourTesteryApiToken> --key "<key>" --name "<name>" --variable "KEY1=FOO1" --variable "KEY2=FOO2" --variable "secure:KEY3=SECRET"
```

