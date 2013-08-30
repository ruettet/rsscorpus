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
    entries = soup.find_all(u"entry")
    for entry in entries:
      try:
        key = entry[u"id"]
        title = entry.find(u"title").string
        summary = entry.find(u"summary").string
        date = entry.find(u"pubdate").string
        out[key] = {u"title": title,
                    u"summary": summary,  
                    u"pubdate": date}      
      except:
        continue
  except IOError:
    out = {}
  return out

def setCorpus(db):
  print "saving corpus", len(db.keys())
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
      try:
        out.append( unicode("\t\t<" + kk + ">" + d[k][kk] + "</" + kk + ">") )
      except:
        continue
    out.append("\t</entry>")
  out.append("</rsscorpus>")
  return "\n".join(out)

def removeHtml(s):
  return re.sub('<[^<]+?>', '', s)

def wc(db):
  wc = 0
  for entry in db.keys():
    try:
      wc += len(unicode(db[entry][u"title"] + " " + db[entry][u"summary"]).split())
    except:
      continue
  return wc

def main():
  db = getCorpus()
  print "there are", len(db.keys()), "rss feeds available"
  rssfeeds = getFeeds()

  for rssfeed in rssfeeds:
    print "\tchecking:", rssfeed.strip()
    d = feedparser.parse(rssfeed)
    for item in d[u"items"]:
      title = removeHtml(item[u"title"])
      summary = removeHtml(item[u"summary"])
      pub = time.strftime(u"%a, %d %b %Y %H:%M:%S", item[u"published_parsed"])
      uid = item[u"id"]
      db[uid] = {u"title": title,
                 u"summary": summary,
                 u"pubdate": pub}
  setCorpus(db)
  print "approximate word count:", wc(db)

if __name__ == "__main__":
    main()
