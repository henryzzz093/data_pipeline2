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
    <li><a href="#howto">HowTo</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- About The Project -->
## About The Project
![](images/Airflow.png)

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

<!-- Usage -->
## Usage
Data Pipeline Demostration

<!-- HowTo -->
## HowTo

### 1. How to verify the Airflow is running
```bash
docker ps
```
![](images/docker_ps.png)

### 2. How to verify the MySQL table is created
```bash
docker exec -it ms_container bash
```
and then connected to the MySQL inside the container by using the following:
- host = host.docker.internal
- port = 3307
- user = henry
- passcode = henry
- table name = stocks

![](images/inside_MySQL.png)
here we can see before tirggering the MySQL dag, the table is empty.
![](images/Empty_MySQL_table.png)

After triggering the dag:
![](images/stock_table_mysql.png)

## 3. How to verify the Postgres table is created
```bash
docker exec -it pg_container bash
```
and then connected to the MySQL inside the container by using the following:
- host = host.docker.internal
- port = 5438
- user = henry
- passcode = henry
- table name = stocks

![](images/inside_Postgres.png)

here we can see before tirggering the Postgres dag, the table is empty.
![](images/Postgres_empty_table.png)

After triggering the dag:
![](images/stock_table_Postgres.png)

<!--LICENSE -->
## License
Distributed under the MIT License.

<!--Contact-->
## Contact
- Henry Zou - heyunzou@magil.com
- Domonique Gordon - 
<p align = "right">(<a href = "#top">back to top</a>)</p>


