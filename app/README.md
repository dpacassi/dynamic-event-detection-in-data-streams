# BA2019

## Cluster Evaluation

The cluster evaluation runs different clustering methods and stores the result in a maria db. The application is fully dockerized.

### Test Data

The test data can either be read from the database or csv. Make sure the 
data is available before running the evaluation.

### Setup

* Create an .env file in the `data_processing` directory based on the .env.example
* Start the required containers `docker-compose up -d mariadb`
* Run the evaluation `docker-compose run -d cluster_evaluation python cluster_evaluation_table.py --rows 1000 --runs 10`

### Debugging

It might be useful to enter the container for debbuging of the script. Use the following command to open container with a shell `docker-compose run cluster_evaluation /bin/bash`. The ipdb package is available for use.

### zhaw open stack

To run on the zhaw cluster upload the app first and then run as described above: 
`rsync -avz --exclude 'data_collection' --exclude 'neo4j' --exclude 'data_database/data'  --exclude 'data_database/test_data/wikiref' . ubuntu@160.85.252.135:~/app`

Export collected data with mysqldump:
`mysqldump -u username -p -h 0.0.0.0 --no-create-info --skip-triggers data_database > export.sql`