import datetime
import numpy as np
import base64
import requests
import cv2
from pyzbar import pyzbar
from datetime import date
import keyboard

productList = []
api_user_token = '99f9da19d9f4ca6cd7b2cad40c70c5cda90fcf8f'
headers = {'Authorization': 'Bearer ' + api_user_token}

# Function to perform ingredient recognition using the Logmeal API
def recognize_ingredients_api(frame):
    # Convert the frame to a byte array
    img = cv2.imread('webcam_shot.jpg')
    success, image_array = cv2.imencode('.jpg',img )
    if not success:
        print('Error: Failed to convert the frame to a byte array')
        return
    print(success)
    # Encode the image data as base64
    base64_image = base64.b64encode(image_array).decode('utf-8')

    # Single/Several Dishes Detection
    url = 'https://api.logmeal.es/v2/image/segmentation/complete'
    resp = requests.post(url, data=base64_image, headers=headers)

    # Print the response content for debugging
    print('Segmentation API Response:', resp.content)

    try:
        # Check if the response contains the imageId
        if 'imageId' in resp.json():
            image_id = resp.json()['imageId']

            # Ingredients information
            url = 'https://api.logmeal.es/v2/recipe/ingredients'
            resp = requests.post(url, json={'imageId': image_id}, headers=headers)

            # Print the response content for debugging
            print('Ingredients API Response:', resp.content)

            # Display ingredients info
            print(resp.json())
        else:
            print('Error: imageId not found in the response')
    except requests.exceptions.JSONDecodeError:
        print('Error: Invalid JSON response from the API')

# Open the webcam

# function to recognize food from web image
def recognize_food():
    cap = cv2.VideoCapture(0)

    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if ret:
        # Specify the file path to save the image
        image_file = 'webcam_shot.jpg'

        # Save the frame as an image file
        cv2.imwrite(image_file, frame)
        print('Webcam shot saved as', image_file)
    else:
        print('Failed to capture a frame from the webcam')

    # Release the webcam
    cap.release()
    img = image_file
    api_user_token = '99f9da19d9f4ca6cd7b2cad40c70c5cda90fcf8f'
    headers = {'Authorization': 'Bearer ' + api_user_token}

    # Single/Several Dishes Detection
    url = 'https://api.logmeal.es/v2/image/segmentation/complete'
    resp = requests.post(url, files={'image': open(img, 'rb')}, headers=headers)

    # Check if the response contains the imageId
    if 'imageId' in resp.json():
        image_id = resp.json()['imageId']

        # Ingredients information
        url = 'https://api.logmeal.es/v2/recipe/ingredients'
        resp = requests.post(url, json={'imageId': image_id}, headers=headers)

        # Display ingredients info
        #print(resp.json())
        if 'foodName' in resp.json():
            food_name = resp.json()['foodName']
            name = food_name[0]
            print(name)
            daysFromToday = int(input("Days from today fruit will expire: "))
            today = date.today()
            expirationdate = today + datetime.timedelta(days=daysFromToday)
            productList.append(freshProduce(name, daysFromToday, expirationdate))
            #print(productList)
    else:
        print('Error: imageId not found in the response')

class Product:
    def __init__(self, barcode, name, category, brand, expirationdate, day, month, year):
        self.barcode = barcode
        self.name = name
        self.category = category
        self.brand = brand
        self.day = day
        self.month = month
        self.year = year
        self.expirationdate = expirationdate
        self.expiration_date_str = str(year) + "-" + str(month) + "-" + str(day)

    def printAttributes(self):
        print("Barcode: " + self.barcode)
        print("Name: " + self.name)
        print("Category: " + self.category)
        print("Brand: " + self.brand)
        print("Expiration date: " + self.expirationdate)
        print("Day: " + self.day)
        print("Month: " + self.month)
        print("Year: " + self.year)

    def printItem(self):
        return self.name + ", " + self.expiration_date_str

class freshProduce:
    def __init__(self, name, daysFromToday, expirationdate):
        self.name = name
        self.daysFromToday = daysFromToday
        self.expirationdate = expirationdate

    def printItem(self):
        return self.name + ", " + str(self.expirationdate)

def sortProductList():
    size = len(productList)
    for ind in range(size):
        min_index = ind

        for j in range(ind + 1, size):
            # select the minimum element in every iteration
            if productList[j].expirationdate < productList[min_index].expirationdate:
                min_index = j
        # swapping the elements to sort the array
        (productList[ind], productList[min_index]) = (productList[min_index], productList[ind])

def lookup_product(barcode):
    api_key = 'er230j0dug8p3c38ryh4so87oi5ecq'
    url = f'https://api.barcodelookup.com/v2/products?barcode={barcode}&key={api_key}'

    response = requests.get(url)
    data = response.json()

    if 'products' in data and len(data['products']) > 0:
        product = data['products'][0]
        title = product.get('product_name', '')
        brand = product.get('brand', '')
        manufacturer = product.get('manufacturer', '')
        category = product.get('category', '')
        expiration_date = askForExpirationDate()
        day = int(expiration_date[8:10])
        month = int(expiration_date[5:7])
        year = int(expiration_date[0:4])
        d1 = datetime.date(year, month, day)
        print(title)
        productList.append(Product(barcode, title, category, brand, d1, day, month, year))

    else:
        print("Product not found or no details available.")

def read_barcodes():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        decoded_objects = pyzbar.decode(frame)

        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')
            barcode_type = obj.type

            #print("Barcode Data:", barcode_data)
            #print("Barcode Type:", barcode_type)
            return barcode_data
        cv2.imshow("Barcode Reader", frame)



        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def askForExpirationDate():
    return input("Enter expiration date (YYYY-MM-DD)")

def addProduct():
    barcode = read_barcodes()
    #barcode = input("Enter a barcode: ")
    print(barcode)
    lookup_product(barcode)


def main():
    counter = 0
    while True:
        user_input = input("Do you want to add another item? (yes/no) ")
        if(user_input.lower() == "yes"):
            user_input3 = input("Do you want to scan a barcode (barcode) or image (image): ")
            if(user_input3.lower() == "barcode"):
                addProduct()
            else:
                recognize_food()
            #print(productList[0].name)
            #productList[counter].printAttributes()
            #counter += 1
        else:
            break

    user_input2 = input("Do you want to print all the items in your list? (yes/no)")
    if(user_input2.lower() == "yes"):
        counter = 1
        sortProductList()
        for p in productList:
            print(str(counter) + ". " + p.printItem())
            counter += 1

main()
