#! /bin/bash

echo "Running CI checks..."
TMPLOG=$(mktemp)

# An array of commands
# The first element is the command to run
# The second element is the message to display
# The third element is the log file to write to
# The fourth element is the exit code to expect
# The fifth element is the command to run if the exit code is not as expected
# The sixth element is the message to display if the exit code is not as expected
# The seventh element is the log file to write to if the exit code is not as expected
# The eighth element is the exit code to expect from the command to run if the exit code is not as expected
# The ninth element is the command to run if the exit code is not as expected
# The tenth element is the message to display if the exit code is not as expected
# The eleventh element is the log file to write to if the exit code is not as expected
# The twelfth element is the exit code to expect from the command to run if the exit code is not as expected


echo -ne "ruff check:\t"
uv run ruff check . 2> $TMPLOG
if [ $? -ne 0 ]; then
    echo -e "Ruff check failed:\n"
    cat $TMPLOG
    exit 1
fi

echo -ne "ruff format:\t"
uv run ruff format --diff . 2> $TMPLOG
if [ $? -ne 0 ]; then
    echo -e "Ruff check failed:\n"
    cat $TMPLOG
    exit 1
else
    echo "No formatting issues found."
fi

echo -ne "mypy:\t\t"
uv run mypy . 2> $TMPLOG
if [ $? -ne 0 ]; then
    echo -e "Mypy failed:\n"
    cat $TMPLOG
    exit 1
fi

echo -ne "deptry:\t\t"
uv run deptry . 2> /tmp/deptry
if [ $? -ne 0 ]; then
    echo -e "Deptry failed:\n"
    cat /tmp/deptry
    exit 1
else
    echo "No dependency issues found."
fi

# Run pytest for all supported Python versions
for PYVER in 3.11 3.12 3.13; do
    #redirect both stdout and stderr to a file
    echo -ne "pytest $PYVER:\t"
    uv run -p $PYVER pytest  > $TMPLOG 2>&1
    if [ $? -ne 0 ]; then
        echo -e "Pytest failed for Python $PYVER:\n"
        cat $TMPLOG
        exit 1
    else
        echo "All tests passed."
    fi
done
