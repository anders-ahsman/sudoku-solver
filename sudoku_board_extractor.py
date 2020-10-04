#!/usr/bin/env python

import os
import sys
from tempfile import gettempdir
from typing import Dict, List, Tuple

import boto3
import cv2 as cv
import numpy as np

from common import Board


Detections = List[Dict]

IMAGE_BUCKET: str = os.getenv('IMAGE_BUCKET', '')


def extract_sudoku_board(img_filename: str) -> Board:
    if not IMAGE_BUCKET:
        raise Exception('Environment variable IMAGE_BUCKET not set.')

    img_cropped_filename_with_path, img_cropped_filename = _apply_threshold_and_crop_image(img_filename)
    _upload_image_to_s3(img_cropped_filename_with_path, img_cropped_filename, IMAGE_BUCKET)
    detections: Detections = _get_detections_from_rekognition(img_cropped_filename, IMAGE_BUCKET)
    board: Board = _get_board_from_detections(detections)
    return board


def _apply_threshold_and_crop_image(img_filename: str) -> Tuple[str, str]:
    img = cv.imread(img_filename)
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    img = cv.GaussianBlur(img, (3, 3), 0)
    _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    img = cv.bitwise_not(img)

    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contour_areas = [cv.contourArea(c) for c in contours]
    max_contour_area_idx = max(range(len(contour_areas)), key=contour_areas.__getitem__)
    max_area_contour = [contours[max_contour_area_idx]]

    x_min, y_min = np.amin(max_area_contour, axis=1)[0][0]
    x_max, y_max = np.amax(max_area_contour, axis=1)[0][0]
    img_cropped = img[y_min:y_max, x_min:x_max]

    _, img_filename_tail = os.path.split(img_filename)
    img_cropped_filename = f'{os.path.splitext(img_filename_tail)[0]}.png'
    img_cropped_filename_with_path = f'{gettempdir()}/{img_cropped_filename}'
    cv.imwrite(img_cropped_filename_with_path, img_cropped)

    return img_cropped_filename_with_path, img_cropped_filename


def _upload_image_to_s3(img_filename_with_path: str, img_filename: str, bucket: str):
    s3 = boto3.client('s3')
    s3.upload_file(img_filename_with_path, bucket, img_filename)


def _get_detections_from_rekognition(img_filename: str, bucket: str) -> Detections:
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': img_filename}})
    detections: Detections = response['TextDetections']
    return detections


def _get_board_from_detections(detections: Detections) -> Board:
    board: Board = [[0] * 9 for _ in range(9)]

    digits = [str(n) for n in range(1, 10)]
    for d in detections:
        if d['Type'] == 'WORD':
            if d['DetectedText'] == 'l':
                d['DetectedText'] = '1'
            if d['DetectedText'] in digits:
                bb = d['Geometry']['BoundingBox']
                bb_center_x = bb['Left'] + bb['Width'] / 2
                bb_center_y = bb['Top'] + bb['Height'] / 2
                board[int(bb_center_y * 9)][int(bb_center_x * 9)] = int(d['DetectedText'])

    return board


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {__file__} [image filename]')
        exit(1)

    img_filename = sys.argv[1]
    board: Board = extract_sudoku_board(img_filename)
    for row in board:
        print(row)
