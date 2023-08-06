import requests
import math
import subprocess
from collections import namedtuple

from gca.urls import USER_API_URL, ORG_API_URL

from rich.table import Column
from rich.progress import Progress, BarColumn, TimeElapsedColumn

def fetch_responses( response ):
    ''' returns the name of the repo and url '''
    user = response.get( 'repositories' )
    number_of_public_repos = user.get( 'public_repos' )
    acctype      = user.get( 'type' )
    username     = user.get( 'name' )
    responses    = list()

    if number_of_public_repos > 0:
        number_of_pages = math.ceil( number_of_public_repos / 100 )

        url_prefix = USER_API_URL + \
            username if acctype == 'User' else ORGS_API_URL + username

        for counter in range( number_of_pages ):
            url = ''.join(
                [ url_prefix, '/repos?per_page=100&page={}'.format( counter + 1 ) ]
            )
            responses +=  requests.get( url ).json()
    return responses 

def get_clone_urls( responses ):
    return  [
        ( repo.get('name'), repo.get('clone_url') ) for repo in responses.get( 'gca.repositories' )
    ]

def dump_summary( filename = 'repositories.md' ):
    pass

def execute_cloning( url_map ):
    repo_urls = url_map.get( 'gca.repositories' )
    if repo_urls: 
        total_repos = len( repo_urls ) 
        with Progress(
            BarColumn(bar_width=None, complete_style='blue'), 
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(), 
            expand=True
        ) as progress:
            task = progress.add_task("[blue]Cloning...", total=total_repos)
            for count, repo in enumerate( repo_urls, start=1 ):
                progress.update(task, advance=1)
                subprocess.run(
                    args=['git', 'clone', repo[1]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                progress.print('[green]✓[/green] '+repo[0])