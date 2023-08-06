[![Build Status](https://travis-ci.com/librato/python-appoptics.svg?token=hJPGuB4cPyioy5R8LBV9&branch=ci)](https://travis-ci.com/librato/python-appoptics)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/appoptics_apm?style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/appoptics_apm?style=plastic)
![PyPI](https://img.shields.io/pypi/v/appoptics_apm?style=plastic)

# appoptics_apm

The 'appoptics_apm' module provides automatic instrumentation and metrics/tracing SDK hooks for use with [AppOptics](https://appoptics.com).

The appoptics_apm module provides middleware and other instrumentation for popular web frameworks such as Django, Tornado, Pyramid, and WSGI, as well as commonly used libraries like SQLAlchemy, httplib, redis, memcached.  Read more at [our full documentation](https://docs.appoptics.com/kb/apm_tracing/python/).


## Installing

The Python instrumentation for AppOptics uses a module named `appoptics_apm`, which is distributed via pypi.

```sh
pip install appoptics_apm
```

Alternately, you can use this repository to build a local copy.

## Configuring

See our documentation on [configuring the python instrumentation](https://docs.appoptics.com/kb/apm_tracing/python/configure/).

## Upgrading

To upgrade an existing installation, you simply need to run:

```sh
pip install --upgrade appoptics_apm
```

## Running the Tests

### Test Suite Organization

The test suite is organized into three main components, which are described in the following sections. All components
are configured to run in a docker environment, which is provided under `test/docker`. All test can be executed locally,
and the unit tests are configured to run automatically in Travis.

#### Unit Tests -- Verifies Python agent functionality

* These are actually functional tests; naming is for historic reasons.
* These are tests that exercise the actual c-lib extension.
* The C-extension is loaded, but certain C-library methods are modified to intercept the events which would otherwise be reported to the production collector
* All unit tests are configured to run automatically in Travis when a commit is pushed to the Github repo.

When running the unit tests locally, a pre-built agent distribution found under `dist` will be used. The agent version of the pre-built distribution is determined by the `APPOPTICS_APM_VERSION` environment variable and the tests will fail if no source distribution or compatible wheel can be found under `dist`. If the environment variable is unset, the version as specified by the source code currently checked out will be assumed.

##### Location of test files

* Python test scripts are located under `test/unit`
* Docker configuration and setup scripts are located under `test/docker/unit`
* Test logs will be located under `test/docker/unit/logs`
* Code coverage report will be located under `test/docker/unit/reports`

#### Install Tests -- Verifies correct installation of agent under a variety of operating systems
* These tests install the Python agent from the source distribution as well as from the Python wheel (if applicable).
* After successful installation, a minimal startup test will be performed to check that the agent installed from the source/ binary distribution starts up properly and can connect to the collector.
* On non-compatible operating systems (such as CentOs 6), a check will be performed that the agent goes into no-nop mode.

When running the install tests locally, a pre-built agent distribution found under `dist` will be used. The agent version of the pre-built distribution is determined by the `APPOPTICS_APM_VERSION` environment variable and the tests will fail no source distribution or compatible wheel can be found under `dist`. If the environment variable is unset, the version as specified by the source code currently checked out will be assumed.

##### Location of test files

* There are currently no Python test scripts needed for the install tests
* Docker configuration and setup scripts and test code is located under `test/docker/install`
* Test logs will be located under `test/docker/install/logs`

#### Manual Tests -- Manual verification of certain behavior
* These tests are currently not maintained.

### Running the tests locally via docker-compose

#### Prerequisites

* Install Docker and Docker Compose on your local machine.
* Build agent distribution under your local `dist/` directory using `make package`.
    * This will create a source distribution (tar.gz archive) as well as Python wheels under the `dist/` directory.
    * To speed up the process, you can only build the source distribution with `make sdist` when you only want to run the unit tests.

#### Run tests

To run unit tests locally, simply navigate to `test/docker/unit`. To execute the install tests, you need to navigate to `test/docker/install`.

In the respective directories you can now execute the following commands:
* To see the test matrix as defined by the Compose environment:
```
docker-compose config
```

* To run the entire test suite:
```
docker-compose up -d
```

* To run the entire test suite against a specific version of the Python agent:
```
APPOPTICS_APM_VERSION=1.2.3 docker-compose up -d
```
Note that the source and binary distribution of the version as specified in `APPOPTICS_APM_VERSION` must be available under `dist/` already, otherwise all tests will fail.

* Test logs are written to `test/docker/unit|install/logs`, and each composed service (i.e. test run) will exit 1 if there are test failures,  you can check via:
```
docker-compose ps
```

* To tear down the docker-compose environment, run:
```
docker-compose down --remove-orphans
```

#### Code Coverage Report for Unit and Extension Tests

To activate code coverage reports for the unit tests, you can simply set the following environment variable in your shell:
```
PYTHON_APPOPTICS_CODECOVERAGE=1
```

This will measure your code coverage with the `coverage` Python module and create html-reports in the `test/docker/unit/reports` directory for the unit tests. The reports will be stored under
```
<project_root>/test/docker/unit/reports/<service>/unit/index.html
````
and can simply be viewed with your browser.

For example, if the project is checked out under `~/source/python-appoptics`:

Run the desired service `<service>` with temporarily activated coverage measurement:
```
PYTHON_APPOPTICS_CODECOVERAGE=1 docker-compose up <service> -d
```

After the tests have been completed, you should find the coverage report for this service under
```
~/source/python-appoptics/test/docker/unit/reports/<service>
```

To view e.g. the unit test results, just open
```
~/source/python-appoptics/test/docker/unit/reports/<service>/unit/index.html
```
in your browser.

## Support

If you find a bug or would like to request an enhancement, feel free to file
an issue. For all other support requests, please email support@appoptics.com.

## Contributing

You are obviously a person of great sense and intelligence. We happily
appreciate all contributions to the appoptics_apm module whether it is documentation,
a bug fix, new instrumentation for a library or framework or anything else
we haven't thought of.

We welcome you to send us PRs. We also humbly request that any new
instrumentation submissions have corresponding tests that accompany
them. This way we don't break any of your additions when we (and others)
make changes after the fact.

### Activating Git hooks

This repo provides a folder hooks, in which all git hook related scripts can be found. Currently, there is only a pre-commit hook which runs Pylint on the changed \*.py files.

To set up the pre-commit hook, simply run the `install_hook.sh` script in this folder. This will install a project-specific virtual Python environment under which the code will be linted. Note that this requires Pyenv and Pyenv-virtualenv to be installed on your system.

Note:
Pyenv-virtualenv provides a functionality to automatically detect your project-specific virtual environment (e.g. when changing into the project folder in the terminal). To activate the auto-detection, you only need to make sure that you added `pyenv virtualenv-init` to your shell (refer to the installation section for [pyenv-virtualenv]( https://github.com/pyenv/pyenv-virtualenv) for more details).

### Pylint
To make sure that the code conforms the standards defined in the `.pylintrc` file, the pre-commit hook will not allow you to commit code if Pylint does issue any errors or warnings on the files you changed.

You can change this behaviour by setting certain environment variables when invoking `git commit`.

#### Ignore Pylint warning messages
You can commit your code even though Pylint issued warning messages by setting
```
PYTHON_APPOPTICS_PYLINT_IGNORE_WARNINGS=1
```
when invoking git commit.

#### Ignore Pylint error messages
You can commit your code even though Pylint issued error messages by setting
```
PYTHON_APPOPTICS_PYLINT_IGNORE_ERRORS=1
```
when invoking git commit. Please use this option with great care as Pylint error messages usually indicate genuine bugs in your code.

### Code Formatting with Yapf
For a more consistent formatting of the Python files, this repository comes with the code formatter Yapf pre-installed in the virtual environment. The configurations of Yapf are stored in the `.style.yapf` file in the root directory of this repository. Please consult the [Yapf documentation](https://github.com/google/yapf) for more information about the auto-formatter.

Currently, the formatting is not enforced through any commit hooks, but you can invoke Yapf with the provided configuration in your local development environment.

## Developer Resources

We have made a large effort to expose as much technical information
as possible to assist developers wishing to contribute to the AppOptics module.
Below are the three major sources for information and help for developers:

* The [AppOptics Knowledge Base](https://docs.appoptics.com/) has a large collection of technical articles or, if needed, you can submit a support request directly to the team.

If you have any questions or ideas, don't hesitate to contact us anytime.

To see the code related to the C++ extension, take a look in `appoptics_apm/swig`.

## License

Copyright (c) 2017 SolarWinds, LLC

Released under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
