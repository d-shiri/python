#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 9 | 23:58:44 2022

@author: dariyoush shiri

"""
import os
import time


def progress(i, n) -> None:
    '''
    Simple progress bar that adjust to the terminal window

    Parameters
    ----------
    i : int
        single steps that program takes (e.g., in a for loop)
    n : int
        Total number of steps
    '''
    row, _ = os.get_terminal_size()
    row = row - 8
    percent = (i +1) / n
    done = int(percent * row)
    remain = int(row-done)
    #print(f"Remaining: {remain} | Done: {done}", end='\r')
    bar = '\033[31m\033[01m{}\033[0m'.format('━'*done) + '┄'*remain
    print(f"\r{bar}{percent*100:.2f}%", end='\r')

#NOTE: Example
for i in range(1, 20):
    time.sleep(.1)
    progress(i, 20)
print()
