import os
import sys


def main():
    print('Env:')
    for k, v in os.environ.items():
        print(f'{k}={v}')

    print()

    print('Args:')
    for arg in sys.argv:
        print(arg)

    print()
