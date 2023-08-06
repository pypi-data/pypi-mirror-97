import argparse
import importlib

from gca.utils import get_user_response, execute_funcs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--user',
        help = 'provide unique github user as arguement',
    )
    parser.add_argument(
        '-i',
        '--ignore-gist',
        help = 'ignore the gist, download only the repos',
    )

    args = parser.parse_args()
    user = args.user
    modlist    = [ 'gca.repositories', 'gca.gists' ] if not args.ignore_gist else [ 'gca.repositories' ]
    response   = get_user_response( username = user )
    result     = execute_funcs( modlist, 'fetch_responses', response = response )
    clone_urls = execute_funcs( modlist, 'get_clone_urls', responses = result )
    clone      = execute_funcs( modlist, 'execute_cloning', url_map = clone_urls )


if __name__ == "__main__":
    main()
