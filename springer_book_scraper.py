#!/usr/bin/env python3

import os
import sys
import argparse
from io import StringIO

import requests
import pandas as pd

SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1HzdumNltTj2SHmCv3SRdoub8SvpIEn75fa4Q23x0keU/gviz/tq?tqx=out:csv'
URL_PDF = 'https://link.springer.com/content/pdf/{codigo_libro}.pdf'
BASE_DIR = '.'


def download_pdfs_from_url(book_url, book_title, book_topic):
	book_title = book_title.replace("/", "_")
	pdf_file_name = '{base_dir}/{book_topic}/{book_title}.pdf'.format(book_topic=book_topic, book_title=book_title, base_dir=BASE_DIR)
	bytes_downloaded = 0
	file_mode = "wb"
	request_header = {}
	if os.path.exists(pdf_file_name):
		# Resume download
		bytes_downloaded = os.stat(pdf_file_name).st_size
		file_mode = "ab"
		request_header['Range'] = 'bytes={}-'.format(bytes_downloaded)
	try:
		r = requests.get(book_url)
		url_base = r.url
		codigo_libro = url_base.split('/')[-1]
		url_pdf = URL_PDF.format(codigo_libro = codigo_libro)
		response = requests.get(url_pdf, headers=request_header, stream=True)
		total_length = response.headers.get('content-length') or 0
		total_length = int(total_length)
		if total_length == 0:
			print('Skipping: {book_topic} - {book_title}'.format(book_topic=book_topic, book_title=book_title))
			return
		total_length = bytes_downloaded + total_length
		print('Downloading: {book_topic} - {book_title}'.format(book_topic=book_topic, book_title=book_title))
		with open(pdf_file_name, file_mode) as f:
			for data in response.iter_content(chunk_size=65536):
				bytes_downloaded += len(data)
				f.write(data)
				done = int(50 * bytes_downloaded / total_length)
				sys.stdout.write('\r[%s%s] %d%%' % ('=' * done, ' ' * (50-done), done*2) )    
				sys.stdout.flush()
			sys.stdout.write('\r\033[K') #clear line
	except requests.exceptions.HTTPError:
		print('\nError downloading: {book_topic} - {book_title}'.format(book_topic=book_topic, book_title=book_title))
	except KeyboardInterrupt:
		print('\nScript aborted')
		sys.exit(0)


args_parser = argparse.ArgumentParser(description='Download all links from the Google Spreadsheet URL')
args_parser.add_argument('--topics', nargs='+', help="List of topics to download")
args_parser.add_argument('--list-topics', action='store_true', help="Show all available topics")
args = args_parser.parse_args()

if args.list_topics is None and args.topics is None:
	print("No se indican temas. Esto descargara todos los archivos.\n")
	print("Si desea filtrar por tema, ejecute ./springer_book_scraper.py -h para obtener ayuda\n")

response = requests.get(SPREADSHEET_URL)
spreadsheet_csv = StringIO(response.content.decode('utf-8'))

df = pd.read_csv(spreadsheet_csv)

list_of_topics = df['English Package Name'].unique().tolist()

# Handle --list-topics argument
if args.list_topics:
	for topic in list_of_topics:
		print('"{}"'.format(topic))
	print("\nYou can filter by topics with --topics argument. Example:\n")
	print('     ./springer_book_scraper.py --topics "Biomedical and Life Sciences" "Medicine"')
	sys.exit(0)

topics_to_download = list_of_topics
links_to_download = df
if args.topics is not None:
	topics_to_download = args.topics
	links_to_download = df[df['English Package Name'].isin(topics_to_download)]

#  creo una carpeta por topico valido
for topic in topics_to_download:
	folder_name = '{base_dir}/{topic}'.format(base_dir=BASE_DIR, topic=topic)
	if not os.path.exists(folder_name):
		os.makedirs(folder_name)

links_to_download.apply(lambda row: download_pdfs_from_url(row['OpenURL'], row['Book Title'], row['English Package Name']), axis=1)