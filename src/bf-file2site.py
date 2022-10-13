"""bf-file2site.py - A utility to upload a file to a BigFix
site via the REST API"""
import argparse

# The following is just for warning suppression
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# end of warning suppression

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--bfserver", type=str, help="BigFix REST Server name/IP address"
    )
    parser.add_argument(
        "-p", "--bfport", type=int, help="BigFix Port number (default 52311)", default=52311
    )
    parser.add_argument("-U", "--bfuser", type=str, help="BigFix Console/REST User name")
    parser.add_argument("-P", "--bfpass", type=str, help="BigFix Console/REST Password")
    pass

# Convention for possible future module/import
if __name__ == "__main__":
    main()
    exit(0)

