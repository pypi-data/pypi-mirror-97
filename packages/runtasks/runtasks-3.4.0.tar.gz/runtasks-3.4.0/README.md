# runtasks

A simple task runner for Python that is useful for build scripts.

It is designed to allow Python functions to be called from the command line with no frameworks
to get in the way.  The "run" utility searches up the directory tree for a file named
"tasks.py".  Any functions decorated with `@task` are callable from the command line.

For example, given a tasks.py file like this:

    from runtasks import task

    @task
    def hello(who='World'):
        "Prints a friendly greeting"
        print('Hello, {}!'.format(who))
        
the hello function can be called in any of these ways:

``` text
$ run hello
Hello, World!

$ run hello who=Bob
Hello, Bob!

$ run hello Bob
Hello, Bob!

$ run hello -w Bob
Hello, Bob!
```

Use the `--list` option to print the list of tasks, their options, and documentation strings:

``` text
$ run --list

Available tasks:

hello
  who='World'

  Prints a friendly greeting
```

Use `--help` to get help on any of the tasks:

``` text
$ run hello --help
hello
  who='World'

  Prints a friendly greeting
```

### Features

* Commands are simple Python functions.
* Flexible command line parsing.
* Supports text arguments, Boolean flags, integers, and counters.


## Command Line Parsing

Command line input is extremely flexible and yet is designed to not require any configuration -
just the function signature.

Multiple tasks can be passed on the command line and they are executed in the order
specified:

``` text
$ run createdb testdb smoketests
```

Arguments can be passed to tasks in a number of formats:

 * Name and Value:
   * `run hello --who=Bob`
   * `run hello --who Bob`
   * `run hello who=Bob`
 * Value:
   * `run hello Bob`
 * Flags:
   * `run hello --debug`
   * `run hello --no-debug`
   * `run hello -d`
 * Counters:
   * `run hello -vvv`

### Value Parameters

Parameters can be provided values.  If a parameter does not have a default value, a value must
be provided.

    @task
    def sometask(arg1, arg2='defvalue'):
        print('arg1={} arg2={}'.format(arg1, arg2))

Values can be provided in a few ways:

``` text
$ run sometask --arg1=value1 --arg2=value2
arg1=value1 arg2=value2

$ run sometask --arg2=value2 --arg1=value1
arg1=value1 arg2=value2

$ run sometask --arg1 value1
arg1=value1 arg2=defvalue

$ run sometask arg1=value1
arg1=value1 arg2=defvalue

$ run sometask value1
arg1=value1 arg2=defvalue

$ run sometask value1 value2
arg1=value1 arg2=value2

$ runtask sometask
Task sometask argument arg1 was not provided a value
```

Notice that arguments can be provided in any order when providing the name of the argument.  To
provide values without names (e.g. `runtask sometask value1 value2`), the arguments must be in
order.  These are only accepted before arguments with names, so the following is not valid:

``` text
# NOT VALID
$ run sometask --arg1=value1 value2
```

Since arg1 was provided with a name, "value2" will be assumed to be the next task name to run.

### Flag Parameters

When a default parameter is set to `True` or `False`, the argument generally does not accept a
value on the command line.  Instead, the argument name itself is accepted to mean the flag
should be set to `True` and the argument name preceded by "no-" is accepted to mean the flag
should be set to `False`.

    @task
    def sometask(flag1=False, flag2=True):
        print(flag1, flag2)

    $ run sometask
    False True

    $ run sometask --flag1
    True True

    $ run sometask --no-flag2
    False False

    $ run sometask --no-flag1
    False true

Note that flag parameter names require dashes.  The following does not work because it will try
to pass the value "flag1" to the first parameter, but values are not accepted for flags:

``` text
$ run sometask flag1
Task sometask flag1 parameter is a flag.  Invalid value 'flag1'
```

It is usually not necessary, but the values 0 and 1 can be passed to Boolean parameters:

``` text
$ run sometask --flag1 1
True True

$ run sometask --flag2 0
False False

$ run sometask 1
True True
```

### Integers

When a default parameter is an integer, the value passed on the command line will be converted
to an integer.

``` text
@task
def inttask(n=123):
    print(n, type(n))

$ run inttask 33
33 <class 'int'>
```

### Counters

If an integer parameter is used but a value is not provided, the parameter is treated as a
*counter* and is incremented.  This makes it easy to implement things like verbosity counters:

``` text
@task
def counter(verbosity=0):
    print(verbosity)

$ run counter --verbosity
1

$ run counter -vvv
3
```

### Short Names

Arguments can also be provided using a single dash and the first letter of the parameter name,
as long as the first letter is unique.

    @task
    def sometask(arg1=None, flag=False):
        print('arg1={} flag={}'.format(arg1, flag))

    $ run sometask -a value1
    arg1=value1 flag=False

    $ run sometask -a=value1
    arg1=value1 flag=False

    $ run sometask -f
    arg1=None flag=True

    $ run sometask -fa=value1
    arg1=value1 flag=True

    $ run sometask -fa value1
    arg1=value1 flag=True

You can override the character assigned to a parameter using the task decorator, which is
particularly handy when the first letters are not unique.

    @task(flags={'x': 'flag'})
    def sometask(flag=False, forward=False):
        print('flag={} forward={}'.format(flag, forward))

    $ run sometask
    flag=False forward=False

    $ run sometask -x
    flag=True forward=False

    $ run sometask -f
    flag=False forward=True

    $ run sometask -fx
    flag=True forward=True

Notice that "f" is assigned to the "forward" parameter since it is the only remaining parameter
that starts with "f" now that "flag" is assigned to "x".

## Rationale

The distutils package is great for packaging, but in the past I'd also used it for defining a
myriad of per-project utility scripts (setup a test database, etc.).  I'd used distutils
because it was built-in, but, honestly, it's design is terrible, the command line parsing
always requires some option name with dashes, and it does bizarre things without telling you.
For example, if you define a user option named "user", it will be silently ignored when
running in a virtual environment!  (That was the last straw!)

All I really wanted was a single script I could invoke with command line parsing that "does
what I want".  I looked at many other packages but the only one close to this simplicity was
Invoke.  Unfortunately the configuration for Invoke was way to complicated for
me to figure out, particularly how to update the configuration in one task for later tasks to
use.

I also don't mind if some combinations are ambiguous.  Command line convenience is most
important here.
