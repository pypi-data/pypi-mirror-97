/** file datetimeparselib.c

Copyright (c) 2021 Kevin Crouse

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@license: http://www.apache.org/licenses/LICENSE-2.0
@author: Kevin Crouse (krcrouse@gmail.com)
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include "datetimeparselib.h"

#define UNDEFINED -100000
#define true 1
#define false 0


const int powtt[] = {
    1, 10, 100, 1000, 10000,100000,1000000
};

inline int isnum(char c){
    /* True if the character is a numeral */
    return(c >= '0' && c <= '9');
}

inline int isalphanum(char c){
    /* True if the character is a numeral or a letter */
    return( (c >= '0' && c <= '9') 
        || (c >= 'a' && c <= 'z')
        || (c >= 'A' && c <= 'Z')
    );
}

inline int intseg(char *string, char offset, char n){
    /* translates {n} characters of {string} starting at {offset} to an integer. If any character is not a numeral, return -2^15  */
    int result = 0;
    for(int i=0; i < n; ++i){
        if(!isnum(string[offset+i]))
            return(UNDEFINED);
        result += (string[offset + i] - '0') * powtt[n - i -1];
    }
    return(result);
}

int tzoffset = UNDEFINED;
inline int _locale_tzoffset(){
    /* fetch the timezone offset (in minutes) for the current local environment and save it in a [global]variable so it is readily accessible in future uses. This is because many uses of isotimestamp may never look up the tzoffset for the local environment, but when they do, there a high likelyhood that it's going to be looked quite a lot, and we don't want to be hitting time() and localtime_r() for each call.*/
    
    if(tzoffset == UNDEFINED){
        // no tzoffset, use the locale of the current environment
        time_t t = time(NULL); // time() is in utc            
        struct tm lt = {0};
        localtime_r(&t, &lt); //localtime
        tzoffset = (int)lt.tm_gmtoff / 60;
    }
    return(tzoffset);
}

int locale_tzoffset(){
    /* Provide a public interface for locale_tzoffset.*/
    return(_locale_tzoffset());
}

char is_rfc3339ish(char *string, char strict){
    /* ensures the format of {string} is essentially in iso8601/rfc3339 format, but doesn't validate numbers within valid date/time component ranges. 
        When {strict} is a true value, requires the non-numeric characters to be exactly one of the valid characters specified in RFC3339. If {strict} is false, allows the non-numeric characters to be any non-numeric value.
    */
 
    int ln = strlen(string);
    if(ln < 19)
        // cannot possibly be a formal rfc string
        return(false);
    if(strict){
        // do additional pattern matching to ensure the non-numeric characters are expected
        if(ln == 19)
            return(false);        
        if(string[4] != '-' || string[7] != '-')
            return(false);
        if(string[10] != 't' && string[10] != 'T' && string[10] != ' ')
            return(false);
        if(string[13] != ':' || string[16] != ':')
            return(false);
    }
    else{
        if(isalphanum(string[4]) || isalphanum(string[7])) // date separators. Should be '-'
            return(false);
        if(isnum(string[10])) // time offset. Should be 'T'
            return(false);
        if(isnum(string[13]) || isnum(string[16])) // time separators - should be ':'
            return(false);
    }
    // now we get to the point differentiation
    if(ln == 19){ // no time zone information is permissble if not strict
        return(!strict);
    }
    if(ln == 20)
        return(string[19] == 'z' || string[19] == 'Z');
    
    int i = 19;
    if(string[19] == '.' || string[19] == ','){
        // microsecond
        if(!isnum(string[20])) // a period but no actual decimal locations
            return(false);                    
        i += 2;        
        while(i < ln && isnum(string[i]))
            ++i;
        if(i > 26)
            return(false); // two many microsecond decimal locations        
    } // term condition: i == ln or string[i] is not a number
    
    if(ln == i){
        return(!strict);  // no time zone information is permissble if not strict
    }
        
    if(string[i] != '+' && string[i] != '-'){
        if(i+1 == ln && (string[i] == 'z' || string[i] == 'Z'))
            return(true);
        return(false);
    }
    if(!isnum(string[++i]))
        return(false);
    if(ln == i+1) // single digit timzeone, e.g. 2021-12-25T14:38:57-5
        return(!strict);

    if(!isnum(string[++i])){
        // this is allowed in non-strict mode for a single-digit timezone offset - but then the string must have exactly 3 characters remaining.  i.e. the time zone must look like +5:00 or -2.15
        if(strict)
            return(false);
        if(ln != i+3 || !isnum(string[i+1]) || !isnum(string[i+2]))
            return(false);
        return(true);        
    }
    if(ln == i+1)
        return(true); // time zone offset is hour only, e.g. +05 or -13
    
    if(!isnum(string[++i])){ // minute separator
        if(ln != i+3 || !isnum(string[i+1]) || !isnum(string[i+2]))
            return(false);
        return(true);
    }
    // string[i] is a the third number in sequence, so valid formats could be 3 or 4 digit timezones, so +515, -600, +1200, -0500.
    if(ln == i+1){
        return(!strict);
    }
    else if(ln == i+2 && isnum(string[i+1]))
        return(true);
    return(false);
}

char is_rfc3339_format(char *string, char strict){
    /* Determines whether {string} is a valid RFC3339 string, including numeric range consideration. If {strict}, applies strict checking of the non-numeric separator characters.  
    
    Notes:
        1. This calls from_string to get the values to check, and so it is actually slower than merely parsing out the values. It, however, provides a succinct truth value when the programmer is not interested in actually handling the data - and for the broader python project doesn't require translation into a datetime object.
        2. Some values are considered valid rfc3339 formats but will not parse into valid Python datetime objects, i.e. second may be 60 to account for leap seconds, but because leap seconds are not predictable or algorithmically determinable, is_rfc_3339 does not validate it. 
    */
    rfctime_t *result = from_string(string, strict);
    if(!result)
        return(false);

    if(result->month > 12)
        return(false);
    
    if(result->month == 4 || result->month == 6 || result->month == 9 || result->month == 11){
        if(result->day > 30)
            return(false);        
    }
    else if(result->month == 2){
        // february
        if(result-> month > 29)
            return(false);
        else if(result->month == 29){        
            if((result->year % 4) != 0)
                return(false); // normal non-leap year
            // now check the century
            if((result->year % 100) == 0){
                // it's a century - this is bad unless it's 2000
                if((result->year % 400) != 0)
                    return(false);
            }
        }
    }
    else{
        if(result->day > 31)
            return(false);
    }
    if(result->hour > 23 || result->minute > 59 || result->second > 60)
        return(false);

    if(result->tzoffset < -1440 || result->tzoffset > 1440)
        return(false);
    return(true);
}

rfctime_t* from_string(char *string, char strict){
    /* Parses {string} and returns the rfctime_t struct for its value. from_string does not actually verify that the integer values are valid ranges; if they are not, it will lead to an error in the creation of the Python object downstream. First calls is_rfc3339ish with the {strict} parameter to determine whether the string is formatted sufficiently to be processed. 
    
    Returns 0 if the string is not in sufficent RFC3339 format.
    */
    if(!is_rfc3339ish(string, strict))
        return(false);

    int ln = strlen(string);
    rfctime_t *result = malloc(sizeof(rfctime_t));  

    result->year = intseg(string, 0, 4);
    result->month = intseg(string, 5, 2);
    result->day = intseg(string, 8, 2);
    result->hour = intseg(string, 11,2);
    result->minute = intseg(string, 14,2);
    result->second = intseg(string, 17,2);
    
    int i = 19;
    if(string[i] == '.' || string[i] == ','){
        // microseconds - there may be 0-5 digits here
        char lsec = 0;
        while(isnum(string[i+1+lsec])){
            ++lsec; 
        }
        // translate and convert fractional seconds into microsecond 
        result->microsecond = intseg(string, i+1, lsec) * powtt[6-lsec];
        i += lsec + 1;
    }
    else {
        result->microsecond = 0;
    }
    if(ln == i || string[i] == 'z' || string[i] == 'Z'){
        //utc time
        result->tzoffset = 0;
    }
    else{
        //timezone offset
        int tzhour;        
        int tzmin = 0;
        char tzsign = string[i++];
        switch(ln-i){ // by looking at the string length we can determine the format.
            case 1: // single digit hour, only in non-strict: '2001-10-15T00:05:23.283+5'
                if(strict)
                    return(0);
                tzhour = string[i] - '0';
                break;
            case 2: // 2 digit hour, no minute:'2001-10-15T00:05:23.283+5'
                tzhour = intseg(string, i, 2);
                break;
            case 3: // single digit hour, 2 digit minute:'2001-10-15T00:05:23.283+500'
                if(strict)
                    return(0);
                tzhour = string[i] - '0';
                tzmin = intseg(string, i+1, 2);
                break;
            case 4: // could be single digit hour, 2 digit minute, or 2-2 without a separator, '2001-10-15T00:05:23.283+5:00' or '2001-10-15T00:05:23.283+0500'
                if(isnum(string[i+1])){
                    tzhour = intseg(string, i, 2);
                    tzmin = intseg(string, i+2, 2);
                }
                else if (!strict){
                    tzhour = string[i] - '0';
                    tzmin = intseg(string, i+2, 2);
                }
                else return(0);
                break;
            case 5:
                tzhour = intseg(string, i, 2);
                tzmin = intseg(string, i+3, 2);
                break;
            default:
                return(0);
        }
        if(tzsign == '-'){
            result->tzoffset = -(tzhour*60 + tzmin);
        }
        else{
            result->tzoffset = tzhour*60 + tzmin;
        }
    }
    return(result);
}


char* to_string(rfctime_t dt, int locale_offset){
    /* Translates an rfctime_t struct into an RFC3339 string. 
    
    locale_offset represents the *default* UTC offset (in minutes) for time-agnostic dates. If the dt object has a tzoffset et, it will use that as the offset instead of locale_offset. 
    
    If dt.tzoffset is UNDEFINED, it will use locale_offset as the UTC offset. However, if locale_offset is also UNDEFINED, the current UTC offset for the locale will be used (see locale_tz() ).
    */

    char *result = malloc(sizeof(char)*30);
    sprintf(result, "%04d-%02d-%02dT%02d:%02d:%02d",dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second);
    
    int i=19;
    if(dt.microsecond){
        sprintf(result+i, ".%03d", dt.microsecond / 1000);
        i += 4;
    }
    
    // Now handle timezones
    //printf("TZ: %d\nLTZ: %d\n", dt.tzoffset, locale_offset);

    if(!dt.tzoffset){ 
        // utc time
        result[i] = 'Z';        
    }
    else if(dt.tzoffset == UNDEFINED){
        // timezone agnostic, so set it appropriately.
    
        if(locale_offset != UNDEFINED){
            // use the offset provided as the function parameter
            if(!locale_offset){
                result[i] = 'Z';
                result[i+1] = '\0';                
            }
            else if(locale_offset > 0){
                sprintf(result+i, "+%02d:%02d", 
                    locale_offset / 60,
                    (locale_offset % 60)
                );
            }
            else{
                sprintf(result+i, "-%02d:%02d", 
                    -locale_offset / 60,
                    (-locale_offset % 60)
                );
            }     
        }
        else{
            // use the offset from the system time.
            int tzoffset = _locale_tzoffset();
            if(!tzoffset){
                // gmt
                result[i] = 'Z';
                result[i+1] = '\0';                                
            }
            else if(tzoffset > 0){
                sprintf(result+i, "+%02d:%02d", 
                    tzoffset / 3600,
                    (tzoffset % 3600) / 60
                );
            }
            else{
                sprintf(result+i, "-%02d:%02d", 
                    -tzoffset / 3600,
                    (-tzoffset % 3600) / 60
                );
            }            
        }
    }
    else if (dt.tzoffset < 0){
        int hr = -dt.tzoffset/60;
        int min = -(dt.tzoffset - hr*60);
        sprintf(result+i, "-%02d:%02d", hr, min); 
    }
    else{
        int hr = dt.tzoffset/60;
        int min = dt.tzoffset - hr*60;
        sprintf(result+i, "+%02d:%02d", hr, min); 
    }
    return(result);
}