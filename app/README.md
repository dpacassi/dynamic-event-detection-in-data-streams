# BA2019

## Cluster Evaluation

The cluster evaluation runs different clustering methods and stores the result in a maria db. The application is fully dockerized.

### Test Data

The test data can either be read from the database or csv. Make sure the 
data is available before running the evaluation.

### Setup

* Create an .env file in the `data_processing` directory based on the .env.example
* Start the required containers `docker-compose up mariadb phpmyadmin`
* Run the evaluation `docker-compose run cluster_evaluation python cluster_evaluation_table.py`

### Debugging

It might be useful to enter the container for debbuging of the script. Use the following command to open container with a shell `docker-compose run cluster_evaluation /bin/bash`. The ipdb package is available for use.