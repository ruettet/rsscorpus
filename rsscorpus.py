import feedparser, time, glob, codecs, re
from collections import Counter
from bs4 import BeautifulSoup

def getCorpus():
  out = {}
  try:
    fin = codecs.open("./corpus.xml", "r", "utf-8")
    xml = fin.read()
    fin.close()
    soup = BeautifulSoup(xml)
    entries = soup.find_all("entry")
    for entry in entries:
      key = entry["id"]
      title = entry.find("title").string
      summary = entry.find("summary").string
      date = entry.find("pubdate").string
      out[key] = {"title": title,
                  "summary": summary,
                  "pubdate": date}      
  except IOError:
    out = {}
  return out

def setCorpus(db):
  print "setting", len(db.keys())
  xml = xmlify(db)
  fout = codecs.open("./corpus.xml", "w", "utf-8")
  fout.write(xml)
  fout.close()

def getFeeds():
  fin = open("rssfeeds.txt", "r")
  rssfeeds = fin.readlines()
  fin.close()
  return rssfeeds

def xmlify(d):
  out = ["<rsscorpus>"]
  for k in d.keys():
    out.append("\t<entry id='" + k + "'>")
    for kk in d[k].keys():
      out.append( unicode("\t\t<" + kk + ">" + d[k][kk] + "</" + kk + ">") )
    out.append("\t</entry>")
  out.append("</rsscorpus>")
  return "\n".join(out)

def removeHtml(s):
  return re.sub('<[^<]+?>', '', s)

def wc(db):
  wc = 0
  for entry in db.keys():
    wc += len(unicode(db[entry]["title"] + " " + db[entry]["summary"]).split())
  return wc

def main():
  db = getCorpus()
  print len(db.keys())
  rssfeeds = getFeeds()

  for rssfeed in rssfeeds:
    d = feedparser.parse(rssfeed)
    for item in d["items"]:
      title = removeHtml(item["title"])
      summary = removeHtml(item["summary"])
      pub = time.strftime("%a, %d %b %Y %H:%M:%S", item["published_parsed"])
      uid = item["id"]
      db[uid] = {"title": title,
                 "summary": summary,
                 "pubdate": pub}
    print len(db.keys())
  setCorpus(db)
  print wc(db)

if __name__ == "__main__":
    main()
