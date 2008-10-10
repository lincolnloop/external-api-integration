Requires `elementtree` and `httplib2`

#. Drop your Basecamp info into the script
#. Create a message in Basecamp (make sure your user entered above has access to the message)
#. Note the message ID from the URL (it's the second number)
#. Create a post-commit hook on your subversion repo that calls this script

::

    #! /bin/sh
    BASECAMP_MESSAGE=11111111
    # $1 is the repository path
    # $2 is the revision
    python /path/to/subversion_basecamp_notifier.py $1 $2 $BASECAMP_MESSAGE
