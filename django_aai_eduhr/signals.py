import django.core.signals

#: Sent before AAI model is created or updated by the `AAIBackend`.
aai_pre_update = django.core.signals.Signal()

#: Sent after AAI model is created or updated by the `AAIBackend`.
aai_post_update = django.core.signals.Signal()
