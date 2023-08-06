#!/usr/bin/env python3

""" Status codes for Gemini <gemini://gemini.circumlunar.space/docs/specification.gmi> """

codes = {"10": "Input request",
         "11": "Sensitive input request",
         "20": "Success",
         "30": "Temporary redirect",
         "31": "Permanent redirect",
         "40": "Temporary failure",
         "41": "Server unavailable",
         "42": "CGI error",
         "43": "Proxy error",
         "44": "Slow down",
         "50": "Permanent failure",
         "51": "Not found",
         "52": "Gone with the wind",
         "53": "Proxy request refused",
         "59": "Bad request",
         "60": "Client certificate request",
         "61": "Certificate not authorised",
         "62": "Certificate not valid"}

categories = {"1": "Input",
              "2": "Success",
              "3": "Redirect",
              "4": "Temporary failure",
              "5": "Permanent failure",
              "6": "Client certificate"}
