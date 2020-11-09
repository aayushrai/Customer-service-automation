from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http.response import StreamingHttpResponse
from .models import User,UserSerializer,Product,ProductSerializer,Order
from rest_framework.parsers import JSONParser
import uuid
face_dis_flag = False
result = []
@api_view(["GET"])
def userData(request):
	global result
	if face_dis_flag:
		for name,idd,dis in sorted(zip(known_names,known_id,distance), key=lambda item: item[2]):
			if dis < .6:
				result =[]
				result.append(User.objects.get(user_id=idd))
	serilizeResult = UserSerializer(result,many=True)
	return Response(serilizeResult.data)

@api_view(["GET"])
def productData(request):
	result = Product.objects.all()
	productResult = ProductSerializer(result,many=True)
	return Response(productResult.data)

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
		
	Order.objects.bulk_create(orders)
		
	return Response({"status":"Order Placed"})

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
