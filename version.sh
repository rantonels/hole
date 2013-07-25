#!/bin/bash

rm hole_release/* -rv

cp -v dMap.py hole_release/dMap.py
cp -v hole hole_release/hole.$1
cp -v playersguide.txt hole_release/playersguide.txt
cp -v title hole_release/title
cp -v final hole_release/final
cp -v vending hole_release/vending
