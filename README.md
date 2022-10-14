# bf-file2site
## A tool to upload a files to a BigFix site
This is a simple python script that will allow you to add files to 
a BigFix site. You can add files to any operator or custom site,
provided you have the rights to do so with the operator credentials
you pass in.
### Room for Improvment
#### Consider contributing a pull request!
This code should be considered "proof of concept." I wrote it to be
practical and useful, but the error checking is minimal, you have the
classic problem of exposing credentials in command line arguments,
and there are a number of things I would do to "harden" this code
for true production applications.
It accepts one to many filenames. On unix-like systems thie means
you can use wildcards. I do not actually know if the python argparse
library will do filename globbing. The way it does multiple files is
not very efficient. You can do multiple files with a single REST call
if you build a MIME document to POST them. This script does one POST
per file.

### Command Line Arguments
Be aware of requirements on your operating system for command line
quoting. The "-S/--site" parameter is interpolated directly into the
BigFix REST API URL. I honestly do not know if you have to entity
escape the argument yourself.

    usage: bf-file2site [-h] [-s BFSERVER] [-p BFPORT] [-U BFUSER] [-S SITE]
                        [-P BFPASS]
                        files [files ...]

    positional arguments:
      files                 Files to upload

    optional arguments:
      -h, --help            show this help message and exit
      -s BFSERVER, --bfserver BFSERVER
                            BigFix REST Server name/IP address
      -p BFPORT, --bfport BFPORT
                            BigFix Port number (default 52311)
      -U BFUSER, --bfuser BFUSER
                            BigFix Console/REST User name
      -S SITE, --site SITE  Site url, like custom/CustomSite. Default 'master'
      -P BFPASS, --bfpass BFPASS
                            BigFix Console/REST Password
