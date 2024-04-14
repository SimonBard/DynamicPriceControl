# This routine should run every minute 

import lib.manager
import lib.heatpump
from datetime import datetime, timedelta
import lib.battery
from requests import get
import json
import lib.ha_connection
import lib.telegram


def main():
    inst = lib.manager.Manager()
    inst.write_counter(3)

if __name__ == "__main__":
    main()
 