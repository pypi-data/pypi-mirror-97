from factory.base import Factory


class PynamoDBFactory(Factory):
    class Meta:
        abstract = True

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return model_class(*args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if not model_class.exists():
            model_class().create_table()

        instance = model_class(*args, **kwargs)
        instance.save()
        return instance
