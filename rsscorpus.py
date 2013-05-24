import feedparser, time
from collections import Counter

def grabCorpus():
  return {}

def grabFeeds():
  fin = open("rssfeeds.txt", "r")
  rssfeeds = fin.readlines()
  fin.close()
  return rssfeeds

def xmlify(d):
  out = []
  for k in d.keys():
    out.append("<entry id='" + k + "'>")
    for kk in d[k].keys():
      out.append( unicode("\t<" + kk + ">" + d[k][kk] + "</" + kk + ">") )
    out.append("</entry>")
  return "\n".join(out)

db = grabCorpus()
rssfeeds = grabFeeds()

for rssfeed in rssfeeds:
  d = feedparser.parse(rssfeed)
  for item in d["items"]:
    title = item["title"]
    summary = item["summary"]
    pub = time.strftime("%a, %d %b %Y %H:%M:%S", item["published_parsed"])
    link = item["link"]
    uid = item["id"]
    db[uid] = {"title": title,
               "summary": summary,
               "pubdate": pub,
               "link": link}
