#!/usr/bin/env python3

import re


def validate_base64(base64_string: bytes) -> bool:
        """
        Returns:
            True if the string is a valid base64 string
            and False if it is not
        """
        if (len(base64_string) % 4) != 0:
            return False
        elif re.match(r'^[a-zA-Z0-9+/=]*=?$', base64_string) == None:
            return False
        else:
            return True
        

if __name__ == '__main__':
     print(validate_base64('oo=='))
