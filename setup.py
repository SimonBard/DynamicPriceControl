#!/usr/bin/python
import lib.manager


def main():
    setup()

if __name__ == "__main__":
    main()

def setup()-> None:
    
    dbmanager = lib.manager.Manager()
    dbmanager.create_tables()