<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- About The Project -->
## About The Project

The goal for this project to demostrate the process of ETL by using Python and Docker containers. 


## Built With
Some major frameworks/libraries used to bootstrap this project:
* [apache-airflow](https://github.com/apache/airflow)
* [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
* [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
1. make sure your installed Docker Desktop on your computer. You can use the below link to download Docker from this link [download](https://www.docker.com/products/docker-desktop):

2. executing the Docker Desktop and make sure it runs in your background.

3. Make sure your Makefile has the latest version, you can check your current version by typing the following in terminal:
```bash
make --version
GNU Make 4.3
Copyright (C) 1988-2020 Free Software Foundation, Inc.
```
Or you can upgrade your makefile by using:
```bash
brew install make
```
and then add a "gnubin" directoryto your PATH from your bashrc like:
```bash
export PATH="/usr/local/opt/make/libexec/gnubin:$PATH"
```

### Installation
1. using the following commend to run the project:
```bash
make run-app
```
it would install every packages for you as well as creating a Apache Airflow UI to monitor the tasks

2. you can reset everything and wipe out the docker images from your computer by using:
```bash
make reset
```

## Usage
Data Pipeline Demostration
## Contributing

## License

## Contact

## Acknowledgments


