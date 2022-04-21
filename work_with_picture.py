import glob
import os
from PIL import Image, ImageDraw
import requests
import lxml.etree as xml
import my_functions.functions as f


def load_pics(root,path2,coupon_name,opath="./original_pic"):
	offers = root.find("shop").find("offers").findall("offer")
	#opath = "./original_pic"
	for offer in offers:
		
		id = str(offer.attrib["id"])
		pic_url = str(offer.find("plashka").text)
		try:
			coupon = str(offer.attrib[coupon_name])
		except Exception as e:
			continue
		xml.SubElement(offer,"plashka2").text = pic_url
		path = opath+"/"+id+"_"+coupon_name+"_"+str(coupon)+".jpg"
		
		load_one_picture(pic_url,path)

	f.make_correctXML(root,path2)

def load_one_picture(url,path,id):
	
	try:
		with open(path, 'wb') as handle:
			response = requests.get(url, stream=True)

			if not response.ok:
				print(response, id)

			for block in response.iter_content(1024):
				if not block:
					break

				handle.write(block)
		handle.close()
	except Exception as e:
		print(e,id)


def resize_pics(input_image_path,output_image_path):
	pics = []
	#plashka = "плашка.png"
	#pl = Image.open(plashka,"r")
	for filename in glob.glob(os.path.join(input_image_path,'*.jpg')):
		pics.append(filename)

	for pic in pics:
		try:
			img = Image.open(pic)
			back = None
			width, height = img.size
			if width > height:
				temp = Image.new('RGB', (width, width), 'white')
				temp.save("background.png")
				temp.close()
				back = Image.open("background.png","r")
				back.paste(img, (0,int((width-height)/2)))
			elif width == height:
				temp = Image.new('RGB', (width, width), 'white')
				temp.save("background.png")
				temp.close()
				back = Image.open("background.png","r")
				back.paste(img, (0, 0))
			else:
				temp = Image.new('RGB', (height, height), 'white')
				temp.save("background.png")
				temp.close()
				back = Image.open("background.png","r")
				back.paste(img, (int((height-width)/2),0))

			
			back.save(output_image_path+pic.split("\\")[-1])
		except Exception as e:
			print(pic,e)
			continue


def reduce_pics(input_image_path,output_image_path):
	pics = []
	#plashka = "плашка.png"
	#pl = Image.open(plashka,"r")
	for filename in glob.glob(os.path.join(input_image_path,'*.jpg')):
		pics.append(filename)

	for pic in pics:
		try:
			img = Image.open(pic)
			back = None
			width, height = (800,800)
			
			temp = Image.new('RGB', (width, width), 'white')
			temp.save("background.png")
			temp.close()
			back = Image.open("background.png","r")
			back.paste(img, (150,150))
			
			back.save(output_image_path+pic.split("\\")[-1])
		except Exception as e:
			print(pic,e)
			continue

def scale_image(input_image_path,
				output_image_path,
				width=None,
				height=None
				):
	original_image = Image.open(input_image_path)
	w, h = original_image.size
	print('The original image size is {wide} wide x {height} '
		  'high'.format(wide=w, height=h))
 
	if width and height:
		max_size = (width, height)
	elif width:
		max_size = (width, h)
	elif height:
		max_size = (w, height)
	else:
		# No width or height specified
		raise RuntimeError('Width or height required!')
 
	original_image.thumbnail(max_size, Image.ANTIALIAS)
	original_image.convert('RGB').save(output_image_path)
 
	scaled_image = Image.open(output_image_path)
	width, height = scaled_image.size
	print('The scaled image size is {wide} wide x {height} '
		  'high'.format(wide=width, height=height))


def resize_image(input_image_path,
				 output_image_path,
				 size:tuple):
	original_image = Image.open(input_image_path)
	width, height = original_image.size
	print('The original image size is {wide} wide x {height} '
		  'high'.format(wide=width, height=height))
 
	resized_image = original_image.resize(size)
	width, height = resized_image.size
	print('The resized image size is {wide} wide x {height} '
		  'high'.format(wide=width, height=height))
	#resized_image.show()
	resized_image.save(output_image_path)

def resize_image_procces(input_image_path,output_image_path,size=(800,800)):
	pics = []
	for filename in glob.glob(os.path.join(input_image_path,'*.jpg')):
		pics.append(filename)
		
	for pic in pics:
		resize_image(pic,output_image_path+pic.split("\\")[-1],size)

def set_background(input_image_path,output_image_path,back_folder:str):

	pics = []
	for filename in glob.glob(os.path.join(input_image_path,'*.jpg')):
		pics.append(filename)

	for pic in pics:
		plashka = back_folder+pic.split("_")[-1].split(".")[0] + ".png"
		pl = Image.open(plashka,"r").convert("RGBA")
		pix = (pl.load())
		alpha = pl.split()[-1]
		
		img = Image.open(pic,"r").convert("RGBA")
		width, height = img.size
		
		

		for x in range(width):
			for y in range(height):
				pl_pix = pix[x,y]
				#print(pl_pix)
				r = pl_pix[0]
				g = pl_pix[1]
				b = pl_pix[2]
				a = pl_pix[3]
				if r!=255 and g!=255 and b!=255 and a!=0:
					img.putpixel((x,y),pl_pix)#draw.point((x,y),pl_pix)#
				else:
					continue
		#img.putalpha(alpha)
		alpha = img.split()[-1]
		background = Image.new("RGB", img.size, (255, 255, 255))
		background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
		background.save(output_image_path+pic.split("\\")[-1])
		#input()