# file datetimeparselib.pxd
#
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

cdef extern from "datetimeparselib.h":
    
    ctypedef struct rfctime_t:
        int year
        char month
        char day
        char hour
        char minute
        char second
        int microsecond
        int tzoffset 
    
    rfctime_t *from_string(char *string, char strict)

    char *to_string(rfctime_t dt, int localetz)

    char is_rfc3339ish(char *string, char strict)
    char is_rfc3339_format(char *string, char strict)

    int locale_tzoffset()