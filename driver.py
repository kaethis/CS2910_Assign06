#!/usr/bin/env python3

import argparse

import dbmgr

import ui


success = { 'OKADD'  : 'RECORD ADDED!',
            'OKDEL'  : 'RECORD(S) DELETED!' }

error =   { 'INVSYN' : 'INVALID SYNTAX!',
            'INVLEN' : 'INVALID LENGTH!',
            'INVTYP' : 'INVALID TYPECH!',
            'INVFRM' : 'INVALID FORMAT!',
            'NOKEY'  : 'KEY ALREADY EXISTS!',
            'NOREC'  : 'RECORD(S) NOT FOUND!',
            'NOATTR' : 'ATTRIBUTE(S) NOT FOUND!' }


def add(args):

    if len(args) == 1 and len(args[0].split(',')) == len(dbmgr.getSchema()):

        schema = dbmgr.getSchema()

        args = args[0].split(',')

        rec = {}

        for i, s in enumerate(schema): rec[s[0]] = args[i]

        for s in schema:

            if not len(rec[s[0]]) <= int(s[1]): return 'INVLEN'

            elif not ui.regex[s[2]].match(rec[s[0]]): return 'INVTYP'


        key = rec[schema[0][0]]

        attrs = []

        for s in schema: attrs.append(rec[s[0]])


        if not dbmgr.add(key, attrs): return 'NOKEY'

        else: return 'OKADD'


    else: return 'INVSYN' 


def delete(args):

    if len(args) == 2 and args[0] == 'WHERE':

        schema = dbmgr.getSchema()

        args = args[1].split('==')

        if len(args) == 2:

            is_invalid = True

            for s in schema:

                if args[0] == s[0]: is_invalid = False

            if is_invalid: return 'NOATTR'


            collect = []

            for rec in dbmgr.getRecords():

                if args[1] in rec[args[0]]: collect.append(rec)

            if len(collect) == 0: return 'NOREC'

            else:

                for c in collect: dbmgr.delete(c[schema[0][0]])

                return 'OKDEL'

        else: return 'INVSYN'


def select(args):

    if len(args) == 0:

        schema = dbmgr.getSchema()

        collect = dbmgr.getRecords()

        return [schema, collect]


    elif len(args) == 1:

        schema = []

        attrs = args[0].split(',')

        if not len(attrs) == 0:

            for a in attrs:

                is_invalid = True

                for s in dbmgr.getSchema():

                    if a == s[0]:

                        schema.append(s)

                        is_invalid = False

                if is_invalid: return 'NOATTR'


            collect = dbmgr.getRecords()

            return [schema, collect]

        else: return 'INVSYN'


    elif len(args) == 2 and args[0] == 'WHERE':

        schema = dbmgr.getSchema()

        args = args[1].split('==')

        if len(args) == 2:

            is_invalid = True

            for s in dbmgr.getSchema():

                if args[0] == s[0]: is_invalid = False

            if is_invalid: return 'NOATTR'


            collect = []

            for rec in dbmgr.getRecords():

                if args[1] in rec[args[0]]: collect.append(rec)

            if len(collect) == 0: return 'NOREC'

            else: return [schema, collect]

        else: return 'INVSYN'


    elif len(args) == 3 and args[1] == 'WHERE':

        schema = []

        attrs = args[0].split(',')

        if not len(attrs) == 0:

            is_invalid = True

            for a in attrs:

                for s in dbmgr.getSchema():

                    if a == s[0]:

                        schema.append(s)

                        is_invalid = False

                if is_invalid: return 'NOATTR'


            args = args[2].split('==')

            if len(args) == 2:

                is_invalid = True

                for s in dbmgr.getSchema():

                    if args[0] == s[0]: is_invalid = False

                if is_invalid: return 'NOATTR'


                collect = []

                for rec in dbmgr.getRecords():

                    if args[1] in rec[args[0]]: collect.append(rec)

                if len(collect) == 0: return 'NOREC'

                else: return [schema, collect]

            else: return 'INVSYN'

        else: return 'INVSYN'


    else: return 'INVSYN'


def exit(args):

    y, x = 1, 2

    if ui.confirm(y, x, 'EXIT?') == 0:

        ui.exit()

        quit();


def main(args):

    ui.init()


    if not args.csv == None:

        dbmgr.redis.flushdb()


        filename = args.csv

        try:

            schema = []

            with open(filename, 'r') as file:

                attribs = file.readline().rstrip().split(',')

                lengths = file.readline().rstrip().split(',')

                typechs = file.readline().rstrip().split(',')


                for i in range(len(attribs)):

                    schema.append([ attribs[i], lengths[i], typechs[i] ])

                dbmgr.init(schema)


                for line in file:

                    line = line.rstrip()

                    if line:

                        attrs = line.split(',')

                        key = attrs[0]

                        dbmgr.add(key, attrs)


        except FileNotFoundError:

            y, x = 1, 2

            ui.alert(y, x, 'FILE NOT FOUND!')

            ui.exit()

            quit();


    if (dbmgr.redis.get('SCHEMA')) == None:

        y, x = 1, 2

        ui.alert(y, x, 'SCHEMA NOT FOUND!')

        ui.exit()

        quit();


    args = []

    cmds = { 'ADD'    : add,
             'DELETE' : delete,
             'SELECT' : select,
             'SHOW'   : select,
             'EXIT'   : exit,
             'QUIT'   : exit,
             'CLOSE'  : exit }


    y, x = 1, 2

    height = 15

    ret = select(args)

    ret = ui.menuwin(y, x, height, 0, ret[0], ret[1])

    if ret == ui.keyboard['ESC']: exit(args)


    while True:

        y, x = 1, 2

        typech = 'VARCHAR'

        length = 55

        title = 'INPUT'

        buffer = ui.textwin(y, x, typech, length, title, False)


        if not buffer == ui.keyboard['ESC']:

            args = buffer.split(' ');

            if args[0] in cmds:

                ret = cmds[args[0]](args[1:])

                if str(ret) in error:

                    y, x = 2, 3

                    ui.alert(y, x, error[ret])

                elif str(ret) in success:

                    y, x = 2, 3

                    ui.alert(y, x, success[ret])


                    y, x = 1, 2

                    schema = dbmgr.getSchema()

                    collect = dbmgr.getRecords()

                    ret = ui.menuwin(y, x, height, 0, schema, collect)

                    if ret == ui.keyboard['ESC']: exit(args)

                else:

                    y, x = 1, 2

                    ret = ui.menuwin(y, x, height, 0, ret[0], ret[1])

                    if ret == ui.keyboard['ESC']: exit(args)
                    
            else:

                y, x = 2, 3

                ui.alert(y, x, error['INVSYN'])

        else:
        
            exit(args)

 
if __name__ == '__main__':

    description = '''A simple Python database program with a Redis backend.
                  '''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-csv',
                        metavar='csv',
                        type=str,
                        help='comma-separated-value file')

    args = parser.parse_args()

    main(args)
