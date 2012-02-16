#!/usr/bin/python

import json, sys
featuremapsrc = open("feature-map.json")
featuremap = json.loads(featuremapsrc.read())

caniusesrc = open("caniuse-data.json")
caniuse = json.loads(caniusesrc.read())

mobilehtmlsrc = open("mobilehtml5-data.json")
mobilehtml = json.loads(mobilehtmlsrc.read())

localdatasrc = open("local-data.json")
localdata = json.loads(localdatasrc.read())
browsers = ["ios_saf","blackberry", "ie", "firefox", "android", "opera"]
mergeddata = {}
for feature,sourcelist in featuremap.iteritems():
    mergeddata[feature] = {}
    if len(sourcelist)==2:
        for browser,version in mobilehtml[sourcelist[1]].iteritems():
            if version:
                mergeddata[feature][browser] = [version,"y"]
            else:
                mergeddata[feature][browser] = []
    else:
        mergeddata[feature] = {}
    if localdata.has_key("feature"):
        for b in browsers:
            if localdata[feature].has_key(b):
                if len(localdata[feature][b].split(":"))==2 and localdata[feature][b].split(":")[1]=="p":
                    mergeddata[feature][b] = [localdata[feature][b].split(":")[0],"p"]
                else:
                    mergeddata[feature][b] = [localdata[feature][b].split(":")[0],"y"]
            elif localdata[feature].has_key("*"):
                mergeddata[feature][b] = []
    if len(sourcelist) > 0:
        if sourcelist[0] and not caniuse["data"].has_key(sourcelist[0]):
            sys.stderr.write("Couldn't find feature %s (%s) in canIuse data\n" % (sourcelist[0], feature))
            continue
        for b in browsers:
            try:
                min_version = 0
                min_partial_version = 0
                for version,status in caniuse["data"][sourcelist[0]]["stats"][b]:
                    if status == "y":
                        min_version =  min(min_version,version) if min_version else version
                    elif status == "a":
                        min_partial_version = min(min_partial_version,version) if min_partial_version else version
                mergeddata[feature][b] =  [min_version, "y"] if min_version else [min_partial_version, "p" ]  if min_partial_version else  []
            except:
                pass

print json.dumps(mergeddata)
