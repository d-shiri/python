#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 9 | 23:58:44 2022

@author: dariyoush shiri

"""
import os

# Get the resolution of the terminal window
row, _ = os.get_terminal_size()

def progress(progress, n, count=[0]) -> None:
    '''
    Simple progress bar that adjust to the terminal window

    Parameters
    ----------
    progress : int
        single steps that program takes (e.g., in a for loop)
    n : int
        Total number of steps
    count : list, optional
        by default [0]
    '''
    
    count[0] += 1
    perc = (count[0] *(100 / float(n)))
    prog = int((perc*(row/1.5))/100)
    bar = '\033[31m\033[01m{}\033[0m'.format('━'*prog) + '┄'* int((row/1.5)-prog)
    print(f"\r{bar} {perc:.2f}%", end='\r')

#NOTE: Example
for i in range(100, 222):
    time.sleep(.1)
    progress(i, 122)
print()