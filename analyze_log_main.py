import argparse
import sys
import analyze_log


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
    parser.add_argument('--prev',    action='store_true', help='Output differences')
    parser.add_argument('--lines',   action='store_true', help='Add log line numbers')
    a = parser.parse_args()

    if a.hist:
        parms['post_process_line'] = process_histogram

    try:
        analyze_obj = analyze_log.AnalyzeLog({  'log':a.log,
                                                'sof':a.sof,
                                                'eof':a.eof,
                                                'csv':a.csv,
                                                'prev':a.prev,
                                                'lines':a.lines,
                                                'filter':a.filter.split(',')})

    except analyze_log.CustomError as e:
        print("!ERROR! " + str(e))
    else:
        csv_lines = 0

        if 'csv' in a and a.csv:
            csv_lines = analyze_obj.write_db_to_csv( a.csv, a.minflds )
            a.csv.close()
        if 'dump' in a and a.dump:
            analyze_obj.print_db( )

        print()
        print("\n\nRead {} csv lines\n".format(analyze_obj.get_log_lines()))
        print("\nWrote {} csv lines\n".format(csv_lines))
        print()
        print("Done")
