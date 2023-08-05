__version__ = '000.000.057'

__release_day__ = 3
__release_month_num__ = 3
__release_year__ = 2021

import datetime
__release_date_object__ = datetime.date(__release_year__, __release_month_num__, __release_day__)
del datetime
__release_date__ = __release_date_object__.__format__('%d %B %Y')
__release_month_name__ = __release_date_object__.__format__('%B')

__author__ = 'Calafiore Carmelo'
__author_email__ = 'c.calafiore@essex.ac.uk'
__maintainer_email__ = 'c.calafiore@essex.ac.uk'
__all__ = [
    'array', 'check', 'clock', 'combinations', 'directory', 'download',
    'format', 'image', 'maths', 'mixamo', 'nn', 'pkl', 'plot', 'preprocessing', 'shutdown', 'stats',
    'stimulation', 'strings', 'txt']


def initiate(names_submodules=None):
    template_import_string = "from . import "
    if isinstance(names_submodules, str):
        import_string_m = template_import_string + names_submodules
        exec(import_string_m)
    elif isinstance(names_submodules, (list, tuple)):
        for name_m in names_submodules:
            if isinstance(name_m, str):
                import_string_m = template_import_string + name_m
            else:
                import_string_m = template_import_string + str(name_m)
            exec(import_string_m)
    elif names_submodules is None:
        exec('from . import *')
        # for name_m in __all__:
        #     if isinstance(name_m, str):
        #         import_string_m = template_import_string + name_m
        #     else:
        #         import_string_m = template_import_string + str(name_m)
        #     exec(import_string_m)
    else:
        raise TypeError(names_submodules)
