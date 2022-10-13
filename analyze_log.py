import json

SOF_LINE_NUM_FIELD = 'sof_line_num'
EOF_LINE_NUM_FIELD = 'eof_line_num'
STRING_FIELD       = 'string'

class CustomError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return str(self.message)


def _post_process_line(db):
    return db


class AnalyzeLog:

    def __init__(self, parms):
        self._log_db     = []
        self.csv_lines   = 0

        if 'log' not in parms:
            raise("Cannot open log file")

        if 'sof' not in parms:
            raise("--sof must be specified")

        if 'eof' not in parms:
            raise("--eof must be specified")

        self.log_lines = self._process_log_into_db( parms )
        if not self._log_db:
            raise("No frames found, are you using the correct SOF/EOF strings? ({},{})".format(args['sof'], args['eof']))
        if 'prev' in parms and parms['prev']:
            self._add_changed_line()


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


    def _add_changed_line( self ):
        prev_db = {}
        for db in self._log_db:
            new_db = {}
            for key in db:
                if key in prev_db and key not in [SOF_LINE_NUM_FIELD, EOF_LINE_NUM_FIELD, STRING_FIELD]:
                    if prev_db[key] != db[key]:
                        new_db['previous_'+key] = prev_db[key]
            prev_db = db
            db.update(new_db)


    def _process_log_into_db( self, parms ):

        line_num        = 0
        sof_line_num    = 0
        line_db         = {}
        in_frame        = False

        log             = parms['log']
        sof             = parms['sof']
        eof             = parms['eof']

        post_process_line = _post_process_line
        if 'post_process_line' in parms:
            post_process_line = parms['post_process_line']

        print("Processing log file: ", end="", flush=True)
        for line in log:
            if 'stop' in parms and stop in line:
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
                if 'filter' not in parms:
                    process_line = True
                else:
                    process_line = False
                    for string in parms['filter']:
                        if string in line:
                            process_line = True
                            if 'Data' in line_db:
                                if string not in line_db['Data']:
                                    line_db['Data'] = line_db['Data']+' '+string
                            else:
                                line_db['Data'] = string
                if process_line:
                    if "|" in line:
                        self._parse_line(line_db, line)
                        line_db = post_process_line(line_db)
                    else:
                        line_db['string'] = line.replace('\n', '')
        print("\n\nProcessed {} lines\n".format(line_num))
        return line_num


    def get_log_lines( self ):
        return self.log_lines


    def write_db_to_csv( self, csv, minflds ):
        # Write db to csv file if args.csv is set
        fields = []
        lines = 0
        print("Writing CSV file: ", end="", flush=True)
        if minflds == None or len(self.log_db) > minflds:
            # get fields
            for db in self._log_db:
                for key in db:
                    if key not in fields:
                        fields.append(key)
            # write headers
            for field in fields:
                csv.write(field+',')
            csv.write('\n')
            # write data
            prev_db = {}
            for db in self._log_db:
                # write line
                for field in fields:
                    if field in db:
                        csv.write(db[field])
                    csv.write(',')
                csv.write('\n')
                lines = lines + 1
                # after writing lines
                prev_db = db
                if lines % (len(db)/60) == 0:
                    print("*", end="", flush=True)
        return lines


    def print_db( self ):
        prev_db = {}
        for db in self._log_db:
            for key in db:
                print(key+" = "+db[key], end="")
                print()
            prev_db = db
            print()
            print()
            print("******************************************")
            print()


