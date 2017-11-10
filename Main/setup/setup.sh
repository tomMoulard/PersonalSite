#!/bin/bash

#To use:
# curl http://tom.moulard.org/setup/setup.sh | bash

if [ "$HOME/.bashrc" ]
then
    #put git:bashrc > .bashrc
    curl https://raw.githubusercontent.com/tomMoulard/configLoader/master/bashrc > $HOME/.bashrc
    echo "Bashrc imported!"
    #put git:alias > .aliases
    curl https://raw.githubusercontent.com/tomMoulard/configLoader/master/aliases >> $HOME/.bashrc
    echo "Aliases imported!"
    source $HOME/.bashrc

    echo Done!
elif [ "$HOME/.zshrc" ]
then
    echo zshrc
else
    echo not recognized
fi
