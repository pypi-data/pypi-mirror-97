# signalvine-sdk

Use the SignalVine API with Python

## Installation

    pip install git+https://github.com/CUBoulder-OIT/signalvine-sdk@main#egg=signalvine-sdk

## Building and Distribution

### Distribution Creation

    python setup.py sdist bdist_wheel

### Testing

To test, you'll have to configure account numbers, access token, and secrets

From the OS, set or export SignalVine variables for the tests:

    set ACCOUNT_NUMBER=1234-123-123-123-1234
    set ACCOUNT_TOKEN=12345567
    set ACCOUNT_SECRET=1234-123-123-123-1234
    set PROGRAM_ID=1234-123-123-123-1234

    pip install -e .
    python setup.py test

    # To test a single
    pytest tests\test_sdk.py -k "test_upsert_participants"

## Miscellania

All trademarks, service marks and company names are the property of their respective owners.

Reference in this site to any specific commercial product, process, or service, or the use of any trade, firm or corporation name is for the information and convenience of the public, and does not constitute endorsement, recommendation, or favoring by the University of Colorado.
