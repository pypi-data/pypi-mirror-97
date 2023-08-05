Airflow Run
----------------

Python tool for deploying Airflow Multi-Node Cluster.

Requirements
------------

-  Python >=3.6 (tested)

Goal
----

| To provide a quick way to setup Airflow Multi-Node Cluster (a.k.a. Celery Executor Setup).

Steps
-----
1. Generate config yaml file.
2. Run commands to start webserver, scheduler, worker, (rabbitmq, postgres).
3. Add dag files and run initdb.

Generate config file:
---------------------

.. code:: python

    afr --generate_config

Running the tool in the same directory as config file:
------------------------------------------------------

.. code:: python

    afr --run postgresql
    afr --run initdb
    afr --run rabbitmq
    afr --run webserver
    afr --run scheduler
    afr --run worker --queue {queue name}
    afr --run flower

Or, running the tool specifying config path:
--------------------------------------------

.. code:: python

    afr --run postgresql --config /path/config.yaml

Or, use this environment variable to set the config path:
---------------------------------------------------------

.. code:: python

    export AIRFLOWRUN_CONFIG_PATH="/some_path/config.yaml"

After running webserver, scheduler and worker (postgres and rabbitmq if needed local instances), Add your dag files in the dags subdirectory in the directory you defined in the config file.

(* note: make sure you have the correct user permission in the dags, logs subdirectories.)

That is it!!


Default Config yaml file:
-------------------------

.. code-block:: yaml

    private_registry: False
    registry_url: registry.hub.docker.com
    username: ""
    password: ""
    repository: pkuong/airflow-run
    image: airflow-run
    tag: latest
    local_dir: {local directory where you want to mount /dags and /logs folder}
    webserver_port: 8000
    flower_port: 5555
    custom_mount_volumes: []
    env:
      AIRFLOW__CORE__EXECUTOR: CeleryExecutor
      AIRFLOW__CORE__LOAD_EXAMPLES: "False"
      AIRFLOW__CORE__DAGS_FOLDER: /usr/local/airflow/airflow/dags
      AIRFLOW__CORE__LOGS_FOLDER: /usr/local/airflow/airflow/logs
      AIRFLOW_HOME: /usr/local/airflow
      AIRFLOW__CORE__FERNET_KEY: ""
    rabbitmq:
      name: rabbitmq
      username: {username}
      password: {password}
      host: {IP}
      virtual_host: /
      image: rabbitmq:3-management
      home: /var/lib/rabbitmq
      ui_port: 15672
      port: 5672
      env:
        RABBITMQ_DEFAULT_USER: {username}
        RABBITMQ_DEFAULT_PASS: {password}
    postgresql:
      name: postgresql
      username: {username}
      password: {password}
      host: {host}
      image: postgres
      data: /var/lib/postgresql/data
      port: 5432
      env:
        PGDATA: /var/lib/postgresql/data/pgdata
        POSTGRES_USER: {username}
        POSTGRES_PASSWORD: {password}


Custom mount volumes
--------------------

| You can specify custom mount volumes in the container, for example:

.. code-block:: yaml

    custom_mount_volumes:
      - host_path: /Users/bob/.aws
        container_path: /usr/local/airflow/.aws


Docker image
------------

| This tool is using the following public docker image by default.

.. code:: python

    https://hub.docker.com/repository/docker/pkuong/airflow-run

Building the image:
-------------------

| If you want to build your own image, you can run the following:

.. code:: python

    afd --build --config_path={absolute path to config.yaml} --dockerfile_path={absolute path to directory which contains Dockerfile}

Contributors
------------

-  Paulo Kuong (`@pkuong`_)

.. _@pkuong: https://github.com/paulokuong

.. |Build Status| image:: https://travis-ci.org/paulokuong/airflow-run.svg?branch=master
.. target: https://travis-ci.org/paulokuong/airflow-run
