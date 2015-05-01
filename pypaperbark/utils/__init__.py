
class ZFSError(Exception):
    '''
    zfs error
    '''
    def __init__(self,err_str):
        self.__error_msg = err_str
    def __str__(self):
        return repr(self.__error_msg)

