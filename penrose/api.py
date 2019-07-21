from penrose import (util,)

def panic(**kwargs):
    """ stop all engines """
    util.invoke(cmd=("ps aux "
                     "| grep -i houdini "
                     "| grep -v grep "
                     "| awk '{print $2}'  "
                     "| xargs -n1 -I% kill -KILL % "
                     "|| true"), system=True)
