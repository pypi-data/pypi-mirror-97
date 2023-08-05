from django.db import models
from typing import List
from w.services.abstract_service import AbstractService
from w import exceptions


# noinspection PyCallingNonCallable
class AbstractModelService(AbstractService):
    _model: models.Model

    @classmethod
    def create(cls, **attrs):
        """
        Create model instance

        Args:
            **attrs: model attributes values

        Returns:
            models.Model
        """
        instance = cls._model(**attrs)
        instance.save()
        return instance

    @classmethod
    def get_by_pk(cls, pk):
        """
        Retrieve model by its primary key

        Returns:
            Model
        """
        return cls._model.objects.get(pk=pk)

    @classmethod
    def is_exists_by_pk(cls, pk) -> bool:
        """
        Check model existsby its primary key

        Returns
            bool
        """
        qs = cls._model.objects.filter(pk=pk)
        return qs.exists()

    @classmethod
    def check_by_pk(cls, pk):
        """
        Check model exists by its primary key

        if found return model else raise NotFoundError

        Raises
            NotFoundError
        """
        try:
            return cls._model.objects.get(pk=pk)
        except cls._model.DoesNotExist:
            label = cls._model._meta.verbose_name.title()  # noqa
            raise exceptions.NotFoundError(f"{label} not found (pk={pk})")

    @classmethod
    def list(cls, **filters) -> models.QuerySet:
        """
        List models filtered by filters (optional)

        Args:
            **filters: filter result

        Returns:
            QuerySet
        """
        if filters:
            return cls._model.objects.filter(**filters)
        return cls._model.objects.all()

    @classmethod
    def list_pks(cls, **filters) -> List:
        """
        List model pks filtered by filters (optional)

        Args:
            **filters:

        Returns:
            List
        """
        return cls.list(**filters).values_list("pk", flat=True)

    @classmethod
    def update(cls, instance, **attrs):
        """
        Update model instance

        Args:
            instance: model instance to update
            **attrs: model attributes values

        Returns:
            models.Model
        """
        for attr, value in attrs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, filters) -> int:
        """
        Delete

        Args:
            filters: model filters to delete

        Returns:
            nb deleted
        """
        nb, _ = cls._model.objects.filter(**filters).delete()
        return nb

    @classmethod
    def delete_by_pk(cls, pk) -> int:
        """
        Delete a model by is primary key

        Args:
            pk: model pk to delete

        Returns:
            nb deleted
        """
        return cls.delete({"pk": pk})
