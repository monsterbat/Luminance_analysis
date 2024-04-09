# -*- coding: utf-8 -*-
"""
Project: *****
Version 3.8.2
Generated for *** to facilitate future data plotting using a consistent color map.  
Released by *****
Release date: 2022/07/22
Authored by *** 
Revise by SC.siao
"""

# -*- import -*-
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
import re
from xlwt import Workbook
from pathlib import Path
import cv2
import json

# -*- Window -*-
window = tk.Tk()
window.title('CCD image generate ver 3.8.2')  # Title
window.geometry('300x160')  # Window size

# -*- Operation -*-
# Data process＋
# //Image cropping
def croping_data(data):
    cropping_scale=0.3
    data_x_shape=data.shape[1]
    data_y_shape=data.shape[0]
    data_mid_for_y=round(data.shape[1]/2)
    data_mid_for_x=round(data.shape[0]/2)

    # find mid raw and column
    data_xaxis=data.iloc[int(data_mid_for_x),:]
    data_xaxis_reverse=data_xaxis[::-1]
    data_yaxis=data.iloc[:,int(data_mid_for_y)]
    data_yaxis_reverse=data_yaxis[::-1]

    # find center point value
    x_mid_position=int(round((data.shape[1]-1)/2))
    y_mid_position=int(round(data.shape[0]/2-1))
    center_radius=10
    x_center_choose_star=x_mid_position-1-center_radius
    x_center_choose_end=x_mid_position+center_radius

    y_center_choose_star=y_mid_position+1-center_radius
    y_center_choose_end=y_mid_position+2+center_radius

    data_matrix=data.iloc[y_center_choose_star:y_center_choose_end,x_center_choose_star:x_center_choose_end]
    center_area_value=np.average(data_matrix)
    # set up bounding condition
    boundary_condition=center_area_value*cropping_scale

    x_left_edge=0
    for find_x_left_edge in data_xaxis:
        if find_x_left_edge<boundary_condition:
            x_left_edge=x_left_edge+1
        else:
            x_left_edge_value=x_left_edge
    x_right_edge=1
    for find_x_right_edge in data_xaxis_reverse:
        if find_x_right_edge<boundary_condition:
            x_right_edge=x_right_edge+1
        else:
            x_right_edge_value=x_right_edge 
         
    x_right_edge_value=data_x_shape-x_right_edge_value

    y_top_edge=0
    for find_y_top_edge in data_yaxis:
        if find_y_top_edge<boundary_condition:
            y_top_edge=y_top_edge+1
        else:
            y_top_edge_value=y_top_edge
    y_down_edge=1
    for find_y_down_edge in data_yaxis_reverse:
        if find_y_down_edge<boundary_condition:
            y_down_edge=y_down_edge+1
        else:
            y_down_edge_value=y_down_edge      
    y_down_edge_value=data_y_shape-y_down_edge_value

    data=data.iloc[y_top_edge_value:y_down_edge_value,x_left_edge_value:x_right_edge_value]
    return data

# //Yield data
def data_yield(file_choose):
    for file_process_x in file_choose:
        data = pd.read_csv(file_process_x, delimiter="\t", header=8)
        data = data.dropna(axis=1, how='all')        
        data=croping_data(data)
        data=[data,file_process_x]
        yield data

# Data generate
# --> Luminance Plot (All)
def Luminance_plot(chosen_cmap):
    file_choose = filedialog.askopenfilenames(title=u'Choose file', initialdir=(os.path.expanduser('H:/')))
    file_choose_data=data_yield(file_choose)
    # Color Map Chosen
    if chosen_cmap in ["cm_data_parula", "false_color_map"]:
        chosen_cmap_name = chosen_cmap
        json_file_path = os.path.join("cmap", f"{chosen_cmap}.json")
        try:
            with open(json_file_path, 'r') as file:
                chosen_cmap_data = json.load(file)
                
                print(chosen_cmap)
        except FileNotFoundError:
            print(f"File Missing : {json_file_path}")
        except json.JSONDecodeError:
            print("Failed to parse JSON file")
        chosen_cmap_data = LinearSegmentedColormap.from_list(f"{chosen_cmap_name}", chosen_cmap_data)
    else :
        chosen_cmap_data=plt.get_cmap(f"{chosen_cmap}")

    # Process
    for file_data_process in file_choose_data:
        file_data=file_data_process[0]
        file_name=file_data_process[1]
        plt.figure()
        ax = plt.gca()
        im = plt.imshow(file_data, cmap=chosen_cmap_data)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        saving_file = re.sub("\.txt","_Parula",file_name)
        file_saving_path = saving_file
        plt.savefig(file_saving_path, dpi=400)

        # --Clean RAM --#
        del file_data_process
        del file_name
        del file_data
        del im
        del cax
        del saving_file
        plt.clf()
        plt.close()
        plt.close('all')
        
    print("Finish!!!")
   
# --> Calculate center point
def calculate_center_point():
    file_choose = filedialog.askopenfilenames(title=u'Choose file', initialdir=(os.path.expanduser('H:/')))
    wb=Workbook()
    center_point_sheet = wb.add_sheet('Center Point')
    center_point_sheet.write(0, 0, "File name")
    center_point_sheet.write(0, 1, "Center Point")
    cp_excel_position=0
    for file_CP_process_x in file_choose:
        data=pd.read_csv(file_CP_process_x, delimiter="\t", header=8)
        data = data.dropna(axis=1, how='all')
        data=croping_data(data)
        x_mid_position=int(round((data.shape[1]-1)/2))
        y_mid_position=int(round(data.shape[0]/2-1))
        data_mid=data.iloc[int(y_mid_position),int(x_mid_position)]
       
        # choose radius value
        center_radius=44
        # calculate radius value
        # x
        x_center_choose_star=x_mid_position-1-center_radius
        x_center_choose_end=x_mid_position+center_radius
        # y
        y_center_choose_star=y_mid_position+1-center_radius
        y_center_choose_end=y_mid_position+2+center_radius

        # calculate
        data_matrix=data.iloc[y_center_choose_star:y_center_choose_end,x_center_choose_star:x_center_choose_end]
        cenper_point=np.average(data_matrix)
        saving_file_name = re.sub("\ .txt","",file_CP_process_x)
        saving_file_name=Path(saving_file_name).stem

        # item_name=saving_file_name
        cp_excel_position=cp_excel_position+1
        center_point_sheet.write(cp_excel_position, 0, saving_file_name)
        center_point_sheet.write(cp_excel_position, 1, cenper_point)

    CP_saving_name=filedialog.asksaveasfilename(title=u'save file', initialdir=(os.path.expanduser('H:/')))
    CP_saving_name=CP_saving_name+".xls"
    wb.save(CP_saving_name)
    print("Finish!!!")

# --> Cropping img for report
def image_crop():
    file_choose = filedialog.askopenfilenames(title=u'Choose file', initialdir=(os.path.expanduser('H:/')))
    for file_process_x in file_choose:
        img=cv2.imread(file_process_x)
        y=322
        x=446
        h=y+1866
        w=x+1048
        crop_image = img[x:w, y:h]
        saving_file = re.sub("\.txt","",file_process_x)
        saving_file = re.sub(".png","_Crop.png",saving_file)
        file_saving_path = saving_file
        cv2.imwrite(file_saving_path, crop_image)
    print("Finish!!!")

# -*- Buttom -*-
bt1 = tk.Button(window, text='Luminance Plot (Parula)', command=lambda: Luminance_plot("cm_data_parula"))
bt1.pack()
bt2 = tk.Button(window, text='Luminance Plot (False color)', command=lambda: Luminance_plot("false_color_map"))
bt2.pack()
bt3 = tk.Button(window, text='Luminance Plot (Gray color)', command=lambda: Luminance_plot("gray"))
bt3.pack()
bt4 = tk.Button(window, text='Calculate Center Point', command=calculate_center_point)
bt4.pack()
bt5 = tk.Button(window, text='Image cropping (no color bar)', command=image_crop)
bt5.pack()
window.mainloop()