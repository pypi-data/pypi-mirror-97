"""Plugin to load the results of SQL queries into atoti stores.

This package is required to use :meth:`atoti.store.Store.load_sql` and :meth:`atoti.session.Session.read_sql`.

It can be installed with pip or conda:

  * .. code-block:: bash

      pip install atoti[sql]

  * .. code-block:: bash

      conda install atoti-sql

Supported SQL implementations are the ones available in :mod:`atoti_sql.drivers`.

"""
