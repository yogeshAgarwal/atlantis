# Create your views here.
# Standard Library
import csv
import base64
from io import StringIO
from datetime import timedelta
from faker import Faker
# Third Party Library
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class Assignment1(APIView):


    def post(self, request):
        print(f'[Assignment1] POST, Data: {request.data}, {request.FILES}')
        try:
            my_file = request.FILES['fisier']
        except Exception as e:
            print("Error",e)
            return Response(
                        {'message': "Error, Please upload csv file correctly"},
                        status=status.HTTP_400_BAD_REQUEST)
        # with open(csv_file, 'r') as csvfile:
        #     csvreader = csv.reader(csvfile)
        #     fields = next(csvreader)
        #     for row in csvreader:
        #         print(row)
        csv_file = my_file.read().decode('utf-8')
        reader = csv.reader(StringIO(csv_file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        header = data[0]
        data = data[1:]
        new_csv_array = []
        len_data = len(data)
        print(len_data)
        limit = int(len_data/10)
        for i in range(limit,len_data + 1,limit):
            f = StringIO()
            print(data[i-limit:i])
            csv.writer(f).writerows(data[i-limit:i])
            new_csv_array.append(f.getvalue().encode())
        "Sending string io values in response, since it is not clear from the question what should be response"
        return Response({"data":new_csv_array}, status=status.HTTP_200_OK, content_type="text/csv")

    def fake_data_generator(self):
        fake = Faker()
        fields = ['id', 'first_name', 'last_name', 'email', 'pincode', 'timestamp']
        rows = []
        filename = "testing.csv"
        for i in range(100):
            temp = []
            temp.append(i+1)
            temp.append(fake.first_name())
            temp.append(fake.last_name())
            temp.append(fake.email())
            temp.append(fake.zipcode())
            temp.append(fake.date() + " " + fake.time())
            rows.append(temp)

        with open(filename, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(fields)
            # writing the data rows
            csvwriter.writerows(rows)

