-----------------------------------------------------------------
          _          _                         _    __   __ 
         /_\   _____(_)__ _ _ _  _ __  ___ _ _| |_ /  \ / / 
        / _ \ (_-<_-< / _` | ' \| '  \/ -_) ' \  _| () / _ \
       /_/ \_\/__/__/_\__, |_||_|_|_|_\___|_||_\__|\__/\___/
                      |___/                                 
-----------------------------------------------------------------

[AUTHOR]  Matt W. Martin, 4374851
          kaethis@tasmantis.net

[VERSION] 1.0

[PROJECT] CS2910, Assign06
          PSEUDO-SQL DBMS w/ REDIS (PYTHON)

          A Python program for administrating a simple database
          using an SQL-like language.  Uses Redis as its back-
          end.  A connection to a Redis database over localhost
          interface on default port 6379 is required (in other
          words, make sure Redis is installed and running).

          The program can load a csv file in order to populate
          the contents of the Redis database.  It's expected that
          a csv file will be supplied its first runthrough.

          Executing the program displays the menu showing the
          contents of the database.  Use the [UP] and [DOWN]
          arrow keys to navigate the menu.  Press the [ENTER] or
          [RET] key to input a command. 

          Commands are as follows:

          - 'CLOSE'  : Quits the program.

          - 'EXIT'   : See 'CLOSE'.

          - 'QUIT'   : See 'CLOSE'.

          - 'DELETE' : Deletes one or more records matching
                       requisite clause in the form:
                       'WHERE attrib==value'.

                       [Ex] 'DELETE WHERE ID==9901'

          - 'SELECT' : Selects attributes of one or more records
                       matching optional 'WHERE' clause (see
                       'DELETE').  If no attributes provided:
                       selects all attrs.  If no clause provided:
                       selects all records.

                       [Ex] 'SELECT'
                            'SELECT FNAME,LNAME'
                            'SELECT FNAME,LNAME WHERE ID==9901'

          - 'SHOW'   : See 'SELECT'

          - 'ADD'    : Takes a list of comma-separated values and
                       adds a record to the database.  Each value
                       represents an attribute described by the
                       schema, and therefore must comply with the
                       schema.

                       [Ex] 'ADD 9901,MATT,MARTIN'
                            (where schema is: [ID,4,NUM],
                                              [FNAME,10,ALPHA],
                                              [LNAME,15,ALPHA])

          All changes to the database are committed upon the
          execution of the command.
      
[DATE]    12-Apr-2017

[ISSUED]  03-Apr-2017

[USAGE]   'python3 driver.py' OR
          'python3 driver.py -csv filename.csv'

[FILES]   ./README.txt
          ./driver.py
          ./dbmgr.py
          ./ui.py
          ./employees.csv
          ./users.csv

[ISSUES]  - [1.0] AGAIN, NO ON-SCREEN MENU
            The program operates on the assumption that the user
            has read this README and has a full understanding of
            the commands listed and described above, but this is
            simply an unrealistic expectation.  I really ought to
            take the time to create a window somewhere inside the
            interface that tells the user what database commands
            are available within the program itself.  Until then,
            I'll stubbornly say to the user: RTFM!

[REPO]    https://github.com/kaethis/CS2910_Assign06
