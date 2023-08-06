Description
============

Introduction
------------

Translucent provides a wrapper around the Python logging module, and is ment to
be a central place to gather all generic functionality related to logging.

Example
-------

The following is a sample `dictConfig` to configure translucent's JSON formatter.

.. code-block:: yaml

    version: 1
    handlers:
      console:
        class: logging.StreamHandler
        formatter: json
        level: INFO
        stream: ext://sys.stdout
    root:
      level: INFO
    handlers: [console]
      loggers:
        urllib3:
          level: INFO
    formatters:
      default:
        format: '%(asctime)s %(levelname)-8s %(name)-35s %(message)s'
        datefmt: '%Y-%m-%d %H:%M:%S'
      json:
        (): translucent.formatters.JSON
        namespace: ai
        name: logzio-prototype
    disable_existing_loggers: False
