import requests
import math
import subprocess

from rich.table import Column
from rich.progress import Progress, BarColumn, TimeElapsedColumn

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
        total_gist = len( gist_urls ) 
        with Progress(
            BarColumn(bar_width=None, complete_style='blue'), 
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(), 
            expand=True
        ) as progress:
            task = progress.add_task("[blue]Cloning...", total=total_gist)
            for count, repo in enumerate( gist_urls, start=1 ):
                progress.update(task, advance=1)
                subprocess.run(
                    args=['git', 'clone', repo[1]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                progress.print('[green]✓[/green] '+repo[0])
