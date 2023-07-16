# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 22:41:49 2023

@author: ppare
"""
import os


source_folder = "C:/data1"
for filename in os.listdir(source_folder):
    if filename.endswith(".csv"):
        new_filename = os.path.splitext(filename)[0] + ".txt"
        old_filepath = os.path.join(source_folder, filename)
        new_filepath = os.path.join(source_folder, new_filename)
        os.rename(old_filepath, new_filepath)
        print(f"Changed extension: {filename} -> {new_filename}")