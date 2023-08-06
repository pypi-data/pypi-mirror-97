#!/usr/bin/env python
"""
`htrc.volumes`

Contains functions to retrieve volumes from the HTRC Data API. 

The functions in this package will not operate unless they are 
executed from an HTRC Data Capsule in Secure Mode. The module 
`htrc.mock.volumes` contains Patch objects for testing workflows.
"""
from __future__ import print_function
from future import standard_library

standard_library.install_aliases()

from builtins import input

import http.client
from io import BytesIO  # used to stream http response into zipfile.
import json
import logging
import os.path
import progressbar
import re
import socket
import ssl
import sys
from time import sleep
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote_plus, urlencode
import xml.etree.ElementTree as ET
from zipfile import ZipFile  # used to decompress requested zip archives.

from htrc.lib.cli import bool_prompt
from htrc.util import split_items
import htrc.config

import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())


def get_volumes(token, volume_ids, host, port, cert, key, epr, concat=False, mets=False):
    """
    Returns volumes from the Data API as a raw zip stream.

    Parameters:
    :token: An OAuth2 token for the app.
    :volume_ids: A list of volume_ids
    :concat: If True, return a single file per volume. If False, return a single
    file per page (default).
    :host: Data API host
    :port: Data API port
    """
    if not volume_ids:
        raise ValueError("volume_ids is empty.")

    url = epr + "volumes"

    for id in volume_ids:
        if ("." not in id
                or " " in id):
            print("Invalid volume id " + id + ". Please correct this volume id and try again.")

    data = {'volumeIDs': '|'.join(
        [id.replace('+', ':').replace('=', '/') for id in volume_ids])}
    if concat:
        data['concat'] = 'true'

    if mets:
        data['mets'] = 'true'

    # Authorization
    headers = {"Authorization": "Bearer " + token,
               "Content-type": "application/x-www-form-urlencoded"}

    # Create SSL lookup
    # TODO: Fix SSL cert verification
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Retrieve the volumes
    httpsConnection = http.client.HTTPSConnection(host, port, context=ctx, key_file=key, cert_file=cert)

    httpsConnection.request("POST", url, urlencode(data), headers)

    response = httpsConnection.getresponse()

    if response.status is 200:
        body = True
        data = BytesIO()
        bytes_downloaded = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength,
                                      widgets=[progressbar.AnimatedMarker(), '    ',
                                               progressbar.DataSize(),
                                               ' (', progressbar.FileTransferSpeed(), ')'])

        while body:
            body = response.read(128)
            data.write(body)
            bytes_downloaded += len(body)
            bar.update(bytes_downloaded)

        data = data.getvalue()
    else:
        logging.debug("Unable to get volumes")
        logging.debug("Response Code: {}".format(response.status))
        logging.debug("Response: {}".format(response.reason))
        raise EnvironmentError("Unable to get volumes.")

    if httpsConnection is not None:
        httpsConnection.close()

    return data


def get_pages(token, page_ids, host, port, cert, key, epr, concat=False, mets=False):
    """
    Returns a ZIP file containing specfic pages.

    Parameters:
    :token: An OAuth2 token for the app.
    :volume_ids: A list of volume_ids
    :concat: If True, return a single file per volume. If False, return a single
    file per page (default).
    """
    if not page_ids:
        raise ValueError("page_ids is empty.")

    url = epr + "pages"

    for id in page_ids:
        if ("." not in id
                or " " in id):
            print("Invalid volume id " + id + ". Please correct this volume id and try again.")

    data = {'pageIDs': '|'.join(
        [id.replace('+', ':').replace('=', '/') for id in page_ids])}

    if concat and mets:
        print("Cannot set both concat and mets with pages.")
    elif concat:
        data['concat'] = 'true'
    elif mets:
        data['mets'] = 'true'

    # Authorization
    headers = {"Authorization": "Bearer " + token,
               "Content-type": "application/x-www-form-urlencoded"}

    # Create SSL lookup
    # TODO: Fix SSL cert verification
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Retrieve the volumes
    httpsConnection = http.client.HTTPSConnection(host, port, context=ctx, key_file=key, cert_file=cert)

    httpsConnection.request("POST", url, urlencode(data), headers)

    response = httpsConnection.getresponse()

    if response.status is 200:
        body = True
        data = BytesIO()
        bytes_downloaded = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength,
                                      widgets=[progressbar.AnimatedMarker(), '    ',
                                               progressbar.DataSize(),
                                               ' (', progressbar.FileTransferSpeed(), ')'])

        while body:
            body = response.read(128)
            data.write(body)
            bytes_downloaded += len(body)
            bar.update(bytes_downloaded)

        data = data.getvalue()
    else:
        logging.debug("Unable to get pages")
        logging.debug("Response Code: ".format(response.status))
        logging.debug("Response: ".format(response.reason))
        raise EnvironmentError("Unable to get pages.")

    if httpsConnection is not None:
        httpsConnection.close()

    return data


def get_oauth2_token(username, password):
    # make sure to set the request content-type as application/x-www-form-urlencoded
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials",
            "client_secret": password,
            "client_id": username}
    data = urlencode(data)

    # create an SSL context
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # make sure the request method is POST
    host, port = htrc.config.get_oauth2_host_port()
    oauth2port = htrc.config.get_oauth2_port()
    oauth2EPRurl = htrc.config.get_oauth2_url()
    httpsConnection = http.client.HTTPSConnection(host, oauth2port, context=ctx)
    httpsConnection.request("POST", oauth2EPRurl + "?" + data, "", headers)

    response = httpsConnection.getresponse()

    # if response status is OK
    if response.status == 200:
        data = response.read().decode('utf8')

        jsonData = json.loads(data)
        logging.info("*** JSON: {}".format(jsonData))

        token = jsonData["access_token"]
        logging.info("*** parsed token: {}".format(token))

    else:
        logging.debug("Unable to get token")
        logging.debug("Response Code: {}".format(response.status))
        logging.debug("Response: {}".format(response.reason))
        logging.debug(response.read())
        raise EnvironmentError("Unable to get token.")

    if httpsConnection is not None:
        httpsConnection.close()

    return token


def grep_error(file_name, output_dir, pattern, txt_index):
    na_volume = []
    if output_dir.endswith("/"):
        file_path = output_dir + file_name
    else:
        file_path = output_dir + "/" + file_name

    if os.path.isfile(file_path):
        for line in open(file_path):
            if pattern in line:
                na_volume.append(line.split()[txt_index])

    return na_volume

def download_volumes(volume_ids, output_dir, username=None, password=None,
                     config_path=None, token=None, concat=False, mets=False, pages=False, host=None, port=None,
                     cert=None, key=None, epr=None):
    # create output_dir folder, if nonexistant
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # get token if not specified
    if not token:
        token = htrc.config.get_jwt_token()
        htrc.config.remove_jwt_token()

    if not host:
        host = htrc.config.get_dataapi_host()

    if not port:
        port = htrc.config.get_dataapi_port()

    if not epr:
        epr = htrc.config.get_dataapi_epr()

    if not cert:
        cert = htrc.config.get_dataapi_cert()

    if not key:
        key = htrc.config.get_dataapi_key()

    if any((token, host, port)) is not None:
        logging.info("obtained token: %s\n" % token)

        try:
            for ids in split_items(volume_ids, 250):
                if pages:
                    if concat & mets:
                        raise ValueError("Cannot set both concat and mets with pages.")
                    else:
                        data = get_pages(token, ids, host, port, cert, key, epr, concat, mets)
                else:
                    data = get_volumes(token, ids, host, port, cert, key, epr, concat, mets)

                myzip = ZipFile(BytesIO(data))
                myzip.extractall(output_dir)
                myzip.close()

                na_volumes_all = []
                if htrc.config.get_dataapi_access() == "true":
                    na_volumes_rights = grep_error("volume-rights.txt", output_dir, " 3", 0)
                    na_volumes_all = na_volumes_rights

                na_volumes_error = grep_error("volume-rights.txt", output_dir, " unavailable", 0)

                if len(na_volumes_error) > 0:
                    na_volumes_all = na_volumes_all + na_volumes_error

                if len(na_volumes_all) > 0:
                    with open(os.path.join(output_dir, "volume_not_available.txt"), "w") as volume_na:
                        volume_na.write("\n".join(str(item) for item in na_volumes_all))

                if 0 < len(na_volumes_all) < 100:
                    print("\nFollowing volume ids are not available. \n Please check volume_not_available.txt for the "
                          "complete list. ")
                    print("\n".join(str(item) for item in na_volumes_all))
                else:
                    if len(na_volumes_all) >= 100:
                        print("\nThere are 100 or more unavailable volumes.\n Please check volume_not_available.txt "
                              "for the "
                              "complete list. \nTo check the validity of volumes in your workset or volume id file go "
                              "to:\n "
                              "https://analytics.hathitrust.org/validateworkset \n or email us at "
                              "htrc-help@hathitrust.org "
                              "for assistance.")


        except socket.error:
            raise RuntimeError("HTRC Data API time out. Check your inode usage if downloading a large workset. "
                               "Contact HTRC for further help.")

    else:
        raise RuntimeError("Failed to obtain jwt token.")


def download(args):
    # extract files
    with open(args.file) as IDfile:
        volumeIDs = [line.strip() for line in IDfile]

    return download_volumes(volumeIDs, args.output,
                            username=args.username, password=args.password,
                            token=args.token, concat=args.concat, mets=args.mets, pages=args.pages, host=args.datahost,
                            port=args.dataport, cert=args.datacert, key=args.datakey,
                            epr=args.dataepr)
