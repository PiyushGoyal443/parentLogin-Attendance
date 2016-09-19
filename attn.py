def get_atten(reg_no = "", pwd = "", mob_num = ""):

	
	import mechanize, json, datetime, pytz
	from bs4 import BeautifulSoup
	from CaptchaParser import CaptchaParser
	from PIL import Image
		  
	
	#browser initialise
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)

	#open website

	# response = br.open("https://academics.vit.ac.in/student/stud_login.asp")
	response = br.open("https://vtop.vit.ac.in/parent/parent_login.asp")
	print br.geturl()

	#select form
	br.select_form("parent_login")

	
	#extracting captcha url
	soup = BeautifulSoup(response.get_data())
	img = soup.find('img', id='imgCaptcha')
	
	
	#retrieving captcha image
	br.retrieve("https://vtop.vit.ac.in/parent/"+img['src'], "captcha_parent.bmp")
	
	# print str("https://academics.vit.ac.in/parent/"+img['src'], "captcha_parent")

	img = Image.open("captcha_parent.bmp")

	parser = CaptchaParser()

	captcha = parser.getCaptcha(img)   
	
	#fill form
	br["wdregno"] = str(reg_no)
	br["wdpswd"] = str(pwd)
	br["wdmobno"] = str(mob_num)
	br["vrfcd"] = str(captcha)
	br.method = "POST"
	br.submit()
	if br.geturl()==("https://vtop.vit.ac.in/parent/home.asp"):
		print "SUCCESS"
		
		#attendance page 
		months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
		atten = {}
		br.open("https://vtop.vit.ac.in/parent/attn_report.asp?sem=WS")
		response = br.open("https://vtop.vit.ac.in/parent/attn_report.asp?sem=WS")
		soup = BeautifulSoup(response.get_data())

		br.select_form(nr=0)
		inputTag = soup.find(attrs={"name": "from_date"})
		from_date = inputTag['value']
		tz = pytz.timezone('Asia/Kolkata')
		now = datetime.datetime.now(tz)
		to_date = str(now.day) + "-" + months[now.month] + "-" + str(now.year)
		
		response = br.open("https://vtop.vit.ac.in/parent/attn_report.asp?sem=WS&fmdt=%(from_date)s&todt=%(to_date)s" % {"from_date":from_date, "to_date":to_date} )
		soup = BeautifulSoup(response.get_data())
		tables = soup.findAll("table")
		trs = soup.findAll("table")[len(tables)-2].findAll("tr")
		for i in range(1,len(trs)): #it should be len(trs) -1 but it works w/o -1
			a_course_code = soup.findAll("table")[len(tables)-2].findAll("tr")[i].findAll("td")[1].getText().encode('utf-8').replace("\xc2\xa0", " ")
			a_attend_percentage =  soup.findAll("table")[len(tables)-2].findAll("tr")[i].findAll("td")[8].getText().encode('utf-8').replace("\xc2\xa0", " ")
			if a_course_code not in atten.keys():
				atten[a_course_code] = [a_attend_percentage]
			else:
				atten[a_course_code+"_L"] = [a_attend_percentage]

		return {"Status" : "sucess" , "attendance" : atten}
