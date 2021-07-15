"""
NOAA tokens which are repeatedly cycled during weather pull to guarantee that the maximum amount of station data can be retrieved before daily requests max out
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
def token_cycle(IN):
    if IN == 'ExHqFtwmXTLwOevojJsTbCcgZdlVYuRh':
        return ('yQkAvpPyYDTWyXhMjOqFYWGRBgoelDsO')

    if IN == 'yQkAvpPyYDTWyXhMjOqFYWGRBgoelDsO':
        return ('RQaGbLvtkfRCqekDyxfRPONeoZwUzbEU')
    else:
        return('ExHqFtwmXTLwOevojJsTbCcgZdlVYuRh')
