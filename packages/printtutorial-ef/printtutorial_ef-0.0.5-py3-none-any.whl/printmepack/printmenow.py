#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 14:29:24 2021

@author: eduard
"""
import pandas as pd
import sys




def print_HALLO():
    print("Hello from print me now")
    
def print_HALLO_2():
    print("Hello from print me now 2")    
    
def print_HALLO_3():
    print("Hello from print me now 3")     
    
def print_HALLO_pandas():
    print(f"Hello, used pandas version = {pd.__version__}")   
    
def print_sys_infos():
    print(f"Hello, sys.path = {sys.path}")      
    
print_sys_infos( ) 