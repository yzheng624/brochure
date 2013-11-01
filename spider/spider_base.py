class SpiderError(Exception):
    '''raise SpiderError if error occurs in spider process.
    '''
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return 'SpiderError: {}'.format(self.error)


class BaseSpider(object):
    def __init__(self):
        self.error = None
        self.ua = r'Mozilla/5.0 (Ubuntu; Linux x86_64) TeapotParser'
        self.headers = {'User-Agent': self.ua}

    def run(self):
        return []
