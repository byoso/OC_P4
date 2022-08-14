#! /usr/bin/env python3
# coding: utf-8


"""Simple lanceur qui appèle la facade du programme"""


from prg.facade import Facade


if __name__ == "__main__":
    try:
        Facade()
    except KeyboardInterrupt:
        print("\nArret volontaire du programme.")
