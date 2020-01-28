#!/usr/bin/env bash

function create() {
    cd
    python create.py $1
    cd /Users/rohandeshmukh/Desktop/Rohan/Study/PProjects
    mkdir $1
	echo $1
}