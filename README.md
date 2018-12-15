# Hardware Usage Notifier

A service that lets the user set thresholds for hardware usage and get notified
when those thresholds are exceeded.

--- The rest of this file is dummy / work in progress ---

## Getting Started

These instructions will get you a copy of the project up and running on your local
machine for development and testing purposes. See deployment for notes on how to 
deploy the project on a live system.

### Prerequisites

* [Python 3.7](https://www.python.org/downloads/release/python-371/)

### Installing

#### Use only
1. Pull the package locally ([git](https://git-scm.com/) is required): 
    ```
    $ git clone git@github.com:ovidiupw/HardwareUsageNotifier.git
    ```
    
1. Go to your terminal and change the directory to the package root.

1. Make the scripts in the package available to be run:
    ```
    $ pip install virtualenv
    $ virtualenv venv
    $ . venv/bin/activate
    $ python setup.py install
    $ pip install --editable .
    ```
    
    ##### Troubleshooting:
    1. If you get permission errors, run with ```sudo``` on Linux or as ```Administrator``` on 
    Windows.
    1. On Windows, if ```. venv/bin/activate``` does not work, use ```virtualenv.exe activate```.
    1. If the ```pip install --editable .``` command does not work the first time, run it again.
    1. It is recommended to use ```bash``` on both Windows (e.g. Git Bash) and Linux. 
    
1. Afterwards the hardware usage notifier CLI should be available:
    ```
    $ hardware_usage_notifier --help
    Usage: hardware_usage_notifier [OPTIONS] COMMAND [ARGS]...
    [...]

    ```

## Running the tests

1. Go to the root of this package and run:
    ```
    pip install pytest
    pytest
    ```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
