import json
import os
import sys

from datalake_scripts.common.base_script import BaseScripts
from datalake_scripts.common.logger import logger
from datalake_scripts.engines.post_engine import BulkSearch


def main(override_args=None):
    """Method to start the script"""
    starter = BaseScripts()
    logger.debug(f'START: get_threats_from_query_hash.py')

    # Load initial args
    parser = starter.start('Retrieve a list of response from a given query hash.')
    parser.add_argument(
        '--query_fields',
        help='fields to be retrieved from the threat (default: only the hashkey)\n'
             'If an atom detail isn\'t present in a particular atom, empty string is returned.',
        nargs='+',
        default=['threat_hashkey'],
    )
    parser.add_argument(
        '--list',
        help='Turn the output in a list (require query_fields to be a single element)',
        action='store_true',
    )
    required_named = parser.add_argument_group('required arguments')
    required_named.add_argument(
        'query_hash',
        help='the query hash from which to retrieve the response hashkeys or a path to the query body json file',
    )
    if override_args:
        args = parser.parse_args(override_args)
    else:
        args = parser.parse_args()

    if len(args.query_fields) > 1 and args.list:
        parser.error("List output format is only available if a single element is queried (via query_fields)")

    query_body = {}
    query_hash = args.query_hash
    if len(query_hash) != 32 or os.path.exists(query_hash):
        try:
            with open(query_hash, 'r') as query_body_file:
                query_body = json.load(query_body_file)
        except FileNotFoundError:
            logger.error(f"Couldn't understand the given value as a query hash or path to query body: {query_hash}")
            exit(1)

    # Load api_endpoints and tokens
    endpoint_config, main_url, tokens = starter.load_config(args)
    logger.debug(f'Start to search for threat from the query hash:{query_hash}')

    bulk_search = BulkSearch(endpoint_config, args.env, tokens)
    if query_body:
        response = bulk_search.get_threats(query_body=query_body, query_fields=args.query_fields)
    else:
        response = bulk_search.get_threats(query_hash=query_hash, query_fields=args.query_fields)
    original_count = response.get('count', 0)
    logger.info(f'Number of threat that have been retrieved: {original_count}')

    formatted_output = format_output(response, args.list)
    if args.output:
        with open(args.output, 'w') as output:
            output.write(formatted_output)
    else:
        logger.info(formatted_output)

    if args.output:
        logger.info(f'Threats saved in {args.output}')
    else:
        logger.info('Done')


def format_output(response: dict, one_threat_per_line=False) -> str:
    if one_threat_per_line:
        threat_list = []
        for result in response.get('results', []):
            if result:
                threat_list += result
        return '\n'.join(threat_list)
    else:
        return json.dumps(response, sort_keys=True, indent=4)


if __name__ == '__main__':
    sys.exit(main())
