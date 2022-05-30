# importing libraries
from bs4 import BeautifulSoup
import requests
import json,csv
def main(URL):
	File = open("data.json", "w")
	HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36',
								'Accept-Language': 'en-US, en;q=0.5'})
	webpage = requests.get(URL, headers=HEADERS)
	soup = BeautifulSoup(webpage.content, "lxml")

	# retrieving product title
	try:
		title_string = soup.find("span",attrs={"id": 'productTitle'}).string.strip().replace(',', '')
	except AttributeError:
		title_string = "NA"
	Dict_output={"Product Title":title_string}
	jsonString = json.dumps(Dict_output)
	File.write(jsonString)

	# retrieving product description
	final=""
	try:
		var = soup.find("div", attrs={"id":"feature-bullets"})
		desc  = var.find_all('li')
		for item in desc:
			final=item.get_text()
	except AttributeError:
		final = "NA"
	Dict_output={"Product Description":final}
	jsonString = json.dumps(Dict_output)
	File.write(jsonString)

	# retrieving price
	try:
		price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '')
	except AttributeError:
		price = "NA"
	Dict_output={"Product Price":price}
	jsonString = json.dumps(Dict_output)
	File.write(jsonString)

	# retrieving Image URL
	main_url=""
	try:
		img_url = soup.find_all("img", attrs={'id':'landingImage'})
		for item in img_url:
			main_url=item['src']
	except AttributeError:
		main_url = "NA"
	Dict_output={"Product Image URL":main_url}
	jsonString = json.dumps(Dict_output)
	File.write(jsonString)

	File.close()


if __name__ == '__main__':
	with open('input.csv','r') as csvFile:
	    reader=csv.reader(csvFile,delimiter=',')
	    next(reader)
	    for row in reader:
	         url = (f"https://www.amazon.{row[3]}/dp/{row[2]}")
	         try:
	         	main(url)
	         except:
	         	print("Error 404 ",url)
	csvFile.close()
