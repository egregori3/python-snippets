import json
import argparse
import sys

show = ["", ""]

SOF_LINE_NUM = 'sof_line_num'
EOF_LINE_NUM = 'eof_line_num'

def display_line(line_num,line):
    for string in show:
        if string in line:
            print(str(line_num)+":"+line)

def parse_line(db, line):
    parse1 = line.split('|')
    for string in parse1:
        if "=" in string:
            parse2 = string.split('=')
            if "[" in parse2[0]:
                parse2[0] = parse2[0].partition("[")[2]
            if "]" in parse2[1]:
                parse2[1] = parse2[1].partition("]")[0]
            db[parse2[0].strip()] = parse2[1].strip()

def process_log_into_db( args ):
    line_num     = 0
    sof_line_num = 0
    line_db      = {}
    log_db       = []

    for line in args.log:
        if args.stop in line:
            break
        line_num = line_num + 1
        if args.show:
            display_line(line_num,line,args.split(','))
        if args.sof in line:
            sof_line_num = line_num
            line_db = {}
        elif "|" in line:
            if args.filter != None:
                if args.filter in line:
                    parse_line(line_db, line)
            else:
                parse_line(line_db, line)
        elif args.eof in line:
            line_db[EOF_LINE_NUM] = str(line_num)
            line_db[SOF_LINE_NUM] = str(sof_line_num)
            log_db.append(line_db)
    return log_db

def print_db(prev_db,db):
    for key in db:
        print(key+" = "+db[key], end="")
        if key in prev_db:
            if key not in [SOF_LINE_NUM, EOF_LINE_NUM]:
                if prev_db[key] != db[key]:
                    print("   previous: "+key+" = "+prev_db[key], end="")
        print()
    if db:
        print()
        print("******************************************")
        print()

def write_db_to_csv( args ):
# Write db to csv file if args.csv is set
if args.csv != None:
    fields = []
    for db in csv_rows:
        for key in db:
            if key not in fields:
                fields.append(key)
    for field in fields:
        args.csv.write(field+',')
    args.csv.write('\n')
    for db in csv_rows:
        for field in fields:
            if field in db:
                args.csv.write(db[field])
            args.csv.write(',')
        args.csv.write('\n')

def db_filter( args ):


#
# Parse command line options
#
parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Process log file")

parser.add_argument(
    '--log', '-l',
    type=argparse.FileType('r'),
    default=sys.stdin,
    metavar='PATH',
    help="Input file (default: standard input).")

parser.add_argument(
        '--csv',
        type=argparse.FileType('w'),
        metvar='PATH',
        help="CSV output file")

parser.add_argument('--sof',     type=str, help='String to use for start of frame',     default="NEXT_EVENT_START")
parser.add_argument('--eof',     type=str, help='String to use for end of frame',       default="NEXT_EVENT_EXIT")
parser.add_argument('--trigger', type=str, help='String to trigger an output')
parser.add_argument('--show',    type=str, help='Comma delimited search terms to show')
parser.add_argument('--filter',  type=str, help='Only parse line containing string')
parser.add_argument('--minflds', type=int, help='Minimum number of fields')
parser.add_argument('--stop',    type=str, help='Stop string - analysis tops when this string is found')
parser.add_argument('--profile', action='store_true', help='Post process for profile switching analysis')
parser.add_argument('--dump',    action='store_true', help='Dump to stdout')
args = parser.parse_args()

log_db = process_log_into_db(args)




            if args.minflds == None or len(db) > args.minflds:
                if args.csv != None:
                    csv_rows.append(db)


if args.dump:
        if args.trigger == None:
            dump = True
    if args.trigger:
        if args.trigger in line:
            dump = True
        if dump:
            if args.dump:
                print_db(prev_db,db)
            dump = False






