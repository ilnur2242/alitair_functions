from unicodedata import category
from lxml import etree as xml
from openpyxl import load_workbook as lwb
import requests
import json

def convert_base(num, to_base=10, from_base=10):
	# first convert to decimal number
	if isinstance(num, str):
		n = int(num, from_base)
	else:
		n = int(num)
	# now convert decimal to 'to_base' base
	alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if n < to_base:
		return alphabet[n]
	else:
		return convert_base(n // to_base, to_base) + alphabet[n % to_base]


def make_correctXML(root, filename):
	'''
	Not return
	'''
	md = xml.tostring(root, encoding="utf-8", method="xml").decode(encoding="utf-8")

	md_new = md.split("><")
	md_new[0] = md_new[0]+">"
	md_new[len(md_new)-1] = "<" + md_new[len(md_new)-1]
	for i in range(1,len(md_new)-1):
		md_new[i] = "<" + md_new[i] + ">"


	file = open(filename, "w",encoding="utf-8")
	file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
	for i in md_new:
		file.write(i + "\n", )

	file.close()


def download_xml(url,path):
	resp = requests.get(url)
	file = open(path,"w",encoding="utf-8")
	resp.encoding = 'utf-8'
	file.write(resp.text)
	file.close()


def write_group_id(path_json,xlsx,num_list=1):
	wb = lwb(xlsx)
	sh = wb.get_sheet_by_name("Лист"+str(num_list))

	with open(path_json,"r",encoding="utf-8") as file:
		res = (json.load(file))['aliexpress_product_productgroups_get_response']['result']['target_list']["aeop_ae_product_tree_group"]
		print(json.dumps(res, ensure_ascii=False,indent=4))
		i = 2
		for group in res:
			id = group["group_id"]
			name = group["group_name"]
			sh["a"+str(i)].value = name
			sh["c"+str(i)].value = str(id)
			i+=1
			try:
				for child in group["child_group_list"]["aeop_ae_product_child_group"]:
					id = child["group_id"]
					name = child["group_name"]
					sh["b"+str(i)].value = name
					sh["c"+str(i)].value = str(id)
					i+=1
			except Exception as e:
				print(e)
			continue
	file.close()
	wb.save(xlsx)



def get_shop(root):
	return root.find("shop")


def get_offers(root):
	return root.find("shop").find("offers")

def get_categories(root):
	return root.find("shop").find("categories")

def get_id(offer):
	return str(offer.attrib["id"])

def get_description(offer):
	return str(offer.find("description").text)

def set_description(offer, text):
	offer.find("description").text = text

def add_item(to, name, text):
	xml.SubElement(to,name).text = xml.CDATA(text)

def open_xml(path):
	tree = xml.parse(path)
	root = tree.getroot()
	return root

def open_xlsx(path):
	return lwb(path)

def get_sheet(wb,name):
	return wb.get_sheet_by_name(name)

def get_sheet_value(sheet, column:str, row:int):
	return str(sheet[column+str(row)].value)


def creat_xml_data(path,
					sheet_name,
					path_to_save,
					start_index=2,
					ae_id_name="ae_id",
					ae_id_col="a",
					name_col="d",
					sku_col = None,
					category_col = None,
					price_col = None,
					dprice_col = None,
					keyword_col=None,
					gi_col=None,
					pic_col=None,
					inv_col=None):
	"""
	Полное описание параметров:
	path - Путь таблице excel
	sheet_name - Название листа
	start_index - Начальная строка
	ae_id_name - Название атрибута для spu алиэкспресса
	name_col - Буква колонки с именем
	sku_col - Буква колонки с sku
	category_col - Буква колонки с названием категории
	price_col - Буква колонки с ценой
	dprice_col - Буква колонки с ценой со скидкой
	keyword_col - Буква колонки с ключевыми словами
	gi_col - Буква колонки с идентификатором товарного дерева
	pic_col - Буква колонки с картинками
	inv_col - Буква колонки с кол-вом остатков
	"""
	wb = lwb(path)
	sh = wb.get_sheet_by_name(sheet_name)

	yml_catalog = xml.Element("yml_catalog")
	shop = xml.SubElement(yml_catalog,"shop")
	offers = xml.SubElement(shop,"offers")

	i=start_index

	while True:
		ae_id = str(sh[ae_id_col+str(i)].value).split(".")[0]
		if ae_id == "None":
			print(i, "the last row")
			break
		offer= xml.SubElement(offers, "offer",attrib={ae_id_name:ae_id})
		xml.SubElement(offer, "name").text = str(sh[name_col+str(i)].value)
		
		if sku_col != None:
			offer.attrib["id"] = str(sh[sku_col+str(i)].value)
		
		if category_col != None:
			xml.SubElement(offer, "category").text = str(sh[category_col+str(i)].value)
			
		if price_col != None:
			xml.SubElement(offer, "price").text = str(sh[price_col+str(i)].value)
		if dprice_col != None:
			dprice = str(sh[dprice_col+str(i)].value)
			if dprice != "None":
				xml.SubElement(offer, "dprice").text = dprice
		
		
		if keyword_col != None:
			keyword = str(sh[keyword_col+str(i)].value)
			if keyword == "None":
				i+=1
				continue
			xml.SubElement(offer, "keyword").text = keyword
		
		if gi_col != None:
			group_id = []
			for gi_col_elem in gi_col.split(","):
				group_id_elem = str(sh[gi_col_elem+str(i)].value).split(".")[0]
				if group_id_elem != "None":
					group_id.append(group_id_elem)
			xml.SubElement(offer, "group_id").text = ",".join(group_id)
		
		if pic_col != None:
			for pic_col_elem in pic_col.split(","):
				pic = str(sh[pic_col_elem+str(i)].value)
				if pic != "None":
					xml.SubElement(offer, "picture").text = pic
		if inv_col != None:
			xml.SubElement(offer, "quantity").text = str(sh[inv_col+str(i)].value)
		i+=1

	make_correctXML(yml_catalog, path_to_save)

def set_ae_id(xml_path,table_path,sheet_name,root=None,tag_name="ae_id",start_index=4):
	'''
	Set aliexpress id
	'''
	if root == None:
		root = xml.parse(xml_path).getroot()
	wb = lwb(table_path)
	sh = wb.get_sheet_by_name(sheet_name)
	
	data = {}
	i=start_index
	while True:
		ae_id = str(sh["a"+str(i)].value)
		if ae_id == "None":
			print(i)
			break
		ids = str(sh["b"+str(i)].value).split(", ")
		
		data.setdefault(ae_id,ids)
		i+=1
		
	offers = root.find("shop").find("offers").findall("offer")
	for offer in offers:
		sku = str(offer.attrib["id"])
		
		try:
			ae_id = str(offer.attrib[tag_name])
			del offer.attrib[tag_name]
		except Exception as e:
			print(e)
		
		for elem in data:
			if sku in data[elem]:
				offer.attrib[tag_name] = elem
				break
				
				
	make_correctXML(root,xml_path)
				
def set_ae_category_id(xml_path,table_path,sheet_name, category_id_col:str,category_ae_col:str,root=None,start_index=2):
	'''
	Set aliexpress category id
	'''
	if root == None:
		root = xml.parse(xml_path).getroot()
	wb = lwb(table_path)
	sh = wb.get_sheet_by_name(sheet_name)
	
	data = {}
	i=start_index
	while True:
		name = str(sh[category_id_col+str(i)].value)
		if name == "None":
			print(i)
			break
		id = str(sh[category_ae_col+str(i)].value).split(".")[0]
		
		
		data.setdefault(name,id)
		i+=1
		
	offers = root.find("shop").find("offers").findall("offer")
	for offer in offers:
		category = offer.find("categoryId")
		try:
			name = str(category.text)
			id = data[name]
			category.attrib["ae_category_id"] = id
		except Exception as e:
			print(e)
			
				
				
	make_correctXML(root,xml_path)
				
def cdata(desc=None, pics=None, params=None):
	
	res = ""
	if desc != None:
		res+="<p style=\"font-size:24px; text-align:left; margin-bottom:25px;font-weight:bolder;\">Описание</p>\n"
		res+="<p style=\"font-size:18px;text-align:left;margin:5px 20px;color:#666666;\">"+desc+"</p>\n" #description
	
	if params != None:
		res+="<p style=\"font-size:24px; text-align:left; margin:25px 10px;font-weight:bolder;\">Характеристики</p>\n"
		res+="<table border=\"1\" style=\"font-size:16px;color:#666666;border: 1px solid #e7e7e7;\" width=\"100%\"><tbody>\n"
		for param in params:
			res+="<tr style=\"text-align:left;height:50px; \"><td style=\"background:#f4f4f4; width:40%;border: 1px solid #e7e7e7;padding:0 10px;font-weight:bold;\">"+str(param)+"</td>	<td style=\"width:60%;border: 1px solid #e7e7e7;padding:0 10px;\">"+str(params[param])+"</td></tr>\n"
		res+="</tbody></table>\n"
	
	if pics != None:
		res+="<p style=\"font-size:24px; text-align:left; margin-bottom:25px;font-weight:bolder;\">Внешний вид товара</p>\n"
		res+="<table border=\"0\" cellpadding=\"10\" cellspacing=\"10\" width=\"100%;\" style=\"margin-bottom:30px;\"><tbody>\n"
		for pic in pics:
			res+="<tr><td style=\"padding: 5px;width: 50.0%;border: 0px solid #e7e7e7;\">	<img src="+pic+" style=\"width: 100.0%;\"></td></tr>\n"
		res+="</tbody></table>\n"

	return res

def cdata_add_pics(desc, pics=None):
	
	res = ""
	if desc != None:
		res+="<p style=\"font-size:24px; text-align:left; margin-bottom:25px;font-weight:bolder;\">Описание</p>\n"
		res+="<p style=\"font-size:18px;text-align:left;margin:5px 20px;color:#666666;\">"+desc+"</p>\n" #description
	
	
	
	if pics != None:
		res+="<p style=\"font-size:24px; text-align:left; margin-bottom:25px;font-weight:bolder;\">Внешний вид товара</p>\n"
		res+="<table border=\"0\" cellpadding=\"10\" cellspacing=\"10\" width=\"100%;\" style=\"margin-bottom:30px;\"><tbody>\n"
		for pic in pics:
			res+="<tr><td style=\"padding: 5px;width: 50.0%;border: 0px solid #e7e7e7;\">	<img src="+pic+" style=\"width: 100.0%;\"></td></tr>\n"
		res+="</tbody></table>\n"

	return res
	
def set_info_gi_kw(path,tpath,sheet_name=u"Шаблон"):
	'''
	Annotation
	tpath is full path to xlsx table
	path is full path to xml file
	'''
	root = xml.parse(path).getroot()
	data = {}
	for offer in get_offers(root):
		try:
			ae_id = offer.attrib["ae_id"]
		except Exception as e:
			print(e)
			continue

		gi = offer.attrib["gi"]
		kayw = offer.attrib["kw"]
		data.setdefault(ae_id,(gi,kayw))

	wb = lwb(tpath)
	sh = wb[sheet_name]

	sh["f"+str(1)].value = "gi"
	sh["g"+str(1)].value = "kw"
	i=2
	while True:
		try:
			ae_id = str(sh["a"+str(i)].value).split(".")[0]
			if ae_id == "None":
				break
			sh["f"+str(i)].value = data[ae_id][0]
			sh["g"+str(i)].value = data[ae_id][1]
			i+=1
		except Exception as e:
			print(e)
			i+=1
			continue

	wb.save(tpath)


def get_categories_dict(root):
	categories = {}
	for cat in get_categories(root):
		id = cat.attrib["id"]
		name = cat.text
		categories.setdefault(id,name)
	return categories
