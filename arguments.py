import argparse


def parser():
    parser = argparse.ArgumentParser(description='Some hyperparameters')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    parser.add_argument('--start', metavar='S', type=int, default=1,
                        help='start number of song\'s ID')
    parser.add_argument('--end', metavar='E', type=int, default=10,
                        help='end number of song\'s ID')

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parser()
    print(args)
