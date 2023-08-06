class MissingPackageError(Exception):
    def __init__(self, pkg):
        d = {'PDF': 'PDF results processing'}
        m = ('Missing required package for {0}. To use this functionality, ' +
             'please install the pdf2image>=1.12.1 package.').format(d.get(pkg))
        self.message = m

    def __str__(self):
        return self.message
