#!/usr/bin/python
import lib.manager


def setup()-> None:
    
    dbmanager = lib.manager.Manager()
    dbmanager.drop_tables
    dbmanager.create_tables()
    
def main():
    setup()

if __name__ == "__main__":
    main()