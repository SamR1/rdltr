Installation
############

Prerequisites
~~~~~~~~~~~~~

- Python 3.6+
- SQLite
- yarn (for development only)
- Vue CLI (for development only)


Installation
~~~~~~~~~~~~

from PyPI
^^^^^^^^^

- install with pip

.. code-block:: bash

    $ pip install rdltr

- export the database location and secret key environment variables.

If needed, the default configuration can be overridden:

=========================== ======================================= ================================================================
variable                              description                   app default value
=========================== ======================================= ================================================================
`RDLTR_SETTINGS`            application configuration               "rdltr.config.ProductionConfig"
`RDLTR_DB_URL`              database location                       **no defaut value, must be initialized**
`RDLTR_SECRET_KEY`          application secret key                  **no defaut value, must be initialized**
`RDLTR_LOG`                 application log file                    no default value (log printed on the console)
`RDLTR_HOST`                host used by gunicorn                   localhost
`RDLTR_PORT`                port used by gunicorn                   5000
`RDLTR_WORKERS`             number of workers spawned by gunicorn   `calculated <http://docs.gunicorn.org/en/stable/custom.html>`__
`RDLTR_ALLOW_REGISTRATION`  is users registration allowed ?         true
=========================== ======================================= ================================================================

- initialize the database

.. code-block:: bash

    $ rdltr_db


- run the application

.. code-block:: bash

    $ rdltr


from source (for development)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Clone this repo:

.. code-block:: bash

    $ git clone https://github.com/SamR1/rdltr.git
    $ cd rdltr

- Update **Makefile.config** file if needed

- Install Python virtualenv,  and related packages and initialize the database:

.. code-block:: bash

    $ make install
    $ make upgrade-db

- Start the server:

    - to use with the front-end server: `make serve` and open http://localhost:8080/static
    - to only use build source: `make run` and open http://localhost:5000


Upgrade
~~~~~~~

.. warning::
    Before upgrading, make a backup of SQLITE database.

from PyPI
^^^^^^^^^

- upgrade with pip

.. code-block:: bash

    $ pip install -U rdltr

- if needed, upgrade database

.. code-block:: bash

    $ rdltr_db
