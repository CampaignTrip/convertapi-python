#!/usr/bin/python

import logging
import argparse
import json
import re

import convertcom

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s::%(funcName)s(): %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Positional args
    parser.add_argument('accountId', type=str, help="account ID")
    parser.add_argument('projectId', type=str, help="project ID")
    parser.add_argument('-a', '--applicationId', type=str, help="API application ID") # default= TODO add env variable
    parser.add_argument('-s', '--secret', type=str, help="API secret key") # default= TODO add env variable
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('--showAll', type=bool, default=False, help="Whether to show paused and archived experiences also. default is False")
    args = parser.parse_args()

    if args.quiet:
        log.setLevel("ERROR")
    elif args.verbose > 0:
        log.setLevel("DEBUG")
    else:
        log.setLevel("INFO")


    d = convertcom.listExperiences(args.accountId, args.projectId,
                        application_id=args.applicationId,
                        secret=args.secret,
                        verbose=args.verbose)
    if not d:
        log.error("Failed to list experiences in account/project {accountId}/{projectId}!".format(
            accountId=args.accountId, projectId=args.projectId
        ))
        exit(1)

    expStr = ""
    for e in d:
        i = e['id']
        n = e['name']
        k = e['key']
        t = e['type']
        s = e['status']
        if s == "active" or args.showAll:
            expStr += "\n - {key} (id={id}, type={type}, status={status}): {name}".format(
                key=k, id=i, type=t, status=s, name=n)

    log.info("Found the following experiences in account/project {accountId}/{projectId}:{str}".format(
        accountId=args.accountId, projectId=args.projectId, str=expStr))




    d = convertcom.getExperience(args.accountId, args.projectId, 100453369,
                        application_id=args.applicationId,
                        secret=args.secret,
                        verbose=args.verbose)
    if not d:
        log.error("Failed to list experiences in account/project {accountId}/{projectId}!".format(
            accountId=args.accountId, projectId=args.projectId
        ))
        exit(1)
    print(d)



    (e, v) = convertcom.getExperienceVariantMaps(
        args.accountId,
        args.projectId,
        application_id=args.applicationId,
        secret=args.secret,
        verbose=args.verbose)
    if not e:
        log.error("Failed to get experience/variant map in account/project {accountId}/{projectId}!".format(
            accountId=args.accountId, projectId=args.projectId
        ))
        exit(1)
    print(json.dumps(e, indent=2))
    print(json.dumps(v, indent=2))


