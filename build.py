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
browsers = ["ios_saf","blackberry", "ie", "firefox", "android", "op_mob", "and_chr"]
browsersImages = { "ios_saf" : {"name": "Safari on iOS", "x":0,"y":0,"width":60,"height":60, "url":"safari.jpg"},
                   "blackberry": {"name": "Blackberry browser", "x":0,"y":75,"width":60,"height":49.5, "url":"blackberry.jpg", "caniusename": "bb"},
                   "ie": {"name": "Internet Explorer on Windows Phone", "x":63,"y":70,"width":60,"height":60, "url":"ie.png"},
                   "firefox": {"name": "Firefox mobile", "x":130,"y":70,"width":60,"height":60, "url":"firefox.png", "caniusename": "and_ff"},
                   "android": {"name": "Android browser", "x":65,"y":0,"width":60,"height":60, "url":"android.png"},
                   "op_mob":  {"name": "Opera mobile", "x":130,"y":0,"width":60,"height":60, "url":"opera.png"},
                   "and_chr":  {"name": "Chrome for Android", "x":195,"y":0,"width":60,"height":59, "url":"chrome.png"}
}

mergeddata = {}
image = open("images/full.svg", "w")
image.write("""<svg
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   width="123"
   height="70"
   viewBox="0 0 255 140"
   version="1.1">
     <style typ="text/css">.unknown, .not { opacity: 0.3 } .partial { opacity: 0.8}</style>
<title>Support for Web Platform features in mobile browsers</title>
""")

for feature,sourcelist in featuremap.iteritems():
    mergeddata[feature] = {}
    if len(sourcelist)==2:
        for browser,version in mobilehtml[sourcelist[1]].iteritems():
            if version:
                mergeddata[feature][browser] = [version,"y"]
            else:
                mergeddata[feature][browser] = []
    if localdata.has_key(feature):
        for b in browsers:
            if localdata[feature].has_key(b):
                if len(str(localdata[feature][b]).split(":"))==2 and localdata[feature][b].split(":")[1]=="p":
                    mergeddata[feature][b] = [str(localdata[feature][b]).split(":")[0],"p"]
                else:
                    if str(localdata[feature][b]).split(":")[0] != "0":
                        mergeddata[feature][b] = [str(localdata[feature][b]).split(":")[0],"y"]
                    else:
                        mergeddata[feature][b] = []
            elif localdata[feature].has_key("*"):
                if not(mergeddata[feature].has_key(b)):
                           mergeddata[feature][b] = []
    if len(sourcelist) > 0:
        if sourcelist[0]:
            if not caniuse["data"].has_key(sourcelist[0]):
                sys.stderr.write("Couldn't find feature %s (%s) in canIuse data\n" % (sourcelist[0], feature))
            else:
                for b in browsers:
                    caniusename = browsersImages[b]["caniusename"] if browsersImages[b].has_key("caniusename") else b
                    min_version = 0
                    min_partial_version = 0
                    unsupported = False
                    if not caniuse["data"][sourcelist[0]]["stats"].has_key(caniusename):
                        continue
                    if type(caniuse["data"][sourcelist[0]]["stats"][caniusename]) == dict:
                        for version,status in caniuse["data"][sourcelist[0]]["stats"][caniusename].iteritems():
                            if len(str(version).split("-")) > 1:
                                version = str(version).split("-")[0]                
                            version=float(version)
                            if status[0] == "y":
                                min_version =  min(min_version,version) if min_version else version
                            elif status[0] == "a":
                                min_partial_version = min(min_partial_version,version) if min_partial_version else version
                            elif status == "n":
                                unsupported = True
                            if min_version:
                                mergeddata[feature][b] =  [min_version, "y"]
                            elif min_partial_version:
                                mergeddata[feature][b] =  [min_partial_version, "p" ]
                            elif unsupported:
                                mergeddata[feature][b] = []
                    elif type(caniuse["data"][sourcelist[0]]["stats"][caniusename]) == list:
                        version = caniuse["agents"][caniusename]["current_version"]
                        status = caniuse["data"][sourcelist[0]]["stats"][caniusename][0]
                        if status[0] == "y":
                            min_version = version
                        elif status[0] == "a":
                            min_partial_version = version
                        elif status[0] == "n":
                            unsupported = True
                        if min_version:
                            mergeddata[feature][b] =  [min_version, "y"]
                        elif min_partial_version:
                            mergeddata[feature][b] =  [min_partial_version, "p" ]
                        elif unsupported:
                            mergeddata[feature][b] = []
    image = open("images/%s.svg" % feature, "w")
    image.write("""<svg
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   width="123"
   height="70"
   viewBox="0 0 255 140"
   version="1.1">
     <style typ="text/css">.unknown, .not { opacity: 0.3 } .partial { opacity: 0.8}</style>""")
    image.write("<title>Support for %s</title>" % (feature))
    for b in browsers:
        bData = browsersImages[b]
        if mergeddata[feature].has_key(b):
            if len(mergeddata[feature][b]):
                if mergeddata[feature][b][1] == "p":
                    text = "Partial support in %s from version %s" % (bData["name"], mergeddata[feature][b][0])
                    className = "partial"
                    label = "<rect x='%s' y='%s' width='60' height='22' fill='#ff0' opacity='0.8'></rect><text x='%s' y='%s' font-size='20px'>%s+</text>" % (bData["x"], bData["y"] + bData["height"]/2, bData["x"] + 3, bData["y"] + bData["height"]/2 + 15, mergeddata[feature][b][0])
                else:
                    text = "Supported in %s from version %s" % (bData["name"],mergeddata[feature][b][0])
                    className =""
                    label = "<rect x='%s' y='%s' width='60' height='22' fill='#fff' opacity='0.8'></rect><text x='%s' y='%s' font-size='20px'>%s+</text>" % (bData["x"], bData["y"] + bData["height"]/2, bData["x"] + 3 , bData["y"] + bData["height"]/2 + 15, mergeddata[feature][b][0])
            else:
                className = "not"
                text = "Not supported in %s" % (bData["name"])
                label = "<text x='%s' y='%s' font-size='40px' fill='red' text-anchor='middle'>X</text>" % (bData["x"] + bData["width"]/2, bData["y"] + bData["height"]/2 + 15)
        else:
            className = "unknown"
            text = "Supported in %s unknown" % (bData["name"])
            label = "<text x='%s' y='%s' font-size='40px' fill='blue' text-anchor='middle'>?</text>" % (bData["x"] + bData["width"]/2, bData["y"] + bData["height"]/2 + 15)
        image.write("<g><title>%s</title>" %(text))
        image.write("<image xlink:href='../%s' class='%s' x='%s' y='%s' width='%s' height='%s'></image>" %(bData["url"], className, bData["x"], bData["y"], bData["width"], bData["height"]))
        image.write(label)
        image.write("</g>\n")
    image.write("""<script type='text/javascript'>
if (window.location.hash) {
  var hash = window.location.hash.slice(1);
  var features = document.documentElement.childNodes;
  for (var i = 0; i&lt;features.length; i++) {
    if (features[i].id) {
       if (features[i].id != hash) {
          features[i].style.display = 'none';
       } else {
          features[i].style.display = 'inherit';
       }
     }
  }
}
</script>""")
    image.write("</svg>");
    image.close()

print json.dumps(mergeddata)
