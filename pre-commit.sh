# Ensure that code that isn't part of the prospective commit isn't tested
# within the pre-commit script using git stash.
# git stash -q --keep-index

# # Test prospective commit
# FILES_PATTERN='\.py(\..+)?$'
# FORBIDDEN_PATTERN='^[^#]*pdb.set_trace()'

# FORBIDDEN_FILES=`git diff --cached --name-only | \
#     grep -E $FILES_PATTERN | \
#     GREP_COLOR='4;5;37;41' xargs grep --color --with-filename -n \
#     -e $FORBIDDEN_PATTERN`


# [ -n "$FORBIDDEN_FILES" ] && echo "COMMIT REJECTED \n$FORBIDDEN_FILES"

# RETVAL=$?
# git stash pop -q

# [ $RETVAL -eq 1 ] && exit 0

FLAKE8_ERRORS=`flake8 --exclude assets,migrations,docs,.tox`
[ -n "$FLAKE8_ERRORS" ] && echo "COMMIT REJECTED \n$FLAKE8_ERRORS"

RETVAL=$?
[ $RETVAL -eq 1 ] && exit 0
