from __future__ import  unicode_literals

class BQException(Exception):
    """
        BQException
    """

class BQApiError(BQException):
    """Exception in API usage"""



class BQCommError(BQException):

    def __init__(self, response):
        """
            @param: status - error code
            @param: headers - dictionary of response headers
            @param: content - body of the response (default: None)

        """
        #print 'Status: %s'%status
        #print 'Headers: %s'%headers
        self.response_url = response.url
        self.response_code = response.status_code
        self.response_headers = response.headers.copy()
        try:
            content = response.content
            if content is not None and len (content) > 64:
                content = "%s...%s" % (content[:64], content[-64:])
        except RuntimeError:
            # If content was consumed then just drop the whole thing (see requests/models.py)
            content =  "Content unavailable: previously consumed"
        self.content = content

    def __repr__(self):
        return "BQCommError(%s, status=%s, req headers=%s)%s" % (self.response_url,
                                                                 self.response_code,
                                                                 self.response_headers,
                                                                 self.content )
    def __str__(self):
        return self.__repr__()
