# Sudoku board extractor + solver

## Extractor
The board extractor tries to read a sudoku board from an image.

It does some simple image processing, mosty threshold and crop, to extract the board from the rest of the image.

Then AWS Rekognition is used to detect digits in the image, and map them to X and Y positions in a sudoku board data structure.

## Solver
The solver tries to find a solution to a given sudoku board.

It was inspired by Thorsten Altenkirch's solution on the Computerphile channel:
https://www.youtube.com/watch?v=G_UYXzGuqvM

## Tests
The tests in `test_sudoku_board_extractor.py` use AWS S3 and Rekognition.

To run the tests make sure to setup an S3 bucket and set the environment variable `IMAGE_BUCKET` to the name of the bucket.
