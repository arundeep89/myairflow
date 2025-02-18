Instructions:
1. Create docker image: docker build --tag my-image:0.0.1 .
2. Add .env file with added with AIRFLOW_UID and AIRFLOW_IMAGE_NAME
3. Ensure postgresdb port is added to docker-compose.yml
4. Create container: docker compose up
5. Run my_dag.py
6. To check tables: 

        - access container: docker exec -it <containerid> psql -U <username> -d <dbname>

        - list tables: \dt

        - exit: \q
        
        - to view content: select * from customer;