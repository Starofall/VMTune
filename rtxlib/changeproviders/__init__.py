from rtxlib import error
from rtxlib.changeproviders.LocalHookChangeProvider import LocalHookChangeProvider

def init_change_provider(wf):
    """ loads the specified change provider into the workflow """
    cp = wf.change_provider
    if cp["type"] == "local_hook":
        cp["instance"] = LocalHookChangeProvider(wf, cp)
    else:
        error("Not a valid changeProvider")
        exit(1)

