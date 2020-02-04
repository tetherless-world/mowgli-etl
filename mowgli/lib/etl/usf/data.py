from xml.dom.minidom import parse, parseString

dom = parse("cue-target.xml")

cue = dom.getElementsByTagName('cue')
words = dict()

for cuetag in cue:
    cueword = cuetag.getAttribute("word")
    targettag = cuetag.getElementsByTagName('target')

    words[cueword] = dict()

    for target in targettag:
        targetword = target.getAttribute("word")
        words[cueword][targetword] = float(target.getAttribute("fsg"))

    for key,val in words.items():
        for key2,val2 in val.items():
            print("<usf:{}>cn:realates-to<usf:{}>weight<usf:{}>".format(key,key2,val2))
