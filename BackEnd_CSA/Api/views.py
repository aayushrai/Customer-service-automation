from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http.response import StreamingHttpResponse
from .models import User,UserSerializer,Product,ProductSerializer,Order,OrderSerializer
from rest_framework.parsers import JSONParser
import uuid
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

face_dis_flag = False
result = []
@api_view(["GET"])
def userData(request):
	global result
	if face_dis_flag:
		result =[]
		for name,idd,dis in sorted(zip(known_names,known_id,distance), key=lambda item: item[2]):
			if dis < .6:
				result.append(User.objects.get(user_id=idd))
	serilizeResult = UserSerializer(result,many=True)
	return Response(serilizeResult.data)

@api_view(["GET"])
def productData(request):
	result = Product.objects.all()
	productResult = ProductSerializer(result,many=True)
	return Response(productResult.data)

def emailTemplate(orderInfo):
	product = ""
	total = 0 
	for order in orderInfo:
		total += order.product.price * (order.product_quantity)
		product += """ <tr>
            <td class="service">{}</td>
            <td class="desc">{}</td>
            <td class="unit">{}</td>
            <td class="qty">{}</td>
            <td class="total">{}</td>
          </tr>""".format(order.product.title,order.product.description,order.product.price,order.product_quantity,order.product.price * (order.product_quantity))
		  
	html = '''
	<!DOCTYPE html>
	<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Example 1</title>
    <link rel="stylesheet" href="style.css" media="all" />
	<style>
	a {
  color: #5D6975;
  text-decoration: underline;
}

body {
  position: relative;
  width: 21cm;  
  height: 29.7cm; 
  margin: 0 auto; 
  color: #001028;
  background: #FFFFFF; 
  font-family: Arial, sans-serif; 
  font-size: 12px; 
  font-family: Arial;
}

header {
  padding: 10px 0;
  margin-bottom: 30px;
}

#logo {
  text-align: center;
  margin-bottom: 10px;
}

#logo img {
  width: 90px;
}

h1 {
  border-top: 1px solid  #5D6975;
  border-bottom: 1px solid  #5D6975;
  color: #5D6975;
  font-size: 2.4em;
  line-height: 1.4em;
  font-weight: normal;
  text-align: center;
  margin: 0 0 20px 0;
  background: url(dimension.png);
}

#project {
  float: left;
}

#project span {
  color: #5D6975;
  text-align: right;
  width: 52px;
  margin-right: 10px;
  display: inline-block;
  font-size: 0.8em;
}

#company {
  float: right;
  text-align: right;
}

#project div,
#company div {
  white-space: nowrap;        
}

table {
  width: 100%;
  border-collapse: collapse;
  border-spacing: 0;
  margin-bottom: 20px;
}

table tr:nth-child(2n-1) td {
  background: #F5F5F5;
}

table th,
table td {
  text-align: center;
}

table th {
  padding: 5px 20px;
  color: #5D6975;
  border-bottom: 1px solid #C1CED9;
  white-space: nowrap;        
  font-weight: normal;
}

table .service,
table .desc {
  text-align: left;
}

table td {
  padding: 20px;
  text-align: right;
}

table td.service,
table td.desc {
  vertical-align: top;
}

table td.unit,
table td.qty,
table td.total {
  font-size: 1.2em;
}

table td.grand {
  border-top: 1px solid #5D6975;;
}

#notices .notice {
  color: #5D6975;
  font-size: 1.2em;
}

footer {
  color: #5D6975;
  width: 100%;
  height: 30px;
  position: absolute;
  bottom: 0;
  border-top: 1px solid #C1CED9;
  padding: 8px 0;
  text-align: center;
}
	</style>
  </head>
	<body>
		<header class="clearfix">
		<h1>INVOICE</h1>
		<div id="company" class="clearfix">
			<div>WE MEGA MART</div>
			<div><a href="dummy21072000@gmail.com">dummy21072000@gmail.com</a></div>
		</div>
		<div id="project">
			<div><span>Order ID </span>'''+ orderInfo[0].order_id+'''</div>
			<div><span>CLIENT</span> '''+orderInfo[0].user.user_name +'''</div>
			<div><span>ADDRESS</span> '''+orderInfo[0].user.user_address +'''</div>
			<div><span>EMAIL</span> <a href="'''+orderInfo[0].user.user_email +'''">'''+orderInfo[0].user.user_email +'''</a></div>
			<div><span>DATE</span>'''+ now.strftime("%d/%m/%Y %H:%M:%S") +'''</div>
		</div>
		</header>
		<main>
		<table>
			<thead>
			<tr>
				<th class="service">PRODUCT NAME>
				<th class="desc">DESCRIPTION</th>
				<th>PRICE</th>
				<th>QTY</th>
				<th>TOTAL</th>
			</tr>
			</thead>
			<tbody>
		    '''+product+'''
			<tr>
				<td colspan="4" class="grand total">GRAND TOTAL</td>
				<td class="grand total"> '''+ str(total) +'''</td>
			</tr>
			</tbody>
		</table>
		</main>
		<footer>
		Invoice was created on a computer and is valid without the signature and seal.
		</footer>
	</body>
	</html>'''
	return html

#https://www.google.com/settings/security/lesssecureapps
def sendEmail(order_id):
	order_info = Order.objects.filter(order_id=order_id)
	user_info = order_info[0].user
	receiver_email = user_info.user_email
	print(receiver_email)
	sender_email = "dummy21072000@gmail.com"
	password = "Aayush#21"
	message = MIMEMultipart("alternative")
	message["Subject"] = "WE MEGA MART BILL"
	message["From"] = sender_email
	html = emailTemplate(order_info)
	text = "hloo"
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")

	message.attach(part1)
	message.attach(part2)
	context = ssl.create_default_context()
	if receiver_email:
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
				print("Sending emails")
				server.login(sender_email, password)
				message["To"] = receiver_email
				server.sendmail(sender_email, receiver_email, message.as_string())
	else:
		print("No Emails")

@api_view(["POST"])
def PlaceOrder(request):
	print(request.data)
	order_details = request.data
	order_id = uuid.uuid4()
	orders = []
	for order in order_details:
		user = User.objects.get(user_id=order["user_id"])
		product = Product.objects.get(product_id=order["product_id"])
		#update quantity of product
		new_quantity = product.quantity - order["product_quantity"]
		if new_quantity < 0:
			product.quantity = 0
		else:
			product.quantity = new_quantity
		product.save()
		orders.append(
			Order(
				user=user,
				product=product,
				order_id=order_id,
				product_quantity=order["product_quantity"]
			)
		)
	user = User.objects.get(user_id=order_details[0]["user_id"])
	user.order_count = user.order_count + 1
	user.save()
	Order.objects.bulk_create(orders)
	sendEmail(order_id)
	return Response({"order_id":order_id})

@api_view(["GET"])
def orderInfo(request,order_id):
	order_info = Order.objects.filter(order_id=order_id)
	user_info = order_info[0].user
	result = []
	serilizeOrderInfo = OrderSerializer(order_info,many=True).data
	for order in serilizeOrderInfo:
		productDis = ProductSerializer(Product.objects.get(id=order["product"])).data
		dis = {} 	
		for key,value in order.items():
			dis[key] = value
		for key,value in productDis.items():
			dis[key] = value
		result.append(dis)
	serilizeUserInfo = UserSerializer(user_info)
	print(serilizeUserInfo.data)
	return Response([serilizeUserInfo.data] + result)
def loadData(request):
	import pandas as pd
	df = pd.read_csv('Api/assets/customer.csv')
	products = []
	for i in range(len(df)):
		products.append(
			Product(
			title=df.iloc[i]["Product Name"],
			description=df.iloc[i]["Product details"],
			logo=df.iloc[i]["Image"],
			category=df.iloc[i]["Category"],
			price=df.iloc[i]["Price"][3:],
			weight=df.iloc[i]["Weight"],
			quantity=df.iloc[i]["Quantity"]
			
			)
		)
	Product.objects.bulk_create(products)
	return Response({"status":"Data loaded"})


def framesGenerator(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def videoStream(request):
    url = 0
    camera = VideoCamera(url)
    return StreamingHttpResponse(framesGenerator(camera),
                        content_type='multipart/x-mixed-replace; boundary=frame')
                    

#================================================FACE RECOGNITION PART===============================================================#


import face_recognition
from imutils.video import VideoStream
import cv2,os
load_encodings = False
face_cascade = cv2.CascadeClassifier('Api/assets/haarcascade_frontalface_default.xml')

class VideoCamera():

	def __init__(self,url):
		global load_encodings
		self.url = url
		self.video=VideoStream(src=self.url).start()
		if not load_encodings:
			VideoCamera.update_encoding()
			load_encodings=True
	
	@staticmethod
	def update_encoding():
		global known_names,known_faces,net,known_id
		known_names=[]
		known_faces=[]
		known_id = []
		print("Loading Encoding")
		UNKNOWN_DIR = "Api/Faces/"
		# for name in os.listdir(UNKNOWN_DIR):
		# 	FOLDER = os.path.join(UNKNOWN_DIR, name)
		# 	for filename in os.listdir(FOLDER):
		users = User.objects.all()
		print(users)
		for user in users:
			image = face_recognition.load_image_file(user.user_image)
			
			location = []
			faces = face_cascade.detectMultiScale(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 1.05, 5)
			for (x,y,w,h) in faces:
				(startX, startY, endX, endY) = x,y,x+w,y+h
				if (startX + 5 < endX) and (startY + 5 < endY): 
						location.append((startY,endX,endY,startX))
			if len(location)>0:
				encoding = face_recognition.face_encodings(image, known_face_locations=location)[0]
				known_faces.append(encoding)
				known_names.append(user.user_name)
				known_id.append(user.user_id)
			else:
				print(name,": Face not found in image" )

	def __del__(self):
		self.video.stop()
    
	def face_detection(self,image):
		rects = []
	
		self.face_cascade = cv2.CascadeClassifier('Api/assets/haarcascade_frontalface_default.xml')
		faces = self.face_cascade.detectMultiScale(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 1.05, 5)
		for (x,y,w,h) in faces:
			(startX, startY, endX, endY) = x,y,x+w,y+h
			if (startX + 5 < endX) and (startY + 5 < endY): 
					rects.append((startY,endX,endY,startX))
		return rects

	
	def face_recog(self):
		global known_names,known_faces
		image = self.frame
		image2 = self.frame.copy()
		#locations = face_recognition.face_locations(image2, number_of_times_to_upsample=3,model="hog")
		rects = self.face_detection(image2)

		encodings = face_recognition.face_encodings(image2, rects)
		
		for face_encoding, face_location in zip(encodings, rects):
			(startY,endX,endY,startX) = face_location
			crop_image=image2[startY-30:endY+30,startX-30:endX+30,:]
			crop_image_H,crop_image_W,crop_image_C=crop_image.shape
			if crop_image_H>5 and crop_image_W>5:

				face_rect = self.face_detection(crop_image)
				# print(face_rect)
				if len(face_rect)==1:
					results = face_recognition.compare_faces(known_faces, face_encoding,tolerance=0.6)
					global distance,face_dis_flag
					distance = face_recognition.face_distance(known_faces,face_encoding)
					face_dis_flag = True
					match = None
					if True in results:
						match = known_names[results.index(True)]
						# print(f"Match Found:", {match})
					else:
						match = "Unknown"
			
				

					top_left = (face_location[3], face_location[0])
					bottom_right = (face_location[1], face_location[2])

					color = [0, 255, 0]

					cv2.rectangle(image, top_left, bottom_right, 1)

					top_left = (face_location[3], face_location[0])
					bottom_right = (face_location[1], face_location[2])

					cv2.rectangle(image, top_left, bottom_right,(0,0,255),2)
					cv2.putText(image, match, (face_location[3], face_location[2]+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

	def get_frame(self):
		self.frame = self.video.read()

		if self.frame.shape:
			self.face_recog()
		ret, jpeg = cv2.imencode('.jpg', self.frame)
		return jpeg.tobytes()
