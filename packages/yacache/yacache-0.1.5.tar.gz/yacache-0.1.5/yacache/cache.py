from copy       import deepcopy
import datetime as dt
import json
import wrapt    as wrapt

def cache( default=False, ttlSeconds=None ):
    '''
    Decorator caches function results on a contingent basis

    Args:
        default (bool): define default in case “doNotCache” is not a valid arg 
        ttlseconds (int): the number of seconds before the object expires

    Returns
        object
    '''
    _dict = {}
    @wrapt.decorator
    def _wrapper( foo, instance, args, kwargs ):
        key = _createDictKey( args, kwargs )
        if key in _dict and kwargs.get( "ttlSeconds", ttlSeconds ) is not None:
            if ( dt.datetime.utcnow() - _dict[ key ][ "insertTime" ] ).total_seconds() > kwargs.get( "ttlSeconds", ttlSeconds ):
                _dict.pop( key, None )
        if kwargs.get( "doNotCache", default ):
            _dict.pop( key, None )
        if key not in _dict:
            _dict[ key ] = {
                "result"     : foo( *args, **kwargs ),
                "insertTime" : dt.datetime.utcnow()
            }
        return deepcopy( _dict[ key ][ "result" ] )
    return _wrapper

def _createDictKey( args, kwargs ):
    '''
    Returns a valid dict key for a given set of args

    Args:
        args (tuple): args to parse into a valid dict key
        kwargs (dict): args to parse into a valid dict key

    Returns:
        tuple
    '''
    hashDict = deepcopy( kwargs ) if kwargs is not None else {}
    hashDict.update( { str( hash( frozenset( args ) ) ) : "" } )
    return hash( json.dumps( hashDict, sort_keys=True, default=str ) )