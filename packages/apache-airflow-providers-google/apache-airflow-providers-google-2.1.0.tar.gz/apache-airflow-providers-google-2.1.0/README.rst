
.. Licensed to the Apache Software Foundation (ASF) under one
   or more contributor license agreements.  See the NOTICE file
   distributed with this work for additional information
   regarding copyright ownership.  The ASF licenses this file
   to you under the Apache License, Version 2.0 (the
   "License"); you may not use this file except in compliance
   with the License.  You may obtain a copy of the License at

..   http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.


Package ``apache-airflow-providers-google``

Release: ``2.1.0``


Google services including:

  - `Google Ads <https://ads.google.com/>`__
  - `Google Cloud (GCP) <https://cloud.google.com/>`__
  - `Google Firebase <https://firebase.google.com/>`__
  - `Google Marketing Platform <https://marketingplatform.google.com/>`__
  - `Google Workspace <https://workspace.google.pl/>`__ (formerly Google Suite)


Provider package
================

This is a provider package for ``google`` provider. All classes for this provider package
are in ``airflow.providers.google`` python package.

You can find package information and changelog for the provider
in the `documentation <https://airflow.apache.org/docs/apache-airflow-providers-google/2.1.0/>`_.


Installation
============

NOTE!

On November 2020, new version of PIP (20.3) has been released with a new, 2020 resolver. This resolver
does not yet work with Apache Airflow and might lead to errors in installation - depends on your choice
of extras. In order to install Airflow you need to either downgrade pip to version 20.2.4
``pip install --upgrade pip==20.2.4`` or, in case you use Pip 20.3, you need to add option
``--use-deprecated legacy-resolver`` to your pip install command.

You can install this package on top of an existing airflow 2.* installation via
``pip install apache-airflow-providers-google``

PIP requirements
================

======================================  ===================
PIP package                             Version required
======================================  ===================
``PyOpenSSL``
``google-ads``                          ``>=4.0.0,<8.0.0``
``google-api-core``                     ``>=1.25.1,<2.0.0``
``google-api-python-client``            ``>=1.6.0,<2.0.0``
``google-auth-httplib2``                ``>=0.0.1``
``google-auth``                         ``>=1.0.0,<2.0.0``
``google-cloud-automl``                 ``>=2.1.0,<3.0.0``
``google-cloud-bigquery-datatransfer``  ``>=3.0.0,<4.0.0``
``google-cloud-bigtable``               ``>=1.0.0,<2.0.0``
``google-cloud-container``              ``>=0.1.1,<2.0.0``
``google-cloud-datacatalog``            ``>=3.0.0,<4.0.0``
``google-cloud-dataproc``               ``>=2.2.0,<3.0.0``
``google-cloud-dlp``                    ``>=0.11.0,<2.0.0``
``google-cloud-kms``                    ``>=2.0.0,<3.0.0``
``google-cloud-language``               ``>=1.1.1,<2.0.0``
``google-cloud-logging``                ``>=2.1.1,<3.0.0``
``google-cloud-memcache``               ``>=0.2.0``
``google-cloud-monitoring``             ``>=2.0.0,<3.0.0``
``google-cloud-os-login``               ``>=2.0.0,<3.0.0``
``google-cloud-pubsub``                 ``>=2.0.0,<3.0.0``
``google-cloud-redis``                  ``>=2.0.0,<3.0.0``
``google-cloud-secret-manager``         ``>=0.2.0,<2.0.0``
``google-cloud-spanner``                ``>=1.10.0,<2.0.0``
``google-cloud-speech``                 ``>=0.36.3,<2.0.0``
``google-cloud-storage``                ``>=1.30,<2.0.0``
``google-cloud-tasks``                  ``>=2.0.0,<3.0.0``
``google-cloud-texttospeech``           ``>=0.4.0,<2.0.0``
``google-cloud-translate``              ``>=1.5.0,<2.0.0``
``google-cloud-videointelligence``      ``>=1.7.0,<2.0.0``
``google-cloud-vision``                 ``>=0.35.2,<2.0.0``
``google-cloud-workflows``              ``>=0.1.0,<2.0.0``
``grpcio-gcp``                          ``>=0.2.2``
``json-merge-patch``                    ``~=0.2``
``pandas-gbq``
======================================  ===================

Cross provider package dependencies
===================================

Those are dependencies that might be needed in order to use all the features of the package.
You need to install the specified backport providers package in order to use them.

You can install such cross-provider dependencies when installing from PyPI. For example:

.. code-block:: bash

    pip install apache-airflow-providers-google[amazon]


========================================================================================================================  ====================
Dependent package                                                                                                         Extra
========================================================================================================================  ====================
`apache-airflow-providers-amazon <https://airflow.apache.org/docs/apache-airflow-providers-amazon>`_                      ``amazon``
`apache-airflow-providers-apache-beam <https://airflow.apache.org/docs/apache-airflow-providers-apache-beam>`_            ``apache.beam``
`apache-airflow-providers-apache-cassandra <https://airflow.apache.org/docs/apache-airflow-providers-apache-cassandra>`_  ``apache.cassandra``
`apache-airflow-providers-cncf-kubernetes <https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes>`_    ``cncf.kubernetes``
`apache-airflow-providers-facebook <https://airflow.apache.org/docs/apache-airflow-providers-facebook>`_                  ``facebook``
`apache-airflow-providers-microsoft-azure <https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure>`_    ``microsoft.azure``
`apache-airflow-providers-microsoft-mssql <https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql>`_    ``microsoft.mssql``
`apache-airflow-providers-mysql <https://airflow.apache.org/docs/apache-airflow-providers-mysql>`_                        ``mysql``
`apache-airflow-providers-oracle <https://airflow.apache.org/docs/apache-airflow-providers-oracle>`_                      ``oracle``
`apache-airflow-providers-postgres <https://airflow.apache.org/docs/apache-airflow-providers-postgres>`_                  ``postgres``
`apache-airflow-providers-presto <https://airflow.apache.org/docs/apache-airflow-providers-presto>`_                      ``presto``
`apache-airflow-providers-salesforce <https://airflow.apache.org/docs/apache-airflow-providers-salesforce>`_              ``salesforce``
`apache-airflow-providers-sftp <https://airflow.apache.org/docs/apache-airflow-providers-sftp>`_                          ``sftp``
`apache-airflow-providers-ssh <https://airflow.apache.org/docs/apache-airflow-providers-ssh>`_                            ``ssh``
========================================================================================================================  ====================