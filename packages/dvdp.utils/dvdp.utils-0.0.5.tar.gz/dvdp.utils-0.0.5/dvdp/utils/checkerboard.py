import cv2
import numpy as np


def generate_checkerboard(
    square_sz,
    cols,
    rows,
):
    border = square_sz
    img_width = 2 * border + cols * square_sz
    img_height = 2 * border + rows * square_sz
    image = np.full((img_height, img_width), 255, dtype=np.uint8)
    for i_row in range(rows):
        fill = bool(i_row % 2)
        for i_col in range(cols):
            fill = not fill
            if fill:
                x_start = border + i_col * square_sz
                y_start = border + i_row * square_sz
                image[
                    y_start:y_start + square_sz,
                    x_start:x_start + square_sz,
                ] = 0
    return image


def generate_gradient(square_sz, nr_steps):
    border = square_sz
    img_width = 2 * border + nr_steps * square_sz
    img_height = 2 * border + square_sz
    image = np.full((img_height, img_width), 255, dtype=np.uint8)
    increment = 255 / (nr_steps - 1)
    for i_col in range(nr_steps):
        x_start = border + i_col * square_sz
        y_start = border
        image[
            y_start:y_start + square_sz,
            x_start:x_start + square_sz,
        ] = int(i_col * increment)
    return image


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'output',
        help='where should we write the checkerboard to?',
    )
    parser.add_argument(
        '--size',
        '-s',
        help='single square size in pixels',
        required=True,
        type=int,
    )
    parser.add_argument(
        '--rows',
        '-r',
        help='nr of rows of checkers',
        required=True,
        type=int,
    )
    parser.add_argument(
        '--columns',
        '-c',
        help='nr of columns of checkers',
        required=True,
        type=int,
    )
    args = parser.parse_args()
    checker_board = generate_checkerboard(
        args.size,
        args.columns,
        args.rows,
    )
    gradient = generate_gradient(args.size, args.columns)
    image = np.vstack([
        checker_board[:-args.size, :],
        gradient[args.size:, :]
    ])

    cv2.imwrite(args.output, image)
    print(f'Wrote file to {args.output}.')


if __name__ == '__main__':
    main()
