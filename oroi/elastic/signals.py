from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry

# Connect to db model signals in order to keep elasticsearch documents in sync

sender_app_label = "db"


@receiver(post_save)
def update_document(sender, **kwargs):
    """Update document on added/changed records.

    Update Declaration document index if foreign keys are removed from the database.
    """
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs["instance"]

    # Check the signal is coming from 'db' and not some other app
    if app_label is not sender_app_label:
        return

    # If person gets updated on the model then update the doc
    if model_name == "member":
        instances = instance.declaration_set.all()
        for _instance in instances:
            registry.update(_instance)

    # If council gets updated on the model then update the doc
    if model_name == "body":
        instances = instance.declaration_set.all()
        for _instance in instances:
            registry.update(_instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    """Update document on deleted records.

    Update Declaration document index if foreign keys are removed from the database.
    """
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs["instance"]

    # Check the signal is coming from 'db' and not some other app
    if app_label is not sender_app_label:
        return

    # If person gets updated on the model then update the doc
    if model_name == "member":
        instances = instance.declaration_set.all()
        for _instance in instances:
            registry.update(_instance)
            # registry.delete(_instance, raise_on_error=False)

    # If body gets updated on the model then update the doc
    if model_name == "body":
        instances = instance.declaration_set.all()
        for _instance in instances:
            registry.update(_instance)
            # registry.delete(_instance, raise_on_error=False)
