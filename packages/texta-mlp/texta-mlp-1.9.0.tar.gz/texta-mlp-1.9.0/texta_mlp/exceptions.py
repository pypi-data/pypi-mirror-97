class LanguageNotSupported(Exception):
    """Raised when MLP fails to detect language or language is not supported.""" 
    pass

class BoundedListEmpty(Exception):
    """Raised when in Concatenator class the BOUNDS are not yet loaded, but concatenate() is tried""" 
    pass
