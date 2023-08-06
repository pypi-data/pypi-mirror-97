subc
====

This is a tiny library to help you write CLI applications with many
sub-commands.

Installation
------------

``pip install subc``

Use
---

Create your own command subclass for your application:


.. code:: python

    class MyCmd(subc.Command):
        pass

Then, write commands in your application which sub-class this:

.. code:: python

    class HelloWorld(MyCmd):
        name = 'hello-world'
        description = 'say hello'
        def run(self):
            print('hello world')

Finally, use your application-level subclass for creating the argument parser
and running your application:

.. code:: python

    if __name__ == '__main__':
        MyCmd.main('description of app')

Advanced Use
------------

Intermediate Base Classes
^^^^^^^^^^^^^^^^^^^^^^^^^

You may find yourself wanting to create intermediate subclasses for your
application, in order to share common functionality. For example, you might
create a class for all commands which handle a single file as an argument:

.. code:: python

    class FileCmd(MyCmd):
        def add_args(self, parser):
            parser.add_args('file', help='the single file')

You can do that, so long as your intermediate subclasses are not executable. For
example, given the following class hierarchy:

.. code::

    MyCmd*
    |- FileCmd*
    |  |- AppendLineCmd
    |  |- RemoveLineCmd
    |- DoSomethingElseCmd

The non-leaf commands (marked with an asterisk) will not be included as
executable commands. Only leaf classes will be executable.

Default Command
^^^^^^^^^^^^^^^

When the user does not provide any argument on the command-line, the default
action is to raise an Exception which states "you must select a sub-command".
You can provide a default command to run instead, via the ``default`` argument
to ``main()`` (or ``add_subcommands()``). For example:

.. code:: python

    if __name__ == '__main__':
        MyCmd.main('description', default='help')

The above code will run the ``help`` subcommand when no subcommand is specified.
Note that in this case, the default sub-command may not receive all of its
expected arguments.

Shortest Prefix Aliasing
^^^^^^^^^^^^^^^^^^^^^^^^

``subc`` has an optional feature which allows the user to specify a subcommand
by the shortest prefix which uniquely identifies the subcommand, or any longer
prefix thereof. As an example, imagine a git command with the following
sub-commands: clone, checkout, commit, cherry-pick. The shortest prefix aliasing
would allow you to run "git clone" by executing ``git cl``, since only "clone"
begins with "cl". You could also execute "git clone" with a longer prefix like
``git clo``. The feature can be enabled by setting ``shortest_prefix`` to true
in ``main()`` or ``add_subcommands()``.

License
-------

This project is released under the Revised BSD license.  See ``LICENSE.txt`` for
details.
