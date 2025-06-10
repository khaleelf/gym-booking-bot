#!/usr/bin/python3

from gym_booker import book_class
from ics_generator import update_calendar


def main():
    date = book_class() # 2025-06-17 18:30
    update_calendar(date)


if __name__ == "__main__":
    main()
