import urllib, urllib2, json
import xbmc, xbmcaddon

from database import ARTWORK_TYPE_POSTER, ARTWORK_TYPE_FANART
from log import log

__addon__     = xbmcaddon.Addon( "script.moviesetart" )

apiurl = 'http://api.themoviedb.org/3/'
apikey = '4be68d7eab1fbd1b6fd8a3b80a65a95e'
apiconfig = None

def _download_getjson( url, params=(), queryparams={} ):
  url = apiurl + url % params + '?' + _download_format_query(queryparams)
  log( 'downloader: '  + url )
  request = urllib2.Request(url)
  request.add_header('Accept', 'application/json')
  data = json.loads(urllib2.urlopen(request).read())
  return data

def _download_base_url():
  global apiconfig
  if not apiconfig:
    apiconfig = _download_getjson( 'configuration' )
  return apiconfig['images']['base_url'] + 'original'

def _download_format_query( queryparams ):
  query = ['api_key=' + apikey]
  for key, value in queryparams.items():
    query.append( key + '=' + urllib.quote_plus(value) )
  return '&'.join([ str(i) for i in query ])

def download( movieset ):
  log( 'downloader: Searching for collection: ' + movieset['label'] )
  baseurl = _download_base_url()
  artwork = {}

  search = _download_getjson( 'search/collection', queryparams={'query': movieset['label']} )
  if search['total_results'] == 1:
    data = search['results'][0]
    if data['poster_path']:
      artwork[ARTWORK_TYPE_POSTER] = baseurl + data['poster_path']
    if data['backdrop_path']:
      artwork[ARTWORK_TYPE_FANART] = baseurl + data['backdrop_path']
  else:
    log( 'downloader: Error while matching collection: ' + movieset['label'] )
    return 0

  if bool(artwork):
    for artwork_type, artwork_link in artwork.items():
      log( 'downloader: Found type ' + artwork_type + ' link: ' + artwork_link )
    return artwork
  else:
    log( 'downloader: No artwork in collection: ' + movieset['label'] )
    return 0

