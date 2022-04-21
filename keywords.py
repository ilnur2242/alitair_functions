from lxml import etree as xml
from openpyxl import load_workbook as lwb
import requests
import json
from my_functions import functions as f



def get_all_names(path="names.txt", id_name="id",root=None,xml_path=None):
	if root == None:
		root = xml.parse(xml_path).getroot()

	offers = root.find("shop").find("offers").findall("offer")

	names = []
	for offer in offers:
		id = str(offer.attrib[id_name])#ae_101ch_id
		name = str(offer.find("name").text)
		with open(path,"a",encoding="utf-8") as file:
			try:
				line = id+" - "+name+"\n"
				file.write(line)
			except Exception as e:
				line = id+"\t"+"error"+"\n"
				file.write(line)
		file.close()


def set_en_names(path_to_file="en_names.txt",id_name="id",root=None,xml_path=None):
	if root == None:
		root = xml.parse(xml_path).getroot()
	names = {}
	with open(path_to_file,"r",encoding="utf-8") as file:
		temp_list = file.readlines()
		for line in temp_list:
			line = line.split("\n")[0]
			new_line = []
			for elem in line.split(" - "):
				if elem == "":
					continue
				else:
					new_line.append(elem)
			if line == "":
				continue
			else:
				id = new_line[0]
				name = " ".join(new_line[1:])
				#print(id,name,sep="\t")
				names.setdefault(id,name)
	file.close()

	offers = root.find("shop").find("offers")

	for offer in offers:
		id = str(offer.attrib[id_name])#ae_101ch_id
		try:
			desc = "".join(str(offer.find("description").text).split("\n"))
			offer.find("description").text = xml.CDATA(desc)
		except Exception as e:
			print(id, e)




		if id in names:
			try:
				offer.find("en_name").text = names[id]
			except Exception as e:
				xml.SubElement(offer,"en_name").text = names[id]


	f.make_correctXML(root,xml_path)


def set_keywords(root,path,path_to_table:str,sheet_name:str,id_col="a",keyword_col="f"):
	wb = lwb(path_to_table)
	sh = wb[sheet_name]

	data = {}
	i=2
	while True:
		id = str(sh[id_col+str(i)].value).split(".")[0]
		if id == "None":
			break
		keyword = str(sh["d"+str(i)].value)
		data.setdefault(id,keyword)
		i+=1

	offers = root.find("shop").find("offers")

	keywords= {}
	for offer in offers:
		try:
			id = str(offer.attrib["ae_101ch_id"])
		except Exception as e:
			continue
		try:
			desc = "".join(str(offer.find("description").text).split("\n"))
			offer.find("description").text = xml.CDATA(desc)
		except Exception as e:
			print(id, e)
		cat = str(offer.find("categoryId").text)


		if id in data:
			keywords.setdefault(cat,data[id])
	count = 0
	coffers = 0
	for offer in offers:
		id = str(offer.attrib["id"])
		try:
			desc = "".join(str(offer.find("description").text).split("\n"))
			offer.find("description").text = xml.CDATA(desc)
		except Exception as e:
			print(id, e)
		coffers += 1


		cat = str(offer.find("categoryId").text)

		if cat in keywords:
			try:
				offer.find("keyword").text = keywords[cat]
			except Exception as e:
				xml.SubElement(offer,"keyword").text = keywords[cat]
				count+=1
	print(count, coffers)
	print(json.dumps(keywords,indent=2))
	f.make_correctXML(root,path)
	
	
def set_keywords_by_category(path,path_to_table:str,sheet_name="ОБЩИЕ КЛЮЧЕВЫЕ СЛОВА",id_col="a",keyword_col="b",category_tag_name="category",root=None):
	if root == None:
		root = xml.parse(path).getroot()
	
	wb = lwb(path_to_table)
	sh = wb[sheet_name]

	data = {}
	i=2
	while True:
		id = str(sh[id_col+str(i)].value).split(".")[0]
		if id == "None":
			break
		keyword = str(sh[keyword_col+str(i)].value)
		if keyword == "None":
			i+=1
			continue
		data.setdefault(id,keyword)
		i+=1

	offers = root.find("shop").find("offers")
	
	cats = []
	
	for offer in offers:
		cat = str(offer.find(category_tag_name).text)

		if cat in data:
			try:
				offer.find("keyword").text = data[cat]
			except Exception as e:
				xml.SubElement(offer,"keyword").text = data[cat]
		else:
			if cat in cats:
				continue
			else:
				cats.append(cat)

	print("\n".join(cats))
	
	f.make_correctXML(root,path)