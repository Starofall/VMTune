from logging import error

from rtxlib.dataproviders.LocalHookChangeProvider import LocalHookChangeProvider


def init_data_providers(wf):
    """ creates the required data providers """
    createInstance(wf, wf.primary_data_provider)
    if hasattr(wf, "secondary_data_providers"):
        for cp in wf.secondary_data_providers:
            createInstance(wf, cp)


def createInstance(wf, cp):
    """ creates a single instance of a data provider and stores the instance as reference in the definition """
    if cp["type"] == "local_hook":
        cp["instance"] = LocalHookChangeProvider(wf, cp)
    else:
        error("Not a valid data_provider")
