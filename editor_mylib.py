from lxml import etree as xml
from bs4 import BeautifulSoup as bs
import json
import my_functions.functions as f
from openpyxl import load_workbook as lwb


def set_elem(offer,name,text):
	try:
		offer.find(name).text = text
	except Exception as e:
		xml.SubElement(offer,name).text = text

def set_picture(offer,orig_offer):
	name = "picture"
	try:
		offer.find(name).text
	except Exception as e:
		pics = orig_offer.findall(name)
		for pic in pics:
			xml.SubElement(offer,name).text = pic.text

def set_desc(offer,orig_offer):
	name = "description"
	try:
		offer.find(name).text

	except Exception as e:
		desc = str(orig_offer.find(name).text)
		
		#i1 = desc.find("<table")
		#i2 = desc.find("</table>")
		
		#desc = "".join((desc[:i1] + desc[i2+len("</table>"):]).split("<p style=\"font-size:24px; text-align:left; margin:25px 10px;font-weight:bolder;\">Характеристики</p>"))
		#print(desc)

		xml.SubElement(offer,name).text = xml.CDATA(desc)

def edit_structure(root,path,prefix_for_id=""):
	originOffers = root.find("shop").find("offers").findall("offer")
	originCategories = root.find("shop").find("categories").findall("category")
	
	yml_catalog = xml.Element("yml_catalog")
	shop = xml.SubElement(yml_catalog,"shop")
	offers = xml.SubElement(shop,"offers")

	data = {}

	for offer in originOffers:
		try:
			gi = str(offer.attrib["group_id"])
		except Exception as e:
			print("no find in ",gi,"->",e,sep="\t")
			continue
		if gi not in data:
			data.setdefault(gi,1)
		else:
			data[gi]+=1

	#print(json.dumps(data,indent=2))
	colors = []
	ignore_id=[]
	for elem in data:
		offer = xml.SubElement(offers,"offer",attrib={"spu":""})
		for i in range(data[elem]):
			for orig_offer in originOffers:
				id = str(orig_offer.attrib["id"])
				try:
					gi = str(orig_offer.attrib["group_id"])
				except Exception as e:
					print("no find in ",gi,"->",e,sep="\t")
					continue
				if id in ignore_id:
					continue
				if elem != gi:
					continue
				else:
					try:
						name = "price"
						text = orig_offer.find(name).text
					except Exception as e:
						continue

					#print(elem,i+1,sep="\t")
					offer.attrib["spu"] = gi

					name = "name"
					text = orig_offer.find(name).text
					set_elem(offer,name,text)
					
					try:
						name = "url"
						text = orig_offer.find(name).text
						set_elem(offer,name,text)
					except Exception as e:
						print("no find in ",gi,name,"->",e,sep="\t")
					
					name = "categoryId"
					text = orig_offer.find(name).text
					set_elem(offer,name,text)
					try:
						offer.find(name).attrib["ae_category_id"] = orig_offer.find(name).attrib["ae_category_id"]
					except Exception as e:
						print("no find in ",gi,name,"->",e,sep="\t")

					name = "vendor"
					text = orig_offer.find(name).text
					set_elem(offer,name,text)
					
					try:
						name = "country_of_origin"
						text = orig_offer.find(name).text
						set_elem(offer,name,text)
					except Exception as e:
						print("no find in ",gi,name,"->",e,sep="\t")
						
					name = "weight"
					text = orig_offer.find(name).text
					set_elem(offer,name,text)

					name = "length"
					text = orig_offer.find(name).text
					set_elem(offer,name,text)

					name = "width"
					text = orig_offer.find(name).text
					set_elem(offer,name,text)

					name = "height"
					text = orig_offer.find(name).text
					set_elem(offer,name,text)

					name = "desc_mob"
					text = orig_offer.find(name).text
					set_elem(offer,name,text)

					set_picture(offer,orig_offer)

					set_desc(offer,orig_offer)

					sku = xml.SubElement(offer,"sku",attrib={"id": prefix_for_id + id})
					ignore_id.append(id)

					name = "price"
					text = orig_offer.find(name).text
					set_elem(sku,name,text)

					name = "quantity"
					text = orig_offer.find(name).text
					set_elem(sku,name,text)
					
					try:
						name = "barcode"
						text = orig_offer.find(name).text
						set_elem(sku,name,text)
					except Exception as e:
						print(e)
						
					try:
						name = "picture"
						text = orig_offer.find(name).text
						set_elem(sku,name,text)
					except Exception as e:
						print(e)
					
					params = orig_offer.findall("param")
					for param in params:
						try:
							name = str(param.attrib["name"]) 
							if name == "Материалы":
								xml.SubElement(sku,"param",attrib={"name":str(param.attrib["name"]),"ae_code": "10"}).text = str(param.text)
							elif name == "Состав":
								xml.SubElement(sku,"param",attrib={"name":str(param.attrib["name"]),"ae_code": "10"}).text = str(param.text)
							#elif name == "Цвет":
								#color = str(param.text)
								#if color not in colors:
									#colors.append(color)
							else:
								xml.SubElement(sku,"param",attrib={"name":str(param.attrib["name"]),"ae_code": str(param.attrib["ae_code"])}).text = str(param.text)
						except Exception as e:
							xml.SubElement(sku,"param",attrib={"name":str(param.attrib["name"])}).text = str(param.text)
					break
	print(colors)
	f.make_correctXML(yml_catalog,path)

def write_size(root):
	sizes = [
								{
									"value_tags": "{}", 
									"id": 200844084, 
									"names": "{\"en\":\"1000mm x 1900mm\",\"zh\":\"1000mm*1900mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844085, 
									"names": "{\"en\":\"1000mm x 2000mm\",\"zh\":\"1000mm*2000mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844086, 
									"names": "{\"en\":\"1200mm x 1900mm\",\"zh\":\"1200mm*1900mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844087, 
									"names": "{\"en\":\"1200mm x 2000mm\",\"zh\":\"1200mm*2000mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844088, 
									"names": "{\"en\":\"1350mm x 1900mm\",\"zh\":\"1350mm*1900mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844089, 
									"names": "{\"en\":\"1350mm x 2000mm\",\"zh\":\"1350mm*2000mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844444, 
									"names": "{\"en\":\"1500*2000*230MM\",\"zh\":\"150*200*23CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844445, 
									"names": "{\"en\":\"1500*2000*250MM\",\"zh\":\"150*200*25CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844446, 
									"names": "{\"en\":\"1500*2000*280MM\",\"zh\":\"150*200*28CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844447, 
									"names": "{\"en\":\"1500*2000*300MM\",\"zh\":\"150*200*30CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844090, 
									"names": "{\"en\":\"1500mm x 1900mm\",\"zh\":\"1500mm*1900mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844091, 
									"names": "{\"en\":\"1500mm x 2000mm\",\"zh\":\"1500mm*2000mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844448, 
									"names": "{\"en\":\"1600*2000*230MM\",\"zh\":\"160*200*23CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844449, 
									"names": "{\"en\":\"1600*2000*250MM\",\"zh\":\"160*200*25CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844450, 
									"names": "{\"en\":\"1600*2000*280MM\",\"zh\":\"160*200*28CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844451, 
									"names": "{\"en\":\"1600*2000*300MM\",\"zh\":\"160*200*30CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844452, 
									"names": "{\"en\":\"1800*2000*150MM\",\"zh\":\"180*200*15CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844453, 
									"names": "{\"en\":\"1800*2000*230MM\",\"zh\":\"180*200*23CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844454, 
									"names": "{\"en\":\"1800*2000*250MM\",\"zh\":\"180*200*25CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844455, 
									"names": "{\"en\":\"1800*2000*280MM\",\"zh\":\"180*200*28CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844456, 
									"names": "{\"en\":\"1800*2000*300MM\",\"zh\":\"180*200*30CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844092, 
									"names": "{\"en\":\"1800mm x 1900mm\",\"zh\":\"1800mm*1900mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844093, 
									"names": "{\"en\":\"1800mm x 2000mm\",\"zh\":\"1800mm*2000mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844457, 
									"names": "{\"en\":\"2000*2000*230MM\",\"zh\":\"200*200*23CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844458, 
									"names": "{\"en\":\"2000*2000*250MM\",\"zh\":\"200*200*25CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844459, 
									"names": "{\"en\":\"2000*2000*280MM\",\"zh\":\"200*200*28CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844460, 
									"names": "{\"en\":\"500mm x 1000mm\",\"zh\":\"500mm*1000mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844461, 
									"names": "{\"en\":\"600mm x 1000mm\",\"zh\":\"600mm*1000mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844462, 
									"names": "{\"en\":\"600mm x 1150mm\",\"zh\":\"600mm*1150mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844463, 
									"names": "{\"en\":\"600mm x 1200\",\"zh\":\"600mm*1200\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844464, 
									"names": "{\"en\":\"700mm x 1300mm\",\"zh\":\"700mm*1300mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844465, 
									"names": "{\"en\":\"700mm x 1400mm\",\"zh\":\"700mm*1400mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844366, 
									"names": "{\"en\":\"800mm x 1900mm\",\"zh\":\"800mm*1900mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844367, 
									"names": "{\"en\":\"800mm x 2000mm\",\"zh\":\"800mm*2000mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844466, 
									"names": "{\"en\":\"900*2000*150MM\",\"zh\":\"90*200*15CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844467, 
									"names": "{\"en\":\"900*2000*230C\",\"zh\":\"90*200*23C\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844468, 
									"names": "{\"en\":\"900*2000*250MM\",\"zh\":\"90*200*25CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844469, 
									"names": "{\"en\":\"900*2000*280MM\",\"zh\":\"90*200*28CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844470, 
									"names": "{\"en\":\"900*2000*300MM\",\"zh\":\"90*200*30CM\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844368, 
									"names": "{\"en\":\"900mm x 1900mm\",\"zh\":\"900mm*1900mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200844369, 
									"names": "{\"en\":\"900mm x 2000mm\",\"zh\":\"900mm*2000mm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446869, 
									"names": "{\"en\":\"100x170cm\",\"zh\":\"100x170cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446870, 
									"names": "{\"en\":\"100x190cm\",\"zh\":\"100x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446871, 
									"names": "{\"en\":\"100x200cm\",\"zh\":\"100x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446872, 
									"names": "{\"en\":\"110x190cm\",\"zh\":\"110x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446873, 
									"names": "{\"en\":\"110x200cm\",\"zh\":\"110x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446874, 
									"names": "{\"en\":\"120x190cm\",\"zh\":\"120x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446875, 
									"names": "{\"en\":\"120x200cm\",\"zh\":\"120x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446710, 
									"names": "{\"en\":\"120x60cm\",\"zh\":\"120x60cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446876, 
									"names": "{\"en\":\"120x90cm\",\"zh\":\"120x90cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446877, 
									"names": "{\"en\":\"130x190cm\",\"zh\":\"130x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446878, 
									"names": "{\"en\":\"130x200cm\",\"zh\":\"130x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446715, 
									"names": "{\"en\":\"140x190cm\",\"zh\":\"140x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446422, 
									"names": "{\"en\":\"140x200cm\",\"zh\":\"140x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446879, 
									"names": "{\"en\":\"140x220cm\",\"zh\":\"140x220cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446709, 
									"names": "{\"en\":\"140x60cm\",\"zh\":\"140x60cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446730, 
									"names": "{\"en\":\"140x70cm\",\"zh\":\"140x70cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446880, 
									"names": "{\"en\":\"150x190cm\",\"zh\":\"150x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200011727, 
									"names": "{\"en\":\"150x200cm\",\"zh\":\"150x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446881, 
									"names": "{\"en\":\"160x190cm\",\"zh\":\"160x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446421, 
									"names": "{\"en\":\"160x200cm\",\"zh\":\"160x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200011737, 
									"names": "{\"en\":\"160x210cm\",\"zh\":\"160x210cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446882, 
									"names": "{\"en\":\"160x220cm\",\"zh\":\"160x220cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446883, 
									"names": "{\"en\":\"165x90cm\",\"zh\":\"165x90cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446884, 
									"names": "{\"en\":\"170x140cm\",\"zh\":\"170x140cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446885, 
									"names": "{\"en\":\"170x170cm\",\"zh\":\"170x170cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446886, 
									"names": "{\"en\":\"170x190cm\",\"zh\":\"170x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446887, 
									"names": "{\"en\":\"170x200cm\",\"zh\":\"170x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446888, 
									"names": "{\"en\":\"170x90cm\",\"zh\":\"170x90cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446717, 
									"names": "{\"en\":\"180x190cm\",\"zh\":\"180x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200011731, 
									"names": "{\"en\":\"180x200cm\",\"zh\":\"180x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200011738, 
									"names": "{\"en\":\"180x210cm\",\"zh\":\"180x210cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 200011739, 
									"names": "{\"en\":\"180x220cm\",\"zh\":\"180x220cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446889, 
									"names": "{\"en\":\"180x80cm\",\"zh\":\"180x80cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446890, 
									"names": "{\"en\":\"180x90cm\",\"zh\":\"180x90cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446891, 
									"names": "{\"en\":\"185x85cm\",\"zh\":\"185x85cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446892, 
									"names": "{\"en\":\"185x90cm\",\"zh\":\"185x90cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446727, 
									"names": "{\"en\":\"190x100cm\",\"zh\":\"190x100cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446725, 
									"names": "{\"en\":\"190x110cm\",\"zh\":\"190x110cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446723, 
									"names": "{\"en\":\"190x120cm\",\"zh\":\"190x120cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446722, 
									"names": "{\"en\":\"190x130cm\",\"zh\":\"190x130cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446720, 
									"names": "{\"en\":\"190x150cm\",\"zh\":\"190x150cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446714, 
									"names": "{\"en\":\"190x160cm\",\"zh\":\"190x160cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446719, 
									"names": "{\"en\":\"190x170cm\",\"zh\":\"190x170cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446708, 
									"names": "{\"en\":\"190x60cm\",\"zh\":\"190x60cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446713, 
									"names": "{\"en\":\"190x80cm\",\"zh\":\"190x80cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446711, 
									"names": "{\"en\":\"190x90cm\",\"zh\":\"190x90cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446893, 
									"names": "{\"en\":\"195x130cm\",\"zh\":\"195x130cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446894, 
									"names": "{\"en\":\"195x160cm\",\"zh\":\"195x160cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446895, 
									"names": "{\"en\":\"195x85cm\",\"zh\":\"195x85cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446726, 
									"names": "{\"en\":\"200x100cm\",\"zh\":\"200x100cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446724, 
									"names": "{\"en\":\"200x110cm\",\"zh\":\"200x110cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446423, 
									"names": "{\"en\":\"200x120cm\",\"zh\":\"200x120cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446721, 
									"names": "{\"en\":\"200x130cm\",\"zh\":\"200x130cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446718, 
									"names": "{\"en\":\"200x170cm\",\"zh\":\"200x170cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446896, 
									"names": "{\"en\":\"200x190cm\",\"zh\":\"200x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446716, 
									"names": "{\"en\":\"200x200cm\",\"zh\":\"200x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446769, 
									"names": "{\"en\":\"200x220cm\",\"zh\":\"200x220cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446712, 
									"names": "{\"en\":\"200x80cm\",\"zh\":\"200x80cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446424, 
									"names": "{\"en\":\"200x90cm\",\"zh\":\"200x90cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446897, 
									"names": "{\"en\":\"200x95cm\",\"zh\":\"200x95cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446898, 
									"names": "{\"en\":\"210x110cm\",\"zh\":\"210x110cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446899, 
									"names": "{\"en\":\"210x120cm\",\"zh\":\"210x120cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446900, 
									"names": "{\"en\":\"210x135cm\",\"zh\":\"210x135cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446901, 
									"names": "{\"en\":\"210x140cm\",\"zh\":\"210x140cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446729, 
									"names": "{\"en\":\"210x90cm\",\"zh\":\"210x90cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446902, 
									"names": "{\"en\":\"220x100cm\",\"zh\":\"220x100cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446903, 
									"names": "{\"en\":\"220x110cm\",\"zh\":\"220x110cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446904, 
									"names": "{\"en\":\"220x120cm\",\"zh\":\"220x120cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446905, 
									"names": "{\"en\":\"220x140cm\",\"zh\":\"220x140cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446906, 
									"names": "{\"en\":\"220x145cm\",\"zh\":\"220x145cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446728, 
									"names": "{\"en\":\"220x90cm\",\"zh\":\"220x90cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446907, 
									"names": "{\"en\":\"230x200cm\",\"zh\":\"230x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446908, 
									"names": "{\"en\":\"60x120cm\",\"zh\":\"60x120cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446909, 
									"names": "{\"en\":\"80x190cm\",\"zh\":\"80x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446910, 
									"names": "{\"en\":\"80x195cm\",\"zh\":\"80x195cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446911, 
									"names": "{\"en\":\"80x200cm\",\"zh\":\"80x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446912, 
									"names": "{\"en\":\"85x190cm\",\"zh\":\"85x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446913, 
									"names": "{\"en\":\"85x195cm\",\"zh\":\"85x195cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446707, 
									"names": "{\"en\":\"90x200cm\",\"zh\":\"90x200cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446914, 
									"names": "{\"en\":\"90x170cm\",\"zh\":\"90x170cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446915, 
									"names": "{\"en\":\"90x190cm\",\"zh\":\"90x190cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 201446916, 
									"names": "{\"en\":\"90x220cm\",\"zh\":\"90x220cm\"}"
								}, 
								{
									"value_tags": "{}", 
									"id": 4, 
									"names": "{\"en\":\"Other\",\"zh\":\"\u5176\u5b83\"}"
								}
							]
	colors = ['Мультиколор', 'Белый, Синий, Шоколад, Бежевый, Серый, Чёрный', 'Белый', 'Бежевый', 'Серый', 'Синий', 'Чёрный', 'Шоколад']
	path = "size.xlsx"
	wb = lwb(path)
	sh = f.get_sheet(wb,"Лист1")

	i=2
	'''
	sizes = []
	offers = root.find("shop").find("offers").findall("offer")
	for offer in offers:
		spu = str(offer.attrib["spu"])
		for sku in offer.findall("sku"):
			for param in sku.findall("param"):
				if str(param.attrib["name"]) == "Размер":
					size = str(param.text)
					if size not in sizes:
						sizes.append(size)
	'''

	for size in sizes:
		temp = size["names"]
		sh["h"+str(i)].value = json.loads(temp)["en"]
		sh["i"+str(i)].value = str(size["id"])
		i+=1

	wb.save(path)
	
def set_size(root):
	wb = lwb("ОНЛАЙНМАРКЕТ_catalog.xlsx")
	sh = wb.get_sheet_by_name("димакс_размеры")
	
	data = {}
	i=2
	while True:
		size = str(sh["a"+str(i)].value)
		if size == "None":
			break
		id = str(sh["b"+str(i)].value)
		
		data.setdefault(size,id)
		i+=1
	
	offers = root.find("shop").find("offers").findall("offer")
	for offer in offers:
		try:
			desc = "".join(str(offer.find("description").text).split("\n"))
			offer.find("description").text = xml.CDATA(desc)
		except Exception as e:
			print(offer.attrib["spu"])
			print(offer.attrib["spu"],e,sep="\t\t")
		for sku in offer.findall("sku"):
			for param in sku.findall("param"):
				name = str(param.attrib["name"])
				if name == "Размер":
					val = str(param.text)
					try:
						param.attrib["ae_code_value"] = (data[val]).split(".")[0]
					except Exception as e:
						print(offer.attrib["spu"],sku.attrib["id"],e,sep="\t\t")
				else:
					continue
	f.make_correctXML(root,"dimax_new_fid2.xml")
	
