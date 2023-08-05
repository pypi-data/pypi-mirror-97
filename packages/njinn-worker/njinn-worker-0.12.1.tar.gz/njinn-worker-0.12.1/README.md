# Njinn Worker

## Installation

You can install the Njinn Worker from [PyPI](https://pypi.org/project/njinn_worker/):

    pip install njinn-worker

The worker is supported on Python 3.7 and above.

## Usage

Worker registration

    njinn-worker <registration_token>

If it's already registered you can run the worker by calling

    njinn-worker

## Docker

The Njinn Worker is also available from dockerhub as njinn/worker. You can also set the registration key via the environment variable `NJINN_WORKER_TOKEN` 
