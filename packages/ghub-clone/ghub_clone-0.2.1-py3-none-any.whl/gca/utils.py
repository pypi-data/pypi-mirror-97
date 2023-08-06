import requests
import importlib

from gca.urls import USER_API_URL 

def get_user_response( username ):
    ''' return user details '''
    try:
        response = requests.get( ''.join( [ USER_API_URL, '{}'.format( username ) ] ) )
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print( 'no such user exists' )
        sys.exit( err )
    
    json = response.json()
    return {
        'repositories': {
            'public_repos': json.get( 'public_repos' ),
            'type': json.get( 'type' ),
            'name': json.get( 'login' )
        },
        'gists': {
            'public_gists': json.get( 'public_gists' ),
            'name': json.get( 'name' )
        }
    } if response.status_code == 200 else None

def execute_funcs( modules, func_name, **kwargs ):
    result = dict()
    for module in modules:
        try:
            mod = importlib.import_module( module )
            func = getattr( mod, func_name )
            result[ module ] = func( **kwargs )
        except ImportError as error:
            print(error.__class__.__name__ + ": " + error.message)
    return result

