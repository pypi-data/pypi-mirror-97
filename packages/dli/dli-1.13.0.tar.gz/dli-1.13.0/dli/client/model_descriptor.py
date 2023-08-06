#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#

class ModelDescriptor:
    """
    This class is responsible for extending the base type passed
    into the __init__ method with the instance of DliClient it has
    been created within, following the descriptor pattern.

    What this means practicably, is that under _client attribute of the 'new'
    type (class instance) there is a backreference to the DliClient,
    which then permits the type to access the shared session object of DliClient,
    rather than having to pass the session into each instance.

    Using an instance instantiated from the base type will not have the
    _client attribute available.
    """

    def __init__(self, model_cls=None):
        self.model_cls = model_cls

    def __get__(self, instance, owner):
        """Returns a model thats bound to the client instance"""
        return type(
            self.model_cls.__name__, (self.model_cls, ),
            {
                '_client': instance
            }
        )