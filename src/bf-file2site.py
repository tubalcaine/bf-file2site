"""bf-file2site.py - A utility to upload a file to a BigFix
site via the REST API"""
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
        "-c", "--savecreds",
        type=str,
        help="Store credentials encrypted"
    )
    parser.add_argument(
        "-k", "--keycreds",
        type=str,
        help="Use stored credentials"
    )
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
    parser.add_argument("files", nargs="+", help="Files to upload")

    conf = parser.parse_args()

    if conf.savecreds is not None:
        ## We need to prompt for and save encrypted credentials
        bf_user = input("BigFix username: ")
        bf_pass = input("BigFix password: ")
        keyring.set_password(conf.savecreds, bf_user, bf_pass)
        sys.exit(0)

    if conf.keycreds is not None:
        xx = keyring.get_credential(conf.keycreds)
        pass

    ## Do the file POST iff the bigfix server is specified
    if conf.bfserver is not None:
        bf_sess = requests.Session()
        bf_sess.auth = (conf.bfuser, conf.bfpass)

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

    print("Run complete!")


# Convention for possible future module/import
if __name__ == "__main__":
    main()
    sys.exit(0)
