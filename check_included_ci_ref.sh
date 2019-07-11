# check reference of included gitlab-ci files
# ref_check()
# {
if [ -f .gitlab-ci.yml ]; then
  REFS=$(grep -i -E "ref[ ]*:" .gitlab-ci.yml)
  CLEANED=$(echo "$REFS" | while read -r line;do echo "$line" | cut -d ":" -f 2 | tr -d " "  ;done | sort | uniq)
  BRANCH=$(git rev-parse --abbrev-ref HEAD)

  RESULT=""
  if [ "$BRANCH" = "master" ]; then
    # allow master ref only
    RESULT=$(echo "$CLEANED" | grep -v "master")
  elif [ "$BRANCH" = "staging" ]; then
    # allow master and staging refs only
    RESULT=$(echo "$CLEANED" | grep -v -E "master|staging")
  fi

  if [ -n "$RESULT" ]; then
    # found refs different from allowed ones
    echo "\e[31mWarning: NOT COMMITTING CHANGES:\e[39m"
    echo "----------------------"
    echo "  Committing on $BRANCH"
    WRONG=$(echo "$RESULT" | tr "\n" " ")
    echo "  Found ref(s): \e[31m$WRONG\e[39m"
    # Assign tty to accept user input
    read -p "Are you sure that is what you want to do? [y/N] " sayyes < /dev/tty
    if [ "${sayyes}" != "y" ]; then
        exit 1
    fi
  fi
fi
# }

# ref_check
