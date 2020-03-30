from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from todo import get_todos
from pprint import pprint
import os, re, datetime, argparse

horizontalline = '-------------------------------------------------------------------------------------------------'

def mark_done(project='base', done=None):
    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    if project == 'base':
        notes_path = os.getenv('notes')

    if done is None:
        matches = get_todos(notes_path)
        choices = [Separator('= TODO =')]
        for match in matches:
            choices.append({'name': match.get('task')})
        questions = [
            {
                'type': 'checkbox',
                'message': 'Select complete task',
                'name': 'tasks',
                'choices': choices,
                'validate': lambda answer: 'You must complete at least 1 task' \
                    if len(answer) == 0 else True
            }
        ]

        answers = prompt(questions, style=style)

        for answer in answers['tasks']:
            for match in matches:
                if answer == match['task']:
                    updated_task = match['task'].replace('#TODO[ ]:', '#TODO[X]:')
                    with open(match['filepath'], 'r') as handle:
                        lines = handle.readlines()
                    with open(match['filepath'], 'w') as handle:
                        for line in lines:
                            if match['task'] in line:
                                handle.write(updated_task + '\n')
                            else:
                                handle.write(line)
                        print('Updated {}'.format(match['filepath']))
                    


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='manage todo lists')
    mark_done()

##---------------------------------------------------------------------------------------------------------
##                                   TODO
##---------------------------------------------------------------------------------------------------------
#base.todo () {
#        project=$1
#        if [[ $project == "base" ]];
#        then
#            notes_path=$notes
#        else
#            notes_path=$work/$project/notes/
#        fi
#        if [[ $# -lt 2 ]];
#        then
#                echo $HORIZONTALLINE
#                x=1
#                grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} "#TODO\[ \]" $notes_path/* -r -h | while read -r line; do
#                    task=$(basename "$line")
#                    tasks[$x]=$task
#                    echo "$x $line"
#                    x=$(( $x + 1 ))
#                done
#                echo $HORIZONTALLINE
#                return 0
#        else
#                todo="${@:2}"
#                year=`date +'%Y'`
#                month=`date +'%m'`
#                day=`date +'%d'`
#                note_dir=$notes_path/$year/$month
#                note_path=$note_dir/$day.md
#                if [ ! -f $note_path ]; then
#                    mkdir -p $note_dir
#                    touch $note_path
#                    printf "$day-$month-$year\n---\n\n" > $note_path
#                    printf "Created new note: $note_path\n"
#                else
#                    printf "Note \"$note_path\" already exists. Saving changes to existing file.\n"
#                echo "#TODO[ ]: $todo" >> $note_path
#                return 0
#    fi
#        fi
#}
#
#todo () {
#    base.todo "base" "$@"
#}
#
#dom.todo () {
#    base.todo "dom" "$@"
#}
#
#stor.todo () {
#    base.todo "stor" "$@"
#}
#
#ship.todo () {
#    base.todo "ship" "$@"
#}
#
#viz.todo () {
#    base.todo "viz" "$@"
#}
#
##--------------------------------------------------------------------------------------------------------
##                                   MARK_DONE
##--------------------------------------------------------------------------------------------------------
#base.mark_done() {
#    # List todo's with a number to select
#    base.todo $1
#    # Already passed the numbers of what is done, just make them complete
#    if [[ $# -gt 1 ]];
#    then
#        tasknums=${@:2}
#    else
#        echo "Which task(s) are complete?"
#        read -r tasknum
#    fi
##        read -r tasknums
##    fi
##    for tasknum in ${tasknums[@]};
##    do
##        echo $tasknum
#        done_task=$tasks[$tasknum]
#        marked_done_task=$(update_todo "$done_task")
#        escaped_task=$(escape_todo "$done_task")
#        # Mark the item as complete
#        LC_ALL=C find $notes_path -type f -exec sed -i "" "s/$escaped_task/$marked_done_task/" {} \;
##    done
#    return 0
#}
#
#mark_done () {
#    base.mark_done "base" "$@"
#}
#
#dom.mark_done () {
#    base.mark_done "dom" "$@"
#}
#
#stor.mark_done () {
#    base.mark_done "stor" "$@"
#}
#
#ship.mark_done () {
#    base.mark_done "ship" "$@"
#}
#
#viz.mark_done () {
#    base.mark_done "viz" "$@"
#}
#
##---------------------------------------------------------------------------------------------------------
##                                   LIST_DONE 
##---------------------------------------------------------------------------------------------------------
#
#list_done() {
#    grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} "#TODO\[X\]" $notes/* -r -h
#    return 0
#}
#
#base.list_done () {
#    project=$1
#    if [[ $project == "base" ]];
#    then
#        notes_path=$notes
#    else
#        notes_path=$work/$project/notes/
#    fi
#    grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} "#TODO\[X\]" $notes_path* -r -h
#    return 0
#}
#
#list_done() {
#    base.list_done "base" $@
#}
#
#dom.list_done () {
#    base.list_done "dom" $@
#}
#
#stor.list_done () {
#    base.list_done "stor" $@
#}
#
#ship.list_done () {
#    base.list_done "ship" $@
#}
#
#viz.list_done () {
#    base.list_done "viz" $@
#}
#
## Easily extract local ip address
#printip() { (awk '{print $2}' <(ifconfig en0 | grep 'inet ')); }
#
## Use lf to switch directories and bind it to ctrl-o
#lfcd () {
#    tmp="$(mktemp)"
#    lf -last-dir-path="$tmp" "$@"
#    if [ -f "$tmp" ]; then
#        dir="$(cat "$tmp")"
#        rm -f "$tmp"
#        [ -d "$dir" ] && [ "$dir" != "$(pwd)" ] && cd "$dir"
#    fi
#}
#bindkey -s '^o' 'lfcd\n'