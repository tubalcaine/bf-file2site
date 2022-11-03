"""bf_file2site.py - A utility to upload a file to a BigFix
site via the REST API"""
from getpass import getpass
import sys
import os
import argparse
import requests
import keyring


# The following is just for warning suppression
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# end of warning suppression


def main():
    """main() Main routine"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--bfserver", type=str, help="BigFix REST Server name/IP address"
    )
    parser.add_argument(
        "-p",
        "--bfport",
        type=int,
        help="BigFix Port number (default 52311)",
        default=52311,
    )
    parser.add_argument(
        "-c", "--savecreds", type=str, help="Store credentials encrypted"
    )
    parser.add_argument("-k", "--keycreds", type=str, help="Use stored credentials")
    parser.add_argument(
        "-U", "--bfuser", type=str, help="BigFix Console/REST User name"
    )
    parser.add_argument(
        "-S",
        "--site",
        default="master",
        help="Site url, like custom/CustomSite. Default 'master'",
    )
    parser.add_argument("-P", "--bfpass", type=str, help="BigFix Console/REST Password")
    parser.add_argument("files", nargs="*", help="Files to upload")

    conf = parser.parse_args()

    # We will store the bigfix account password over this:
    bfpass = ""

    if conf.savecreds is not None:
        if conf.bfuser is None:
            print("You must specify a user name with --bfuser or -U.")
            sys.exit(1)

        ## We need to prompt for and save encrypted credentials
        onepass = "not"  # Set to ensure mismatch and avoid fail msg 1st time
        twopass = ""

        print(f"Enter the password for the user {conf.bfuser}")
        print("The password will not display. You must enter the same")
        print("password twice in a row. It will be stored encrypted")
        print(f"under the key name {conf.savecreds} in your system's")
        print("secure credential store. Use the command switches: ")
        print(f"-k {conf.savecreds} -U {conf.bfuser}    --OR--")
        print(f"--keycreds {conf.savecreds} --bfuser {conf.bfuser}")
        print("to run the program without having to provide the password")
        while onepass != twopass:
            if onepass != "not":
                print("\nPasswords did not match. Try again.\n")

            onepass = getpass(f"BigFix password for {conf.bfuser}: ")
            twopass = getpass("Enter the password again: ")

        keyring.set_password(conf.savecreds, conf.bfuser, onepass)
        sys.exit(0)

    # First, set bfpass to the provided command switch (if any)
    if conf.bfpass is not None:
        bfpass = conf.bfpass

    # If a keystore reference is provided, use that, overriding any
    # previous setting
    if conf.keycreds is not None:
        bfpass = keyring.get_password(conf.keycreds, conf.bfuser)

    ## Do the file POST iff the bigfix server is specified
    if conf.bfserver is not None:
        bf_sess = requests.Session()
        bf_sess.auth = (conf.bfuser, bfpass)

        for filename in conf.files:
            with open(filename, "rb") as file_handle:
                ram_copy = file_handle.read()

            print(f"Uploading file {filename} to {conf.site}\n")

            qheader = {"Content-Type": "application/x-www-form-urlencoded"}

            req = requests.Request(
                "POST",
                f"https://{conf.bfserver}:{conf.bfport}"
                + f"/api/site/{conf.site}/file/{os.path.basename(filename)}"
                + "?force=true&isClientFile=true",
                headers=qheader,
                data=ram_copy,
            )

            prepped = bf_sess.prepare_request(req)

            result = bf_sess.send(prepped, verify=False)

            if not result.ok:
                print(f"\n\nREST API call failed with status {result.status_code}")
                print(f"Reason: {result.text}")
                sys.exit(1)
            else:
                print(f"File [{filename}] posted successfully.")
                print(f"  http result [{result.status_code} {result.reason}]")

    print("Run complete!")


# Convention for possible future module/import
if __name__ == "__main__":
    main()
    sys.exit(0)
