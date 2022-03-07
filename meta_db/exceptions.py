from __future__ import unicode_literals

###############################
# CUSTOM EXCEPTION FOR MODELS #
###############################


class PreventSaveException(Exception):
    pass


class PreventDeleteException(Exception):
    pass
