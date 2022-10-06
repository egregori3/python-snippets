import json
import argparse
import sys

SOF_LINE_NUM_FIELD = 'sof_line_num'
EOF_LINE_NUM_FIELD = 'eof_line_num'
STRING_FIELD       = 'string'

class CustomError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return str(self.message)

class AnalyzeLog:

    def __init__(self, args):
        self._log_db = []
        self.log_lines = 0
        self.csv_lines = 0
        if args['log']:
            self._process_log_into_db(args['log'], args['sof'], args['eof'], args['stop'], args['filter'])
            args['log'].close()
        else:
            raise("Cannot open log file")
        if not self._log_db:
            raise("No frames found, are you using the correct SOF/EOF strings? ({},{})".format(args['sof'], args['eof']))
        if args['csv']:
            self._write_db_to_csv(args['csv'], args['minflds'])
            args['csv'].close()
        if args['dump']:
            self._print_db()

    def _write_db_to_csv( self, csv, minflds ):
        # Write db to csv file if args.csv is set
        fields = []
        lines = 0
        print("Writing CSV file: ", end="", flush=True)
        if minflds == None or len(self._log_db) > minflds:
            for db in self._log_db:
                for key in db:
                    if key not in fields:
                        fields.append(key)
            for field in fields:
                csv.write(field+',')
            csv.write('\n')
            for db in self._log_db:
                for field in fields:
                    if field in db:
                        csv.write(db[field])
                    csv.write(',')
                csv.write('\n')
                lines = lines + 1
                if lines % (len(db)/60) == 0:
                    print("*", end="", flush=True)
        print("Wrote {} lines\n".format(lines))
        self.csv_lines = lines

    def _parse_line(self, db, line):
        parse1 = line.split('|')
        for string in parse1:
            if "=" in string:
                parse2 = string.split('=')
                if "[" in parse2[0]:
                    parse2[0] = parse2[0].partition("[")[2]
                if "]" in parse2[1]:
                    parse2[1] = parse2[1].partition("]")[0]
                db[parse2[0].strip()] = parse2[1].strip()

    def _process_log_into_db( self, log, sof, eof, stop, filter_list ):
        line_num     = 0
        sof_line_num = 0
        line_db      = {}
        in_frame     = False

        print("Processing log file: ", end="", flush=True)
        for line in log:
            if stop != None and stop in line:
                break
            line_num = line_num + 1
            if sof in line:
                if in_frame:
                    raise CustomError("Error double SOF: "+str(line_num))
                sof_line_num = line_num
                line_db      = {}
                in_frame     = True
            elif eof in line:
                if not in_frame:
                    raise CustomError("Error EOF before SOF: "+str(line_num))
                if line_db:
                    line_db[EOF_LINE_NUM_FIELD] = str(line_num)
                    line_db[SOF_LINE_NUM_FIELD] = str(sof_line_num)
                    self._log_db.append(line_db)
                in_frame = False
                if line_num % 50 == 0:
                    print("*", end="", flush=True)
            if in_frame:
                if filter_list == None:
                    process_line = True
                else:
                    process_line = False
                    for string in filter_list:
                        if string in line:
                            process_line = True
                            line_db['Data'] = string
                if process_line:
                    if "|" in line:
                        self._parse_line(line_db, line)
                    else:
                        line_db['string'] = line.replace('\n', '')
        print("\n\nProcessed {} lines\n".format(line_num))
        self.log_lines = line_num

    def _print_db(self):
        prev_db = {}
        for db in self._log_db:
            for key in db:
                print(key+" = "+db[key], end="")
                if key in prev_db and key not in [SOF_LINE_NUM_FIELD, EOF_LINE_NUM_FIELD, STRING_FIELD]:
                    if prev_db[key] != db[key]:
                        print("   previous: "+key+" = "+prev_db[key], end="")
                print()
            prev_db = db
            print()
            print()
            print("******************************************")
            print()

    def print_stats(self):
        print("Processed {} log lines\n".format(self.log_lines))
        if self.csv_lines > 0:
            print("Wrote {} csv lines\n".format(self.csv_lines))

if __name__ == "__main__":
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
            metavar='PATH',
            help="CSV output file")

    parser.add_argument('--sof',     type=str, help='String to use for start of frame',     default="NEXT_EVENT_START")
    parser.add_argument('--eof',     type=str, help='String to use for end of frame',       default="NEXT_EVENT_EXIT")
    parser.add_argument('--filter',  type=str, help='Comma seperated strings, only parse line containing string')
    parser.add_argument('--minflds', type=int, help='Minimum number of fields')
    parser.add_argument('--stop',    type=str, help='Stop string - analysis tops when this string is found')
    parser.add_argument('--profile', action='store_true', help='Post process for profile switching analysis')
    parser.add_argument('--dump',    action='store_true', help='Dump to stdout')
    a = parser.parse_args()

    try:
        analyze_obj = AnalyzeLog({  'log':a.log,
                                    'csv':a.csv,
                                    'sof':a.sof,
                                    'eof':a.eof,
                                    'filter':a.filter.split(','),
                                    'minflds':a.minflds,
                                    'stop':a.stop,
                                    'profile':a.profile,
                                    'dump':a.dump})
    except CustomError as e:
        print("!ERROR! " + str(e))

    print()
    analyze_obj.print_stats()

    print("Done")
