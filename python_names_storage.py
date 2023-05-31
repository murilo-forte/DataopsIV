from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "seraphic-scarab-368022",
  "private_key_id": "cfa660904c69872149acc2be6c674464471cdb2e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCqqNMR+ue0kReX\nDDxlFPckOmdVnoAsiBk7LYW7a+loWoNUuMc7+CrIWy3ETF55N1jgG4XvVZl2SdS+\n2I4H9a1Sjlh1bxQ39O/9N3W/vs2Nhe3JeBn2FGX/VNbmwBy2mfslx/p7Mpb4QonD\nHJSF+xfDNJR+WKyWOgRrA6tEbG9vvb2U1tg2foR1E53cyCXmezH1T5U+mrB1x9kP\npzgHd3MkgogmJYExYO9zF6w12oXv+a3w6En8KrIkZEnmeAxQnHXAKMaS7POvSedy\nGc0041WT17fYdyG97zyi2oQhfiyrNcbMoV5PP8PVEBMikPpkltgV6X+aYBWlBCSM\n7bewOhkXAgMBAAECggEAFZVZcHYzlLYe7icJgl027nmGdSEhI8CotD/LIIuCzwRX\nhMEDzZVSz9kcPi3MavcxgdJpS34fdQLcabCYsfAD1iOTk3KTc4pCSduYREJc28+6\n5ZaPbfxhc/vmW/OjDgMGbN5QUwFwb4B2zNrR++noNPNy7lHHrg4zXdducy5ln5OB\nygJEE1wwkBRM3tLmI3tsDrvMEHUr/NinR+viydtfHJr8eXGk02LeOPlVkP2wfelK\nFLM69L3dsTjXnnVGNUgut/TnrrG3dHWWYEMrvNn25pVnVeFCVn6TlkBw+0E0mP52\nG7+GPd0xC7IbPU3jpBEhtPoa16g18rNv3b/DAt8tHQKBgQDvU9X8vkUMjavKMkEk\n1XsjP8t58KuoHI5HXFmiPaQPCkPEBV7Owr/9sG6WMBYE+96wN0F5tSlrTM52aJGV\nM92xp1KlUQzPppgMSSSg4LNQdGVhQHF/3PNnCsr2Ysrrq9Lkg6teKVELxMQeTgKS\nOAGKmT9TA52FSAArDxnZiigMQwKBgQC2jF0ocxLg5KU+2kzI7zltYsLTx5ZIa9w+\nHsA6Y4Kn0jcyUQwuu4txugarfHCWJ14nQIGnF24q/tsfyWuUXBiZMRvxnMLfGyXe\nn7aszJdPnmkHUNOTF4v6QtxCj9sGPvavv67ql9PJ/x6KToGfKxeeUA40YSu+VxLQ\nNNbyxsvcnQKBgBpiWq/vZftZTvwOiEIASv/603rQ/oudAk55ruQE+aYy0n+0u9v9\nel8EaVyjVnocLlOs88nwH+3VXNmO86XIPwOL17+j7M6jphWMpr4Zp4sSGe8bxKd8\n+1R7yx5Yi9hpa+mHXogV8/phKeHRZdUq2XinJmUHfAEqi+IzWv0xjvKzAoGAN9kF\nfySFeAw7idkbeLXHafG3DTeYgJuPC+o4gSSEindDr78f7QQviyGQfNJbV3S/115i\nzA3dBIZn33et0/vBAs0FcYu2Cq+xjERsjL0i5ZbfJv/RWsTvbCccX7jHF0gYDHim\nONsuTjQg0ctm2J1EYoi3b8ryqQ7WkKA5ypiLMfkCgYA7Azv+BochIFK/obFWt4wf\n/EZHp/qzWpAUme20YaX4Na0EjvnWsbcNefu4oVuNmSLWwOFMN7vhPD+265XLo2hY\nLHFc140yMZyMahAoU+7mMmuuNxK4hGzsZ7RGnJVAXPf4nnGMn/3EYas4VOl8O0HY\nZzttJQUJ1jIvH/WtPUdQeQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "service@seraphic-scarab-368022.iam.gserviceaccount.com",
  "client_id": "106065757886936028340",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service%40seraphic-scarab-368022.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('trabalhoiv') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
