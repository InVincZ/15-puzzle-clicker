from __future__ import print_function
from PIL import Image
from PIL import ImageGrab
from random import randint
import os
import time
import pyautogui
import math
from random import randint, uniform
import pyscreeze
import cv2
import numpy as np
import argparse
import imutils
import glob
import psutil
import sys
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
from resizeimage import resizeimage
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)

ProcessXlength = 0
ProcessYheight = 0
solution = 'C:\\Users\\Michael\\Documents\\Projects\\usr\\bin\\python\\8-Puzzle\\15-puzzle-clicker\\images\\Zauberpuzzle_Loesung.png'
# puzzle = 'C:\\Users\\Michael\\Documents\\Projects\\usr\\bin\\python\\8-Puzzle\\puzzle4.png'

def Resize_Image(file):
    with open(file, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [120, 120])
            # filename = file.split('\\')
            # filename = filename[-1].split('.')
            cover.save(file, image.format)

def fullscreenGrab():
    global puzzle_filename
    rect256 = getRectAsImage((3840, 590, 5760, 1670))
    puzzle_filename = 'C:\\Users\\Michael\\Documents\\Projects\\usr\\bin\\python\\8-Puzzle\\15-puzzle-clicker\\puzzle_' + time.strftime("%Y%m%d-%H%M%S") + '.png'
    # rect256.save(puzzle_filename, format='png')
    # img = Image.open(puzzle_filename)
    puzzle = rect256.crop((1650, 175, 1778, 303))
    puzzle.save(puzzle_filename)

def relX(rel_value):
    X_point = int(round(ProcessXlength * rel_value))
    return X_point

def relY(rel_value):
    Y_point = int(round(ProcessYheight * rel_value))
    return Y_point

def PrepareWindow():
    global first_row
    global second_row
    global third_row
    global fourth_row
    global file
    global ProcessXlength
    global ProcessYheight

    first_row = {'pos1': (relX(0.125), relY(0.125)), 'pos2': (relX(0.375), relY(0.125)), 'pos3': (relX(0.625), relY(0.125)), 'pos4': (relX(0.875), relY(0.125))}
    second_row = {'pos1': (relX(0.125), relY(0.375)), 'pos2': (relX(0.375), relY(0.375)), 'pos3': (relX(0.625), relY(0.375)), 'pos4': (relX(0.875), relY(0.375))}
    third_row = {'pos1': (relX(0.125), relY(0.625)), 'pos2': (relX(0.375), relY(0.625)), 'pos3': (relX(0.625), relY(0.625)), 'pos4': (relX(0.875), relY(0.625))}
    fourth_row = {'pos1': (relX(0.125), relY(0.875)), 'pos2': (relX(0.375), relY(0.875)), 'pos3': (relX(0.625), relY(0.875)), 'pos4': (relX(0.875), relY(0.875))}

    im = Image.open(solution)
    ProcessXlength, ProcessYheight = im.size

def CropTiles(file,sets,element,bool):
    PrepareWindow()
    # Opens a image in RGB mode
    im = Image.open(file)
    cord = eval(sets + "['" + element + "']")

    spotextension = 0.125
    X_conquest = int(round(float(ProcessXlength) * spotextension))
    Y_conquest = int(round(float(ProcessYheight) * spotextension))
    box = (cord[0] - X_conquest, cord[1] - Y_conquest, cord[0] + X_conquest, cord[1] + Y_conquest)

    im1 = im.crop(box)
    if bool == 1:
        im1.save(os.getcwd() + '\\images\\tileSnap_' + str(sets) + '_' + str(element) + '.png', 'PNG')
    else:
        im1.save(os.getcwd() + '\\images\\puzzleSnap_' + str(sets) + '_' + str(element) + '.png', 'PNG')
    # return im1

def Pos_to_Number(row,column):
    number = ((row * 4) + column) + 1
    if number == 16:
        number = 0
    return number

def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    s = ssim(imageA, imageB)
    return s

def main():
    print('15-PUZZLE SOLVER')
    print('--------------------------')
    print('Take screenshot, crop puzzle and start evaluating positions...\n')
    print('--------------------------')
    PrepareWindow()

    fullscreenGrab()
    im2 = Image.open(puzzle_filename)
    PuzzleXlength, PuzzleYheight = im2.size
    if PuzzleXlength != 120:
        Resize_Image(puzzle_filename)

    # solution_matrix = np.zeros((4,4))
    for i_index, i_name in enumerate(['first_row', 'second_row', 'third_row', 'fourth_row']):
        for j_index, j_name in enumerate(['pos1', 'pos2', 'pos3', 'pos4']):
            CropTiles(solution, i_name, j_name, 1) # Solution
            CropTiles(puzzle_filename, i_name, j_name, 0) # Puzzle

    puzzle_matrix = np.zeros((4,4))
    pos_list = []
    pos_blacklist = []
    score_max = 0
    row = 'None'
    column = 'None'
    # load the images -- the original, the original + contrast,
    # and the original + photoshop
    path = 'C:\\Users\\Michael\\Documents\\Projects\\usr\\bin\\python\\8-Puzzle\\15-puzzle-clicker\\images'

    for p_index, p_name in enumerate(['first_row', 'second_row', 'third_row', 'fourth_row']):
        for q_index, q_name in enumerate(['pos1', 'pos2', 'pos3', 'pos4']):
            tile = cv2.imread(path + '\\puzzleSnap_' + str(p_name) + '_' + str(q_name) + '.png')
            tile = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
            # print(p_index)
            # print(q_index)
            new_number = 0
            # Find best fitting position
            while new_number == 0:
                score_max = 0
                for f_index, f_name in enumerate(['first_row', 'second_row', 'third_row', 'fourth_row']):
                    for z_index, z_name in enumerate(['pos1', 'pos2', 'pos3', 'pos4']):
                        tileSnap = cv2.imread(path + '\\tileSnap_' + f_name + '_' + z_name + '.png')
                        tileSnap = cv2.cvtColor(tileSnap, cv2.COLOR_BGR2GRAY)
                        # print('f: ' + str(f_index) + ' z: ' + str(z_index))
                        # compare the images
                        score = compare_images(tile, tileSnap, "Solution vs. Puzzle")
                        if (score > score_max) and (Pos_to_Number(f_index,z_index) not in pos_blacklist):
                            score_max = score
                            row = f_index
                            column = z_index

                # print('Row: ' + str(row) + ' -- Column: ' + str(column) + ' -- Score: ' + str(score_max))
                if Pos_to_Number(row,column) not in pos_list:
                    pos_list.append(Pos_to_Number(row,column))
                    new_number = 1
                else:
                    pos_blacklist.append(Pos_to_Number(row,column))

                # print(pos_blacklist)
            puzzle_matrix[p_index][q_index] = Pos_to_Number(row,column)
    print('Extracted puzzle from file:\n')
    print(puzzle_matrix)
    val = 0
    starting_position = np.where(puzzle_matrix==0)
    starting_position = (starting_position[0][0], starting_position[1][0])
    # print(starting_position)
    return starting_position, tuple(list(map(int, puzzle_matrix.flatten())))

if __name__ == '__main__':
    main()
