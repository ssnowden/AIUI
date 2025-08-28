ConversationThreads app
==========================================

* Main app Directory: chats
* App Description: This app manages the AI chats.
* App Initialised by: Simon Snowden (email: simon.snowden@googlemail.com)
* App Initialised on: 17/06/2025

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   project_apps.chats.tests

**App Modules**
---------------

*URLs*
-------------------------------

.. automodule:: project_apps.chats.urls

*Views*
--------------------------------

.. automodule:: project_apps.chats.views

.. autoclass:: project_apps.chats.views.ConversationThreadListView
   :show-inheritance:

.. autoclass:: project_apps.chats.views.ConversationThreadDetailView
   :show-inheritance:

.. autoclass:: project_apps.chats.views.ConversationThreadCreateView
   :show-inheritance:

.. autoclass:: project_apps.chats.views.ConversationThreadUpdateView
   :show-inheritance:

.. autoclass:: project_apps.chats.views.ConversationThreadDeleteView
   :show-inheritance:

*Models*
---------------------------------

.. automodule:: project_apps.chats.models

.. autoclass:: project_apps.chats.models.ConversationThread
   :show-inheritance:

.. autoclass:: project_apps.chats.models.ConversationItem
   :show-inheritance:

*Forms*
--------------------------------

.. automodule:: project_apps.chats.forms

.. autoclass:: project_apps.chats.forms.ConversationThreadForm
   :show-inheritance:


.. autoclass:: project_apps.chats.forms.ConversationItemForm
   :show-inheritance:


.. autoclass:: project_apps.chats.forms.ConversationItemFormSet
   :show-inheritance:


.. autoclass:: project_apps.chats.forms.ConversationItemCreateFormset
   :show-inheritance:


.. autoclass:: project_apps.chats.forms.ConversationItemUpdateFormset
   :show-inheritance:

*Admin site setup*
--------------------------------

.. automodule:: project_apps.chats.admin

.. autoclass:: project_apps.chats.admin.ConversationItemInLine
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: project_apps.chats.admin.ConversationThreadAdmin
   :members:
   :undoc-members:
   :show-inheritance:


*apps.py module*
-------------------------------

.. automodule:: project_apps.chats.apps

.. autoclass:: project_apps.chats.apps.ConversationThreadsConfig
   :members:
   :undoc-members:
   :show-inheritance:

