from bs4 import BeautifulSoup
import requests
import csv

url = "http://www.loinquieto.net/category/literatura/"
data = []

response = requests.get(url).text
soup = BeautifulSoup(response, 'lxml')

csv_file = open('dataset.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Titulo','Autor','Fecha','Entrada','Tags','Comentarios'])

paginas = soup.find('div',class_='pagination')
for pagina in paginas.ul.find_all('li'):
    pageUrl = pagina.a['href']
    pageRequest = requests.get(pageUrl).text
    pag = BeautifulSoup(pageRequest, 'lxml')
    for articulo in pag.find_all('article'):
        try:
            contenido = articulo.find('div',class_='post-main')
            titulo = contenido.find('header',class_='entry-header').h2.a.text
            articuloUrl = contenido.find('div',class_='continue-reading').a['href']
            articuloRequest = requests.get(articuloUrl).text
            art = BeautifulSoup(articuloRequest, 'lxml')
            autor = art.find('span',class_='author').a.text
            fecha = art.find('span',class_='posted-on').a.text
            entrada = ""
            contenidoArticulo = art.find('div',class_='entry-content')
            for parrafo in contenidoArticulo.find_all('p'):
                try:
                    entrada = entrada + " " +parrafo.text
                except Exception as e:
                    entrada = entrada
            tags = ""
            try:
                contenidoTags = art.find('span',class_='tags-links')
                for tag in contenidoTags.find_all('a'):
                    try:
                        tags = tags + " " +tag.text
                    except Exception as e:
                        tags = tags
            except Exception as e:
                tags = ""
            comentarios = ""
            try:
                contenidoComentarios = art.find('div',class_='comments-area')
                for comentario in contenidoComentarios.ol.find_all('li'):
                    try:
                        comentarios = comentarios + " " +comentario.article.find('div',class_='comment-content').p.text
                    except Exception as e:
                        comentarios = comentarios
            except Exception as e:
                comentarios = ""
            print(titulo)
            csv_writer.writerow([titulo,autor,fecha,entrada,tags,comentarios])
        except Exception as e:
            titulo = None
            print(e)
csv_file.close()
