Preql Modules
=============

__builtins__
------------


.. function:: PY(code_expr, code_setup)

    Evaluate the given Python expression and convert the result to a Preql object

    :param  code_expr:         The Python expression to evaluate
    :type  code_expr: string
    :param  code_setup:         Setup code to prepare for the evaluation
        (default=null)
    :type  code_setup: string?

    :Note:

        This function is still experemental, and should be used with caution.

    :Example:

        .. code-block:: javascript

            >> PY("random.randrange(1, 10)", "import random")
            >> x = "Hello World"
            >> PY("'$x'[::-1]")
            "dlroW olleH"



.. function:: SQL(result_type, sql_code)

    Create an object with the given SQL evaluation code, and given result type.
    The object will only be evaluated when required by the program flow.

    :param  result_type:         The expected type of the result of the SQL query
    :type  result_type: union[collection, type]
    :param  sql_code:         The SQL code to be evaluated
    :type  sql_code: string

    :Example:

        .. code-block:: javascript

            >> ["a", "b"]{item: SQL(string, "$item || '!'")}
            table  =2
            ┏━━━━━━━┓
            ┃ item  ┃
            ┡━━━━━━━┩
            │ a!    │
            │ b!    │
            └───────┘
            >> x = ["a", "b", "c"]
            >> SQL(type(x), "SELECT item || '!' FROM $x")
            table  =3
            ┏━━━━━━━┓
            ┃ item  ┃
            ┡━━━━━━━┩
            │ a!    │
            │ b!    │
            │ c!    │
            └───────┘



.. function:: bfs(edges, initial)

    Performs a breadth-first search on a graph.

    :param  edges:         a table of type `{src: int, dst: int}`, defining the edges of the graph
    :type  edges: table
    :param  initial:         list[int], specifies from which nodes to start
    :type  initial: table



.. function:: cast(obj, target_type)

    Attempt to cast an object to a specified type
    The resulting object will be of type `target_type`, or a `TypeError`
    exception will be thrown.

    :param  obj:         The object to cast
    :type  obj: any
    :param  target_type:         The type to cast to
    :type  target_type: type



.. function:: char_range(start, end)

    Produce a list of all characters from 'start' to 'stop'

    :param  start: 
    :type  start: string
    :param  end: 
    :type  end: string

    :Example:

        .. code-block:: javascript

            >> char_range('a', 'z')



.. function:: columns(table)

    Returns a dictionary `{column_name: column_type}` for the given table

    :param  table: 
    :type  table: collection

    :Example:

        .. code-block:: javascript

            >> columns([0])
            {item: int}



.. function:: commit()

    Commit the current transaction
    This is necessary for changes to the tables to become persistent.



.. function:: connect(uri, load_all_tables, auto_create)

    Connect to a new database, specified by the uri

    :param  uri:         A string specifying which database to connect to (e.g. "sqlite:///test.db")
    :type  uri: string
    :param  load_all_tables:         If true, loads all the tables in the database into the global namespace.
        (default=false)
    :type  load_all_tables: bool
    :param  auto_create:         If true, creates the database if it doesn't already exist (Sqlite only)
        (default=false)
    :type  auto_create: bool

    :Example:

        .. code-block:: javascript

            >> connect("sqlite://:memory:")     // Connect to a database in memory



.. function:: count(obj)

    Count how many rows are in the given table, or in the projected column.
    If no argument is given, count all the rows in the current projection.

    :param  obj: 
    :type  obj: container?

    :Examples:

        .. code-block:: javascript

            >> count([0..10])
            10
            >> [0..10]{ => count() }
            table  =1
            ┏━━━━━━━┓
            ┃ count ┃
            ┡━━━━━━━┩
            │    10 │
            └───────┘
            >> [0..10]{ => count(item) }
            table  =1
            ┏━━━━━━━┓
            ┃ count ┃
            ┡━━━━━━━┩
            │    10 │
            └───────┘



.. function:: count_false(field)

    Count how many values in the field are false or zero

    :param  field: 
    :type  field: collection



.. function:: count_true(field)

    Count how many values in the field are true (non-zero)

    :param  field: 
    :type  field: collection



.. function:: debug()

    Breaks the execution of the interpreter, and enters into a debug
    session using the REPL environment.



.. function:: dict(...x)

    Construct a dictionary



.. function:: dir(obj)

    List all names in the namespace of the given object.
    If no object is given, lists the names in the current namespace.

    :param  obj: 
    :type  obj: any



.. function:: distinct(t)

    Removes identical rows from the given table

    :param  t: 
    :type  t: collection

    :Example:

        .. code-block:: javascript

            >> distinct(["a","b","b","c"])
            table  =3
            ┏━━━━━━━┓
            ┃ item  ┃
            ┡━━━━━━━┩
            │ a     │
            │ b     │
            │ c     │
            └───────┘



.. function:: enum(tbl)

    Return the table with a new index column
    Count starts from 0.

    :param  tbl: 
    :type  tbl: collection

    :Example:

        .. code-block:: javascript

            >> enum(["a", "b", "c"])
            table  =3
            ┏━━━━━━━┳━━━━━━┓
            ┃ index ┃ item ┃
            ┡━━━━━━━╇━━━━━━┩
            │     0 │ a    │
            │     1 │ b    │
            │     2 │ c    │
            └───────┴──────┘



.. function:: exit()

    Exit the current interpreter instance.
    Can be used from running code, or the REPL.
    If the current interpreter is nested within another Preql interpreter (e.g. by using debug()),
    exit() will return to the parent interpreter.



.. function:: first(obj)

    Return the first member of a column or a list

    :param  obj: 
    :type  obj: collection



.. function:: first_or_null(obj)

    Return the first member of a column or a list, or null if it's empty

    :param  obj: 
    :type  obj: collection



.. function:: fmt(s)

    Format the given string using interpolation on variables marked as `$var`

    :param  s: 
    :type  s: string

    :Example:

        .. code-block:: javascript

            >> ["a", "b", "c"]{item: fmt("$item!")}
            table  =3
            ┏━━━━━━━┓
            ┃ item  ┃
            ┡━━━━━━━┩
            │ a!    │
            │ b!    │
            │ c!    │
            └───────┘



.. function:: force_eval(expr)

    Forces the evaluation of the given expression.
    Executes any db queries necessary.

    :param  expr: 
    :type  expr: object



.. function:: get_db_type()

    Returns a string representing the type of the active database.

    :Example:

        .. code-block:: javascript

            >> get_db_type()
            "sqlite"



.. function:: help(inst)

    Provides a brief summary for the given object

    :param  inst: 
    :type  inst: any



.. function:: import_csv(table, filename, header)

    Import a csv file into an existing table

    :param  table:         A table into which to add the rows.
    :type  table: table
    :param  filename:         A path to the csv file
    :type  filename: string
    :param  header:         If true, skips the first line
        (default=false)
    :type  header: bool



.. function:: import_table(name, columns)

    Import an existing table from the database, and fill in the types automatically.

    :param  name:         The name of the table to import
    :type  name: string
    :param  columns:         If this argument is provided, only these columns will be imported.
        (default=null)
    :type  columns: list[item: string]

    :Example:

        .. code-block:: javascript

            >> import_table("my_sql_table", ["some_column", "another_column])



.. function:: inspect_sql(obj)

    Returns the SQL code that would be executed to evaluate the given object

    :param  obj: 
    :type  obj: object



.. function:: is_empty(tbl)

    Efficiently tests whether the table expression `tbl` is empty or not

    :param  tbl: 



.. function:: isa(obj, type)

    Checks if the give object is an instance of the given type

    :param  obj: 
    :type  obj: any
    :param  type: 
    :type  type: type

    :Examples:

        .. code-block:: javascript

            >> isa(1, int)
            true
            >> isa(1, string)
            false
            >> isa(1.2, number)
            true
            >> isa([1], table)
            true



.. function:: issubclass(a, b)

    Checks if type 'a' is a subclass of type 'b'

    :param  a: 
    :type  a: type
    :param  b: 
    :type  b: type

    :Examples:

        .. code-block:: javascript

            >> issubclass(int, number)
            true
            >> issubclass(int, table)
            false
            >> issubclass(list, table)
            true



.. function:: join(...tables)

    Inner-join any number of tables.
    Each argument is expected to be one of -
    (1) A column to join on. Columns are attached to specific tables. or
    (2) A table to join on. The column will be chosen automatically, if there is no ambiguity.
    Connections are made according to the relationships in the declaration of the table.

    :param  tables:         Each argument must be either a column, or a table.

    :Returns:

        A new table, where each column is a struct representing one of
        the joined tables.

    :Examples:

        .. code-block:: javascript

            >> join(a: [0].item, b: [0].item)
            table join46 =1
            ┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
            ┃ a           ┃ b           ┃
            ┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
            │ {'item': 0} │ {'item': 0} │
            └─────────────┴─────────────┘
            >> join(a: [1..5].item, b: [3..8].item) {...a}
            table  =2
            ┏━━━━━━━┓
            ┃  item ┃
            ┡━━━━━━━┩
            │     3 │
            │     4 │
            └───────┘
            >> join(c: Country, l: Language) {...c, language: l.name}



.. function:: joinall(...tables)

    Cartesian product of any number of tables
    See `join`

    :Example:

        .. code-block:: javascript

            >> joinall(a: [0,1], b: ["a", "b"])
            table joinall14 =4
            ┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
            ┃ a           ┃ b             ┃
            ┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
            │ {'item': 0} │ {'item': 'a'} │
            │ {'item': 0} │ {'item': 'b'} │
            │ {'item': 1} │ {'item': 'a'} │
            │ {'item': 1} │ {'item': 'b'} │
            └─────────────┴───────────────┘



.. function:: leftjoin(...tables)

    Left-join any number of tables
    See `join`



.. function:: length(s)

    Returns the length of the string
    For tables or lists, use `count()`

    :param  s: 
    :type  s: union[string, vectorized[item: string]]



.. function:: limit(tbl, n)

    Return the first 'n' rows in table

    :param  tbl: 
    :type  tbl: collection
    :param  n: 
    :type  n: int



.. function:: limit_offset(tbl, lim, offset)

    Return the first 'n' rows in table at given offset

    :param  tbl: 
    :type  tbl: collection
    :param  lim: 
    :type  lim: int
    :param  offset: 
    :type  offset: int



.. function:: list_median(x)

    Find the median of a list
    Cannot be used inside a projection.

    :param  x: 
    :type  x: list[any]



.. function:: lower(s)

    Return a copy of the string converted to lowercase.

    :param  s: 
    :type  s: union[string, vectorized[item: string]]



.. function:: map_range(tbl, start, end)

    For each row in the table, assigns numbers out of a range, and
    produces `(end-start)` new rows instead, each attached to a number.
    If `start` or `end` are functions, the index is the result of the function, per row.

    :param  tbl:         Table to map the range onto
    :type  tbl: table
    :param  start:         The starting index, or a function producing the starting index
    :type  start: union[int, function]
    :param  end:         The ending index, or a function producing the ending index
    :type  end: union[int, function]

    :Examples:

        .. code-block:: javascript

            >> map_range(["a", "b"], 0, 3)
            table  =6
            ┏━━━┳━━━━━━┓
            ┃ i ┃ item ┃
            ┡━━━╇━━━━━━┩
            │ 0 │ a    │
            │ 1 │ a    │
            │ 2 │ a    │
            │ 0 │ b    │
            │ 1 │ b    │
            │ 2 │ b    │
            └───┴──────┘
            >> map_range(["a", "ab"], 1, length)
            table  =3
            ┏━━━┳━━━━━━┓
            ┃ i ┃ item ┃
            ┡━━━╇━━━━━━┩
            │ 1 │ a    │
            │ 1 │ ab   │
            │ 2 │ ab   │
            └───┴──────┘



.. function:: max(field)

    Find the maximum of a column or a list

    :param  field: 
    :type  field: collection



.. function:: mean(field)

    Mean of a column or a list

    :param  field: 
    :type  field: collection



.. function:: min(field)

    Find the minimum of a column or a list

    :param  field: 
    :type  field: collection



.. function:: names(obj)

    List all names in the namespace of the given object.
    If no object is given, lists the names in the current namespace.

    :param  obj: 
    :type  obj: any



.. function:: outerjoin(...tables)

    Outer-join any number of tables
    See `join`



.. function:: page(table, index, page_size)

    Pagination utility function for tables

    :param  table: 
    :param  index: 
    :param  page_size: 



.. function:: remove_table(table_name)

    Remove table from database (drop table)

    :param  table_name: 



.. function:: repr(obj)

    Returns the representation text of the given object

    :param  obj: 
    :type  obj: any



.. function:: rollback()

    Rollback the current transaction
    This reverts the data in all the tables to the last commit.
    Local variables will remain unaffected.



.. function:: round(n)

    Returns a rounded float

    :param  n: 
    :type  n: union[number, vectorized[item: number]]

    :Example:

        .. code-block:: javascript

            >> round(3.14)
            3.0



.. function:: sample_fast(tbl, n, bias)

    Returns a random sample of n rows from the table in one query (or at worst two queries)

    :param  tbl:         The table to sample from
    :type  tbl: collection
    :param  n:         The number of items to sample
    :type  n: int
    :param  bias:         Add bias (reduce randomness) to gain performance. Higher values of 'bias'
        increase the chance of success in a single query, but may introduce a
        higher bias in the randomness of the chosen rows, especially in sorted tables.
        (default=0.05)
    :type  bias: number



.. function:: sample_ratio_fast(tbl, ratio)

    Returns a random sample of rows from the table, at the approximate amount of (ratio*count(tbl)).

    :param  tbl: 
    :param  ratio: 



.. function:: serve_rest(endpoints, port)

    Start a starlette server (HTTP) that exposes the current namespace as REST API

    :param  endpoints:         A struct of type (string => function), mapping names to the functions.
    :type  endpoints: struct
    :param  port:         A port from which to serve the API
        (default=8080)
    :type  port: int

    :Note:

        Requires the `starlette` package for Python. Run `pip install starlette`.

    :Example:

        .. code-block:: javascript

            >> func index() = "Hello World!"
            >> serve_rest({index: index})
            INFO     Started server process [85728]
            INFO     Waiting for application startup.
            INFO     Application startup complete.
            INFO     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)



.. function:: str_contains(substr, s)

    Tests whether string `substr` is contained in `s`

    :param  substr: 
    :type  substr: string
    :param  s: 
    :type  s: string

    :Example:

        .. code-block:: javascript

            >> str_contains("i", "tim")
            true
            >> str_contains("i", "team")
            false



.. function:: str_notcontains(substr, s)

    Tests whether string `substr` is not contained in `s`
    Equivalent to `not str_contains(substr, s)`.

    :param  substr: 
    :type  substr: string
    :param  s: 
    :type  s: string



.. function:: sum(field)

    Sum up a column or a list

    :param  field: 
    :type  field: collection



.. function:: table_concat(t1, t2)

    Concatenate two tables (union all). Used for `t1 + t2`

    :param  t1: 
    :type  t1: collection
    :param  t2: 
    :type  t2: collection



.. function:: table_intersect(t1, t2)

    Intersect two tables. Used for `t1 & t2`

    :param  t1: 
    :type  t1: collection
    :param  t2: 
    :type  t2: collection



.. function:: table_subtract(t1, t2)

    Substract two tables (except). Used for `t1 - t2`

    :param  t1: 
    :type  t1: collection
    :param  t2: 
    :type  t2: collection



.. function:: table_union(t1, t2)

    Union two tables. Used for `t1 | t2`

    :param  t1: 
    :type  t1: collection
    :param  t2: 
    :type  t2: collection



.. function:: tables()

    Returns a table of all the persistent tables in the database.
    The resulting table has two columns: name, and type.



.. function:: temptable(expr, const)

    Generate a temporary table with the contents of the given table
    It will remain available until the database session ends, unless manually removed.

    :param  expr:         the table expression to create the table from
    :type  expr: collection
    :param  const:         whether the resulting table may be changed or not.
        (default=null)
    :type  const: bool?

    :Note:

        A non-const table creates its own `id` field.
        Trying to copy an existing id field into it will cause a collision



.. function:: type(obj)

    Returns the type of the given object

    :param  obj: 
    :type  obj: any

    :Example:

        .. code-block:: javascript

            >> type(1)
            int
            >> type([1])
            list[item: int]
            >> type(int)
            type



.. function:: upper(s)

    Return a copy of the string converted to uppercase.

    :param  s: 
    :type  s: union[string, vectorized[item: string]]



.. function:: zipjoin(a, b)

    Joins two tables on their row index.
    Column names are always `a` and `b`.
    Result is as long as the shortest table.
    Similar to Python's `zip()` function.

    :param  a: 
    :type  a: collection
    :param  b: 
    :type  b: collection

    :Example:

        .. code-block:: javascript

            >> zipjoin(["a", "b"], [1, 2])
            table  =2
            ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
            ┃ a             ┃ b           ┃
            ┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
            │ {'item': 'a'} │ {'item': 1} │
            │ {'item': 'b'} │ {'item': 2} │
            └───────────────┴─────────────┘



.. function:: zipjoin_left(a, b)

    Similar to `zipjoin`, but the result is as long as the first parameter.
    Missing rows will be assigned `null`.

    :param  a: 
    :type  a: collection
    :param  b: 
    :type  b: collection

    :Example:

        .. code-block:: javascript

            >> zipjoin_left(["a", "b"], [1])
            table  =2
            ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
            ┃ a             ┃ b              ┃
            ┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
            │ {'item': 'a'} │ {'item': 1}    │
            │ {'item': 'b'} │ {'item': null} │
            └───────────────┴────────────────┘



.. function:: zipjoin_longest(a, b)

    Similar to `zipjoin`, but the result is as long as the longest table.
    Missing rows will be assigned `null`.

    :param  a: 
    :type  a: collection
    :param  b: 
    :type  b: collection


