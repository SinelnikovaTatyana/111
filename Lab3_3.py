import http.client
url='http://example.com'
url = url[7:]  
a = url.split('/')[0] # домен
b = '/' + '/'.join(url.split('/')[1:]) # не домен
conn = http.client.HTTPConnection(a)
conn.request("GET", b)
r = conn.getresponse()
z = r.read().decode('utf-8')
print(z)
conn.close()
