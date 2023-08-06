import re
import sys

from collections import OrderedDict

from datalake_scripts.common.base_script import BaseScripts
from datalake_scripts.common.logger import logger
from datalake_scripts.engines.post_engine import ThreatsPost, BulkThreatsPost


def main(override_args=None):
    """Method to start the script"""
    starter = BaseScripts()

    # Load initial args
    parser = starter.start('Submit a new threat to Datalake from a file')
    required_named = parser.add_argument_group('required arguments')
    csv_controle = parser.add_argument_group('CSV control arguments')
    required_named.add_argument(
        '-i',
        '--input',
        help='read threats to add from FILE',
        required=True,
    )
    required_named.add_argument(
        '-a',
        '--atom_type',
        help='set it to define the atom type',
        required=True,
    )
    csv_controle.add_argument(
        '--is_csv',
        help='set if the file input is a CSV',
        action='store_true',
    )
    csv_controle.add_argument(
        '-d',
        '--delimiter',
        help='set the delimiter of the CSV file',
        default=',',
    )
    csv_controle.add_argument(
        '-c',
        '--column',
        help='select column of the CSV file, starting at 1',
        type=int,
        default=1,
    )
    parser.add_argument(
        '-p',
        '--public',
        help='set the visibility to public',
        action='store_true',
    )
    parser.add_argument(
        '-w',
        '--whitelist',
        help='set it to define the added threats as whitelist',
        action='store_true',
    )
    parser.add_argument(
        '-t',
        '--threat_types',
        nargs='+',
        help='choose specific threat types and their score, like: ddos 50 scam 15',
        default=[],
    )
    parser.add_argument(
        '--tag',
        nargs='+',
        help='add a list of tags',
        default=[],
    )
    parser.add_argument(
        '--link',
        help='add link as external_analysis_link',
        nargs='+',
    )
    parser.add_argument(
        '--permanent',
        help='sets override_type to permanent. Scores won\'t be updated by the algorithm. Default is temporary',
        action='store_true',
    )
    parser.add_argument(
        '--no-bulk',
        help='force an api call for each threats, useful to retrieve the details of threats created',
        action='store_true',
    )
    if override_args:
        args = parser.parse_args(override_args)
    else:
        args = parser.parse_args()
    logger.debug(f'START: add_new_threats.py')

    if not args.threat_types and not args.whitelist:
        parser.error("threat types is required if the atom is not for whitelisting")

    permanent = 'permanent' if args.permanent else 'temporary'

    if args.is_csv:
        try:
            list_new_threats = starter._load_csv(args.input, args.delimiter, args.column - 1)
        except ValueError as ve:
            logger.error(ve)
            exit()
    else:
        list_new_threats = starter._load_list(args.input)
    list_new_threats = defang_threats(list_new_threats, args.atom_type)
    list_new_threats = list(OrderedDict.fromkeys(list_new_threats))  # removing duplicates while preserving order
    threat_types = ThreatsPost.parse_threat_types(args.threat_types) or []

    # Load api_endpoints and tokens
    endpoint_config, main_url, tokens = starter.load_config(args)
    if args.no_bulk:
        post_engine_add_threats = ThreatsPost(endpoint_config, args.env, tokens)
        response_dict = post_engine_add_threats.add_threats(
            list_new_threats,
            args.atom_type,
            args.whitelist,
            threat_types,
            args.public,
            args.tag,
            args.link,
            permanent
        )
    else:
        post_engine_add_threats = BulkThreatsPost(endpoint_config, args.env, tokens)
        hashkeys = post_engine_add_threats.add_bulk_threats(
            list_new_threats,
            args.atom_type,
            args.whitelist,
            threat_types,
            args.public,
            args.tag,
            args.link,
            permanent
        )
        response_dict = {'haskeys': list(hashkeys)}

    if args.output:
        starter.save_output(args.output, response_dict)
        logger.debug(f'Results saved in {args.output}\n')
    logger.debug(f'END: add_new_threats.py')


def defang_threats(threats, atom_type):
    defanged = []
    # matches urls like http://www.website.com:444/file.html
    standard_url_regex = re.compile(r'^(https?:\/\/)[a-z0-9]+([\-\.][a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
    # matches urls like http://185.25.5.3:8080/result.php (ipv4 or ipv6)
    ip_url_regex = re.compile(r'^(https?:\/\/)[0-9a-zA-Z]{1,4}([\.:][0-9a-zA-Z]{1,4}){3,7}(:[0-9]{1,5})?(\/.*)?$')
    for threat in threats:
        unmodified_threat = threat
        threat = threat.replace('[.]', '.')
        threat = threat.replace('(.)', '.')
        if atom_type == 'url':
            if not threat.startswith('http'):
                if threat.startswith('hxxp'):
                    threat = threat.replace('hxxp', 'http')
                elif threat.startswith('ftp'):
                    threat = threat.replace('ftp', 'http')
                elif threat.startswith('sftp'):
                    threat = threat.replace('sftp', 'https')
                else:
                    threat = 'http://' + threat
            if not standard_url_regex.match(threat) and not ip_url_regex.match(threat):
                logger.warning(f'\'{unmodified_threat}\' has been modified as \'{threat}\' but is still not recognized'
                               f' as an url. Skipping this line')
                continue
            if unmodified_threat != threat:
                logger.info(f'\'{unmodified_threat}\' has been modified as \'{threat}\'')
        defanged.append(threat)
    return defanged


if __name__ == '__main__':
    sys.exit(main())
