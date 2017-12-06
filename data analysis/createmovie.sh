#!/bin/bash

python3 matrixplot.py
cd ../Results/grid_animation

filename+="animation"$(date +"%T")
filename+=".mp4"

convert -delay 20 -loop 0 *png $filename
