AI-STAC Foundation Package
##########################

.. class:: no-web no-pdf

|pypi| |license| |wheel|


.. contents::

.. section-numbering::

What is Project Hadron
======================

Project Hadron is based on 'Augmented Intent - Single Task Adaptive Components' (AI-STAC) is a unique approach to
data recovery, discovery, synthesis and modeling that innovates the approach to data science and it's transition to
production. it's origins came from an incubator project that shadowed a team of Ph.D. data scientists in connection
with the development and delivery of machine learning initiatives to define measurable benefit propositions for
customer success. From this, a number of observable 'capabilities' were identified as unique and separate concerns.
The challenges of the data scientist, and in turn the production teams, were to effectively leveraging that separation
of concern and distribute and loosely couple the specialist capability needs to the appropriate skills set.

In addition the need to remove the opaque nature of the machine learning end-to-end required better transparency and
traceability, to better inform to the broadest of interested parties and be able to adapt without leaving being the
code 'sludge' of redundant ideas. Project Hadron is a disruptive innovation, changing the way we approach the
challenges of Machine Learning and Augmented Inelegance, introduces the ideas of 'Single Task Adaptive Component'
around the core concept of 'Parameterised Intent'

Main features
=============

* Machine Learning Capability Mapping
* Parametrised Intent
* Discovery Transitioning
* Feature Cataloguing
* Augmented Knowledge

Overview
========
Project Hadron is a change of approach in terms of improving productivity of the data
scientists. This approach deconstructs the machine learning discovery vertical into a set of capabilities, ideas and
knowledge.  It presents a completely novel approach to the traditional process automation and model wrapping that is
broadly offered as a solution to solve the considerable challenges that currently restrict the effectiveness of
machine learning in the enterprise business.

To achieve this, the project offers advanced and specialized programming methods that are unique in approach and novel
while maintaining familiarity within common tooling can be identified in four constructs.

1. Machine Learning Capability Mapping - Separation of capabilities, breaking the machine learning vertical into a set
of decoupled and targeted layers of discrete and refined actions that collectively present a human lead (ethical AI)
base truth to the next set of capabilities. This not only allows improved transparency of, what is, a messy and
sometimes confusing set of discovery orientated coded ideas but also loosely couples and targets activities that are,
generally, complex and specialized into identifiable and discrete capabilities that can be chained as separately
allocated activities.

2. Parametrized Intent - A unique technique extracting the ideas and thinking of the data scientist from their
discovery code and capturing it as intent with parameters that can be replayed against productionized code and data.
This decoupling and Separation of Concern between data, code and the intent of actions from that code on that data,
considerably improves time to market, code reuse, transparency of actions and the communication of ideas between data
scientists and product delivery specialists.

3. Discovery Transitioning - Discovery Transitioning - is a foundation of the sepatation of concerns between data
provisioning and feature selection. As part of the Accelerated ML discovery Vertical, Transitioning is a foundation
base truth facilitating a transparent transition of the raw canonical dataset to a fit-for-purpose canonical dataset
to enable the optimisation of discovery analysis and the identification of features-of-interest, for the data scientist
and created boundary separation of capabilities decoupling the Data Scientist for the Data Engineer. As output it also
provides 'intelligent Communication', not only to the Data Scientist through canonical fit-for-purpose datasets, but
more generally offers powerful visual discovery tools and artefact generation for production architects, data and
business SME's, Stakeholders and is the initiator of Augmented Knowledge for an enriched and transparent shared view of
the extended data knowledge.

4. Feature Cataloguing – With cross over skills within machine learning and advanced data heuristics,
investigation identified commonality and separation across customer engagements that particularly challenged our
Ph.D data scientists in their effective delivery of customer success. As a result the project designed and developed
Feature Cataloguing, a machine learning technique of extracting and engineering features and their characteristics
appropriately parameterized for model selection.  This technique implements a juxta view of how features are
characterized and presented to the modelling layer. Traditionally features are directly mapped as a representation
of the underlying data set. Feature Cataloguing treats each individual feature as its own individual set of
characteristics as its representation. The resulting outcome considerably improves experimentation, cross feature
association, even when unrelated in the original data sets, and the reuse of identified features-of-interest across
use case and business domains.

5. Augmented Knowledge - This the ability to capture information on data, activities and the rich stream of subject
matter expertise, injected into the machine learning discovery vertical to provide an Augmented n-view of the model
build. This includes security, sensitivity, data value scaling, dictionary, observations, performance, optimization,
bias, etc. This enriched view of data allows, amongst other things, improved knowledge share, AI explainability,
feature transparency, and accountability that feeds into AI ethics, and insight analysis.

Background
==========
Born out of the frustration of time constraints and the inability to show business value
within a business expectation, this project aims to provide a set of tools to quickly
produce visual and observational results. It also aims to improve the communication
outputs needed by ML delivery to talk to Pre-Sales, Stakholders, Business SME's, Data SME's
product coders and tooling engineers while still remaining within familiar code paragigms.

The package looks to build a set of outputs as part of standard data wrangling and ML exploration
that, by their nature, are familiar tools to the various reliant people and processes. For example
Data dictionaries for SME's, Visual representations for clients and stakeholders and configuration
contracts for architects, tool builders and data ingestion.

Installation
============

package install
---------------

The best way to install this package is directly from the Python Package Index repository using pip

.. code-block:: bash

    $ pip install aistac-foundation

if you want to upgrade your current version then using pip

.. code-block:: bash

    $ pip install --upgrade aistac-foundation

Package Overview
================

AbstractComponent
-----------------

The ``AbstractComponent`` class is a foundation class for the component build. It provides an encapsulated view of
the Property Management and Parameterised Intent

Abstract AI Single Task Application Component (AI-STAC) component class provides all the basic building blocks
of a components build including property management, augmented knowledge notes and parameterised intent pipeline.

For convenience there are two Factory Initialisation methods available ``from_env(...)`` and ``from_uri(...)`` the
second being an abstract method. This factory method initialises the concrete PropertyManager and IntentModel
classes and should use the parent ``_init_properties(...)`` methods to set the properties connector

As an example concrete implementation of this method:

.. code-block:: python

    def __init__(self, property_manager: ExamplePropertyManager, intent_model: ExampleIntentModel,
                 default_save=None, reset_templates: bool=None, align_connectors: bool=None):
        super().__init__(property_manager=property_manager, intent_model=intent_model, default_save=default_save,
                         reset_templates=reset_templates, align_connectors=align_connectors)

    @classmethod
    def from_uri(cls, task_name: str, uri_pm_path: str, pm_file_type: str=None, pm_module: str=None,
             pm_handler: str=None, pm_kwargs: dict=None, default_save=None, reset_templates: bool=None,
             align_connectors: bool=None, default_save_intent: bool=None, default_intent_level: bool=None,
             order_next_available: bool=None, default_replace_intent: bool=None):
        pm_file_type = pm_file_type if isinstance(pm_file_type, str) else 'pickle'
        pm_module = pm_module if isinstance(pm_module, str) else 'aistac.handlers.python_handlers'
        pm_handler = pm_handler if isinstance(pm_handler, str) else 'PythonPersistHandler'
        _pm = ExamplePropertyManager(task_name=task_name)
        _intent_model = ExampleIntentModel(property_manager=_pm, default_save_intent=default_save_intent,
                                          default_intent_level=default_intent_level,
                                          order_next_available=order_next_available,
                                          default_replace_intent=default_replace_intent)
        super()._init_properties(property_manager=_pm, uri_pm_path=uri_pm_path, pm_file_type=pm_file_type,
                                 pm_module=pm_module, pm_handler=pm_handler, pm_kwargs=pm_kwargs)
        return cls(property_manager=_pm, intent_model=_intent_model, default_save=default_save,
                   reset_templates=reset_templates, align_connectors=align_connectors)


To implement a new remote class Factory Method follow the method naming convention '_from_remote_<schema>()'
where <schema> is the uri schema name. this method should be a @classmethod and return a tuple of
module_name and handler.

For example if we were using an AWS S3 where the schema is s3:// the Factory method be similar to:

.. code-block:: python

    @classmethod
    def _from_remote_s3(cls) -> (str, str):
        _module_name = 'ds_discovery.handler.aws_s3_handlers'
        _handler = 'AwsS3PersistHandler'
        return _module_name, _handler


AbstractPropertyManager
-----------------------
The ``AbstractPropertiesManager`` facilitates the management of all the contract properties  including that of the
connector handlers, parameterised intent and Augmented Knowledge

Abstract AI Single Task Application Component (AI-STAC) class that creates a super class for all properties
managers

The Class initialisation is abstracted and is the only abstracted method. A concrete implementation of the
overloaded ``__init__`` manages the ``root_key`` and ``knowledge_key`` for this construct. The ``root_key`` adds a key
property reference to the root of the properties and can be referenced directly with ``<name>_key``. Likewise
the ``knowledge_key`` adds a catalog key to the restricted catalog keys.

More complex ``root_key`` constructs, where a grouping of keys might be desirable, passing a dictionary of name
value pairs as part of the list allows a root base to group related next level keys. For example

.. code-block:: python

    root_key = [{base: [primary, secondary}]

would add ``base.primary_key`` and ``base.secondary_key`` to the list of keys.

Here is a default example of an initialisation method:

.. code-block:: python

        def __init__(self, task_name: str):
            # set additional keys
            root_keys = []
            knowledge_keys = []
            super().__init__(task_name=task_name, root_keys=root_keys, knowledge_keys=knowledge_keys)


The property manager is not responsible for persisting the properties but provides the methods to load and persist
its in memory structure. To initialise the load and persist a ConnectorContract must be set up.

The following is a code snippet of setting a ConnectorContract and loading its content

.. code-block:: python

            self.set_property_connector(connector_contract=connector_contract)
            if self.get_connector_handler(self.CONNECTOR_PM_CONTRACT).exists():
                self.load_properties(replace=replace)

When using the property manager it will not automatically persist its properties and must be explicitely managed in
the component class. This removes the persist decision making away from the property manager. To persist the
properties use the method call ``persist_properties()``


AbstractIntentModel
-------------------
The ``AbstractIntentModel`` facilitates the Parameterised Intent, giving the base methods to record and replay intent.

Abstract AI Single Task Application Component (AI-STAC) Class for Parameterised Intent containing parameterised
intent registration methods ``_intent_builder(...)`` and ``_set_intend_signature(...)``.

it is creating a construct initialisation to allow for the control and definition of an ``intent_param_exclude``
list, ``default_save_intent`` boolean and a ``default_intent_level`` value.

As an example of an initialisation method

.. code-block:: python

    def __init__(self, property_manager: AbstractPropertyManager, default_save_intent: bool=None,
                 default_intent_level: bool=None, order_next_available: bool=None, default_replace_intent: bool=None):
        # set all the defaults
        default_save_intent = default_save_intent if isinstance(default_save_intent, bool) else True
        default_replace_intent = default_replace_intent if isinstance(default_replace_intent, bool) else True
        default_intent_level = default_intent_level if isinstance(default_intent_level, (str, int, float)) else 0
        default_intent_order = -1 if isinstance(order_next_available, bool) and order_next_available else 0
        intent_param_exclude = ['data', 'inplace']
        intent_type_additions = []
        super().__init__(property_manager=property_manager, default_save_intent=default_save_intent,
                         intent_param_exclude=intent_param_exclude, default_intent_level=default_intent_level,
                         default_intent_order=default_intent_order, default_replace_intent=default_replace_intent,
                         intent_type_additions=intent_type_additions)

in order to define the run pattern for the component task ``run_intent_pipeline(...)`` is an abstracted method
that defines the run pipeline of the intent.

As an example of a run_pipeline that iteratively updates a canonical with each intent

.. code-block:: python

    def run_intent_pipeline(self, canonical, intent_levels: [int, str, list]=None, **kwargs):
        # test if there is any intent to run
        if self._pm.has_intent():
            # get the list of levels to run
            if isinstance(intent_levels, (int, str, list)):
                intent_levels = Commons.list_formatter(intent_levels)
            else:
                intent_levels = sorted(self._pm.get_intent().keys())
            for level in intent_levels:
                level_key = self._pm.join(self._pm.KEY.intent_key, level)
                for order in sorted(self._pm.get(level_key, {})):
                    for method, params in self._pm.get(self._pm.join(level_key, order), {}).items():
                        if method in self.__dir__():
                            # add method kwargs to the params
                            if isinstance(kwargs, dict):
                                params.update(kwargs)
                            # add excluded parameters to the params
                            params.update({'inplace': False, 'save_intent': False})
                            canonical = eval(f"self.{method}(canonical, **{params})", globals(), locals())
        return canonical

    the code signature for an intent method would have the following construct

.. code-block:: python

    def <method>(self, <params>..., save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                 replace_intent: bool=None, remove_duplicates: bool=None):
        # resolve intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intend code block on the canonical
        ...


Reference
=========


Python version
--------------

Python 2.6 and 2.7 are not supported nor is Python 3.5. Although Python 3.6 is supported, it is recommended to install
``aistac-foundation`` against the latest Python 3.7> whenever possible.
Python 3 is the default for Homebrew installations starting with version 0.9.4.

GitHub Project
--------------
aistac-foundation: `<https://github.com/project-hadron/aistac-foundation>`_.

Change log
----------

See `CHANGELOG <https://github.com/project-hadron/aistac-foundation/blob/master/CHANGELOG.rst>`_.


Licence
-------

BSD-3-Clause: `LICENSE <https://github.com/project-hadron-cs/aistac-foundation/blob/master/LICENSE.txt>`_.


Authors
-------

`Gigas64`_  (`@gigas64`_) created aistac-foundation.


.. _pip: https://pip.pypa.io/en/stable/installing/
.. _Github API: http://developer.github.com/v3/issues/comments/#create-a-comment
.. _Gigas64: http://opengrass.io
.. _@gigas64: https://twitter.com/gigas64


.. |pypi| image:: https://img.shields.io/pypi/pyversions/Django.svg
    :alt: PyPI - Python Version

.. |rdt| image:: https://readthedocs.org/projects/aistac-foundation/badge/?version=latest
    :target: http://aistac-foundation.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |license| image:: https://img.shields.io/pypi/l/Django.svg
    :target: https://github.com/project-hadron/aistac-foundation/blob/master/LICENSE.txt
    :alt: PyPI - License

.. |wheel| image:: https://img.shields.io/pypi/wheel/Django.svg
    :alt: PyPI - Wheel

