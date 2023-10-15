#!/bin/bash
DATABASE=(
%%DATABASE%%
)
declare -i maxline minline
maxline=${#DATABASE[@]}
minline=0
rand=$((RANDOM % ($maxline - $minline) + $minline))
echo -e "${DATABASE[$rand]}"
