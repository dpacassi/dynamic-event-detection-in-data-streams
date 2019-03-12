# Data documentation
The current architecture aims to consume data from two different API's:
- [newsapi.org](https://newsapi.org/)
- [twitter.com](https://developer.twitter.com/)

Both define REST endpoints which return the data in a JSON structure.

## newsapi.org
- 1000 requests per day, one request every 2nd minute -> 720 per day
- free for all non-commercial projects
- attribution required
- Swiss sources (examples):
  - 20min.ch
  - aargauerzeitung.ch
  - blick.ch
  - bluewin.ch
  - itmagazine.ch
  - netzwoche.ch
  - tagesanzeiger.ch
  - telebasel.ch
  - watson.ch
  - www.gmx.ch
  - www.nau.ch
  - www.nzz.ch
  - www.srf.ch
- German sources (examples):
  - bild.de
  - chip.de
  - computerbild.de
  - faz.net
  - filmstarts.de
  - focus.de
  - futurezone.at
  - golem.de
  - handelskraft.de
  - heise.de
  - morgenpost.de
  - pcgameshardware.de
  - pcwelt.de
  - stern.de
  - sueddeutsche.de
  - teleboerse.de
  - www.ndr.de
  - www.tagesspiegel.de
  - www.zeit.de

### Data fields
- source/name (e.g. `www.srf.ch`)
- author (e.g. `Alexander König`)
- title (e.g. `"Schwerer Sturz von Mowinckel - Feuz-Konkurrent Paris mit Trainingsbestzeit - Schweizer Radio und Fernsehen (SRF)`)
- description (e.g. `Dominik Paris setzt im Abschlusstraining zur letzten Weltcup-Abfahrt des Winters in Soldeu ein Zeichen.`)
- url (e.g. `https://www.srf.ch/sport/ski-alpin/weltcup-maenner/schwerer-sturz-von-mowinckel-feuz-konkurrent-paris-mit-trainingsbestzeit`)
- urlToImage (e.g. `https://www.srf.ch/static/cms/images/960w/c940b4a79b27d5e3907d11a3e5d0c5471523496d.jpg`)
- publishedAt (e.g. `2019-03-12T10:56:03Z`, ISO-8601)
- content (limited to 260 characters)

Also check the [newsapi.org response example](response-examples/newsapi.org.json).

### Top headlines (Switzerland)
- https://newsapi.org/v2/top-headlines?apiKey=API_KEY&country=ch&pageSize=100
  - Returns around 30 - 40 results from the past 48 hours
  - (in average one new result every 1-2 hours)

### Everything (Switzerland)
- https://newsapi.org/v2/everything?apiKey=API_KEY&domains=20min.ch,aargauerzeitung.ch,blick.ch,bluewin.ch,itmagazine.ch,netzwoche.ch,tagesanzeiger.ch,telebasel.ch,watson.ch,www.gmx.ch,www.nau.ch,www.nzz.ch,www.srf.ch&from=2019-03-12&pageSize=100
  - Returns around 70 - 80 results for the current day
  - (in average 3-4 new results per hour)

### Everything (German)
- https://newsapi.org/v2/everything?apiKey=API_KEY&q=E&language=de&from=2019-03-12&pageSize=100
  - Returns around 250 results for the current day
  - (in average 10+ new results per hour)
