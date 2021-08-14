import subprocess
import argparse
import re

parser = argparse.ArgumentParser(
    description='Rsync if both source and destination are present')
parser.add_argument('source', help='path/to/source_folder')
parser.add_argument('destination', help='path/to/destination_folder')
parser.add_argument('-z', '--zip_archive_recusive',
                    help='zip transfer, archived, and recursively transfered', action="store_true")
parser.add_argument('-d', '--delete',
                    help='delete files if destination is not in source', action="store_true")
args = parser.parse_args()

command_output = subprocess.check_output(
    'df -h', shell=True).decode().split('\rn')[0].split('\n')[1:-1]

mount_paths = [re.sub(r"\s+", " ", each_line).split()[-1]
               for each_line in command_output]

check_for_existance = len(list(filter(lambda x: x in args.source, mount_paths))) == len(
    list(filter(lambda x: x in args.destination, mount_paths))) == 2

if check_for_existance:
    if args.zip_archive_recusive:
        if args.delete:
            subprocess.run(
                f'/usr/bin/rsync -zar --delete-during {args.source} {args.destination}', shell=True)
        else:
            subprocess.run(
                f'/usr/bin/rsync -zar {args.source} {args.destination}', shell=True)
    else:
        if args.delete:
            subprocess.run(
                f'/usr/bin/rsync -ar --delete-during {args.source} {args.destination}', shell=True)
        else:
            subprocess.run(
                f'/usr/bin/rsync -ar {args.source} {args.destination}', shell=True)
else:
    print(parser.print_help())
