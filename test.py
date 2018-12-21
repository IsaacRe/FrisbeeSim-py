#import sys, traceback, pdb
import argparse

import matplotlib.pyplot as plt
import tensorflow as tf
from disc import Disc, simple_trajectory

TICK_TIME = 0.1


def test_disc(pos, angles, veloc):
    print("Starting simulation...")

    disc = Disc(TICK_TIME)

    disc.begin_flight(pos, angles, veloc)
    x_coords, y_coords = [], []

    while disc.y > 0.0:
        disc.update_flight()
        x_coords += [disc.x]
        y_coords += [disc.y]
    plt.plot(x_coords, y_coords)
    plt.show()


def test_simple_disc(distance):
    with tf.Session() as sess:
        y = 1
        t = 0.0
        x_coords, y_coords = [], []

        while y > 0:
            x, y = simple_trajectory(t, distance)
            t += TICK_TIME
            x_coords += [x]
            y_coords += [y]
        plt.plot(x_coords, y_coords)
        plt.ylim(0, max(x_coords))
        plt.show()


if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--simple', action='store_true',
                        help='Test simple trajectory approximation')

    # test params for Disc
    parser.add_argument('--veloc_x', type=float, default=14.0,
                        help='The initial forward velocity of the disc')
    parser.add_argument('--veloc_y', type=float, default=2.0,
                        help='The initial upward velocity of the disc')
    parser.add_argument('--direction', type=float, default=0.0,
                        help='The xz direction (in radians) in which the frisbee is thrown')
    parser.add_argument('--tilt', type=float, default=7,
                        help='The upward tilt (in degrees) of the frisbee on release')

    # test params for SimpleDisc
    parser.add_argument('--distance', type=float, default=20.0,
                        help='Distance of disc flight')

    args = parser.parse_args()

    assert args.tilt > 0.0 and args.tilt < 90.0

    if args.simple:
        test_simple_disc(args.distance)
    else:
        test_disc([0.0, 1.0, 0.0], [args.direction, args.tilt], [args.veloc_x, args.veloc_y])

    """
    try:
        game = GameManager()
        game.test([0.0, 5.0, 0.0], [args.direction, args.tilt], [args.veloc_x, args.veloc_y])

    except:
        typ, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
    """
