#!/usr/bin/env python3

import argparse
import importlib


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("day", help="number of the day to run", type=int)
    args = parser.parse_args()
    print(f"Run day {args.day}")
    day_main_module = importlib.import_module(f"src.day_{args.day}.main")
    day_main_module.main()
