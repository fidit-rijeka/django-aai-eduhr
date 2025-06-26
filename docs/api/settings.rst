django_aai_eduhr.backends
=========================

AAIBackend
----------

Configurable values used by `django_aai_eduhr.backends.AAIBackend`.

.. py:data:: settings.AAI_MODEL

   String specifying the model which will hold AAI data in the format `<app>.<model>`.

.. py:data:: settings.AAI_MODEL_RELATED_NAME

   String specifying the related name by which the user model can access the `AAI_MODEL`.

.. py:data:: settings.AAI_BACKEND_AUTHORISATION

   Dictionary mapping AAI\@EduHr attributes to values needed for successful authorisation.

.. py:data:: settings.AAI_BACKEND_POLICY

   String specifying how to apply authorisation rules, can be either `all` or `any`.

   `all` : default
      User must meet all of the criteria (values) in `AAI_BACKEND_AUTHORISATION` to be authorised.
   `any`
      User must meet at least one criteria (value) in `AAI_BACKEND_AUTHORISATION` to be authorised.

AssertionReplayMitigationMixin
------------------------------
Configurable values used by `django_aai_eduhr.backends.AssertionReplayMitigationMixin`.

.. py:data:: settings.AAI_ASSERTION_CACHE

   String specifying the name of a cache which will be used to store assertion id by `AssertionReplayMitigationMixin`.
