
import sys
import os
import stat
import argparse
from pathlib import Path

#print symlink_info
def print_lynk_info(path):
    stat_info = os.lstat(path)
    target_path = os.readlink(path)
    print(f"""\t*****************
     Target: {target_path}
     Permissions: {stat_info.st_mode}
     Owner: {stat_info.st_uid}
     Group: {stat_info.st_gid}
     Size: {stat_info.st_size} bytes
     Last modified: {stat_info.st_mtime}
     Last accessed: {stat_info.st_atime}
     Creation time: {stat_info.st_ctime}
\t****************""")
    return

#print file info
def follow_link(target):
    target_path = os.path.realpath(target)
    target_name = os.path.basename(target_path)
    file_size = os.path.getsize(target_path)

    print(f""" \tThe name of the target file is {target_name}.
    \tThe size of the target file is {file_size}.""")
    return

def check_optional(file_path,args):
    #Check if -L
                if args.follow_symlink:
                    args.symlink_info = False
                    follow_link(file_path)
    #Check if -H
                elif args.symlink_args:
                    args.symlink_info = False
                    if os.path.basename(file_path)== args.name:
                        follow_link(file_path)
                    else:
                        print_lynk_info(file_path)
    #Check if -p
                elif args.symlink_info:
                    print_lynk_info(file_path)
    # exception
                else :
                    print("***** error with symlink*****")
                return


# find files with specified name
def name_find(start, args):
    for file_path in start.rglob(args.name):
        if file_path.is_symlink():
            check_optional(file_path,args)
        else:
            print(file_path)

def type_find(start, args):
    if args.type not in ['d','f']:
        print(f"Unknown type: {args.type}")
        sys.exit(1)

    for f in start.rglob(args.name or '*'):
        if args.type == "d" and f.is_dir():
            print(f)
        elif args.type == "f" and f.is_file() :
            if f.is_symlink():
                check_optional(f,args)
            else :
                print(f)
        else:
                print("type not recognised")


def find_files(args):
    start_path = Path(args.start)
    valid_path = Path.exists(start_path)

    if valid_path :
        if(args.name)and(not args.type):
            name_find(start_path, args)
        elif args.type:
            type_find(start_path, args)
        else:
            print("You need either --name or --type")
            sys.exit(1)
    else:
        print("problem with path input")



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('start', type=str)
    parser.add_argument('--name', type=str)
    parser.add_argument('--type' , type=str)
    parser.add_argument('-p','--symlink_info',action='store_true',default=True,help ="prints out symlink information")
    parser.add_argument('-L','--follow_symlink',action='store_true',help='Follows the symbolic link to file location')
    parser.add_argument('-H','--symlink_args',action='store_true',help='Follows the symbolic link to file location')
    return parser.parse_args()

find_files(parse_args())
