# distutils: sources=["clib/datetimeparselib.c"]

# file datetimeparse.pyx

# Copyright (c) 2021 Kevin Crouse
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @license: http://www.apache.org/licenses/LICENSE-2.0
# @author: Kevin Crouse (krcrouse@gmail.com)


cimport datetimeparselib
import datetime

def locale_tzoffset():
    ''' The offset for the timezone in the locale environment, in minutes.'''
    return(datetimeparselib.locale_tzoffset())

def is_rfc3339ish(char *string, strict=False):
    ''' The fastest check of whether a string is in RFC3339 format. This does not valid whether the date/time components are within valid ranges - just whether the string formatting of numbers vs separators is correct.
    
    Args:
        string (str): A character string to validate.
        strict (bool): Whether to be strict about formatting. If not strict, nonstandard separators can be used and a string that ends without timezone information is allowed as it is assumed to be UTC (or agnostic). Default is false.    
    Return:
        bool: Whether the string looks like an RFC3339 date-time.
     '''
    cdef char cstrict = 1 if strict else 0
    if datetimeparselib.is_rfc3339ish(string, cstrict):
        return(True)
    return(False)

def is_rfc3339(char *string, strict=False):
    ''' Is the string in RFC3339 format, including whether the numeric values are within acceptable ranges. This accounts for correct leap day accounting for centuries.
    
    Args:
        string (str): A character string to validate.
        strict (bool): Whether to be strict about formatting. If not strict, nonstandard separators can be used and a string that ends without timezone information is allowed as it is assumed to be UTC (or agnostic). Default is false.    
    Return:
        bool: Whether the string is a valid RFC3339 date-time.
    Note: This function calls parse_rfc3339, and so attempting to use it to pre-validate strings that may or may not be in rfc3339 format will not be efficient. From a performance standpoint, the only use for this is if you want to determine whether the string is an RFC3339 date but have no use for the actual date, as this will save the time to create the python datetime.datetime object.
     '''
    cdef char cstrict = 1 if strict else 0
    if datetimeparselib.is_rfc3339_format(string, cstrict):
        return(True)
    return(False)

def from_string(char *string, strict=False, ignore_leapseconds=True):
    ''' Parse an RFC3339 string and return a datetime object.
    
    Args:
        string (str): A character string to validate.
        strict (bool): Whether to be strict about formatting. If not strict, nonstandard separators can be used and a string that ends without timezone information is allowed as it is assumed to be UTC (or agnostic). Default is false.    
        ignore_leapseconds (bool): Whether to "functionally ignore" leap seconds. See the section on leap seconds in the package documentation. Because leap seconds are real and part of the RFC3339/ISO8601 specification, but not valid in Python datetime.datetime objects, they are handled by default to prevent random program crashes if one is encounted. 
             If ignore_leapseconds is True, a string in which the second is 60 will set second to 59 and microsecond to 999999 so that the datetime object can be constructed. 
             If False, any encounted leap second will raise an Exception in the datetime.datetime creation (unless Python addresses this limitation a future version). 
             Default is True to avoid program crashes.
    Return:
        datetime.datetime
    Raises:
        ValueError if the string is not in an RFC3339 format.
    '''
    cdef char cstrict = 1 if strict else 0
    cdef char leapignore = 1 if ignore_leapseconds else 0
    cdef datetimeparselib.rfctime_t* result = datetimeparselib.from_string(string, cstrict)
    if not result:
        invalid = string.decode('UTF-8')
        raise ValueError(f"string '{invalid}' is not formatted in an RFC3339 Format")
    if result.second == 60 and ignore_leapseconds:
        result.second = 59
        result.microsecond = 999999

    return(datetime.datetime(result.year, result.month, result.day, result.hour, result.minute, result.second, result.microsecond, datetime.timezone(datetime.timedelta(minutes=result.tzoffset))))


def to_string(dt, utcoffset=None):
    ''' Converts a datetime object into an ISO8601/RFC3339 string.
    
    Args:
        dt (datetime.datetime): The datetime object to translate.
        utcoffset (int|str, optional): If the datetime object is timezone-agnostic, an offset to correctly set the timezone. If an integer, this should be the number of minutes offset from UTC. An offset of 0 is UTC. If a string, it can be 'Z', '+hh:mi', or '-hh:mi'. If the datetime object is not timezone agnostic, the parameter is ignored. If utcoffset is not provided and the object is timezone agnostic, the localtime offset will be used."""
    Return:
        str: The RFC3339 datetime string for the datetime object.
    Notes:
        If the datetime object dt has a timezone specified, it is assumed that that is correct and utcoffset is ignored.
     '''

    
    timestruct = {
        'year': dt.year,
        'month': dt.month,
        'day': dt.day,
        'hour': dt.hour,
        'minute': dt.minute,
        'second': dt.second,
        'microsecond': dt.microsecond,        
    }
    if dt.tzinfo is None:
        timestruct['tzoffset'] = -86400
    else:
        timestruct['tzoffset'] = dt.tzinfo.total_seconds() // 60        

    if utcoffset is None:
        utcoffset = -86400
    elif type(utcoffset) is str:
        if len(utcoffset) == 6:
            offset = int(utcoffset[1:3]) * 60 + int(utcoffset[4:6])
        else:
            offset = int(utcoffset[1:2]) * 60 + int(utcoffset[3:5])
        if utcoffset[0] == '-':
            utcoffset = -offset
        else:
            utcoffset = offset        
    cdef char* result = datetimeparselib.to_string(timestruct, utcoffset)
    return(result.decode('UTF-8'))

