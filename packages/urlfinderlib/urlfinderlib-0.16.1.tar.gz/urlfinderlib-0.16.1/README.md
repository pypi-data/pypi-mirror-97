# urlfinderlib
[![Build Status](https://travis-ci.com/ace-ecosystem/urlfinderlib.svg?branch=master)](https://travis-ci.com/ace-ecosystem/urlfinderlib)
[![codecov](https://codecov.io/gh/ace-ecosystem/urlfinderlib/branch/master/graph/badge.svg)](https://codecov.io/gh/ace-ecosystem/urlfinderlib)

This is a Python (3.6+) library for finding URLs in documents and checking their validity.

## Supported Documents

Extracts URLs from the following types of documents:

* Binary files (finds URLs within strings)
* CSV files
* HTML files
* iCalendar/vCalendar files
* PDF files
* Text files (ASCII or UTF-8)
* XML files

Every extracted URL is validated such that it contains a domain with a valid TLD (or a valid IP address) and does not contain any invalid characters.

## URL Permutations

This was originally written to accommodate finding both valid and obfuscated or slightly malformed URLs used by malicious actors and using them as indicators of compromise (IOCs). As such, the extracted URLs will also include the following permutations:

* URL with any Unicode characters in its domain
* URL with any Unicode characters converted to its IDNA equivalent

For both domain variations, the following permutations are also returned:

* URL with its path %-encoded
* URL with its path %-decoded
* URL with encoded HTML entities in its path
* URL with decoded HTML entities in its path
* URL with its path %-decoded and HTML entities decoded

## Child URLs

This library also attempts to extract or decode child URLs found in the paths of URLs. The following formats are supported:

* Barracuda protected URLs
* Base64-encoded URLs found within the URL's path
* Google redirect URLs
* Mandrill/Mailchimp redirect URLs
* Outlook Safe Links URLs
* Proofpoint protected URLs
* URLs found in the URL's path query parameters

## Basic usage

    from urlfinderlib import find_urls
    
    with open('/path/to/file', 'rb') as f:
        print(find_urls(f.read())

### base_url Parameter

If you are trying to find URLs inside of an HTML file, the paths in the URLs are often relative to their location on the server hosting the HTML. You can use the *base_url* parameter in this case to extract these "relative" URLs.

    from urlfinderlib import find_urls
    
    with open('/path/to/file', 'rb') as f:
        print(find_urls(f.read(), base_url='http://example.com')
