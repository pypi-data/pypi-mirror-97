import requests
import math
import subprocess

from yaspin import yaspin

from gca.urls import USER_API_URL 

def fetch_responses( response ):
    ''' returns the name and url of user gists '''
    user = response.get( 'gists' )
    public_gists    = user.get( 'public_gists' )
    username        = user.get( 'name' )
    responses       = list()

    if public_gists:
        number_of_pages = math.ceil( public_gists / 100 )
        url_prefix      = USER_API_URL + username

        for counter in range( number_of_pages ):
            url = ''.join(
                [ url_prefix, '/gists?per_page=100&page={}'.format( counter + 1 ) ]
            )
            responses += requests.get( url ).json()
    return responses

def get_clone_urls( responses ):
    return [ 
        ( gist.get( 'id' ), gist.get( 'git_pull_url' ) ) for gist in responses.get( 'gca.gists' )
    ]

def dump_summary( filename = 'gists.md' ):
    pass

def execute_cloning( url_map ):
    gist_urls = url_map.get( 'gca.gists' )
    if gist_urls: 
        total_gist = len( url_map.get( 'gists' ) )
        print('cloning gists...')
        for count, gist in enumerate( gist_urls, start=1 ):
            with yaspin(text="({}/{}) cloning {}".format( count, total_gist, gist[ 0 ] ), color = 'blue' ) as spinner:
                subprocess.run(
                    args=[ 'git', 'clone', gist[ 1 ] ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )


