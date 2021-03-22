# Create your views here.
# Standard Library
import csv
import re
from math import radians, cos, sin, asin, sqrt
# Third Party Library
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import CabDriverSerializer
from .models import CabPosition, CabDriver


class Registration(APIView):
    def validate_email(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, email)):
            return False
        else:
            return True

        return True
    def post(self, request):
        print(f'[Registration] POST, Data: {request.data}')
        try:
            request_data = request.data
            if request_data is None:
                raise Exception('Required data not given!')
            name = request_data.get('name', None)
            if name is None:
                raise Exception('Name not provided!')
            car_number = request_data.get('car_number', None)
            if car_number is None:
                raise Exception('Car Number Information not given!')
            phone_number = request_data.get('phone_number', None)
            if phone_number is None:
                raise Exception('phone_number not provided!')
            if len(phone_number) != 13:
                raise Exception("Please provide correct Mobile number,Note- provide phone number with country code, for eg. +91")
            license_number = request_data.get('license_number', None)
            if license_number is None:
                raise Exception('license Number Information not given!')
            email = request.data.get('email', None)
            if email is None:
                raise Exception('email Information not given!')
            # check whether any cart modification payment is pending, if yes, don't allow split for any role
            resp_val = self.validate_email(email)
            if not resp_val:
                return Response({"message":"Email is not correct"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            error_msg = str(e)
            print(f'[Registration] Error: {error_msg}, Exception: {e}')
            return Response(
                {'message': error_msg},
                status.HTTP_400_BAD_REQUEST)
        print("LOL")
        final_data = request.data
        serialized = CabDriverSerializer(data=final_data)
        if serialized.is_valid():
            data = serialized.save()
            driver_id = data.id
            return Response({"message":f"Registration completed, Your Driver id is {driver_id}"}, status=status.HTTP_200_OK)
        return Response({"message":serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

class UpdateLocation(APIView):
    def post(self, request, driver_id):
        print(f'[UpdateLocation] POST, Data: {request.data}, {driver_id}')
        try:
            request_data = request.data
            if request_data is None:
                raise Exception('Required data not given!')
            latitude = request_data.get('latitude', None)
            if latitude is None:
                raise Exception('latitude not provided!')
            longitude = request_data.get('longitude', None)
            if longitude is None:
                raise Exception('longitude Information not given!')
        except Exception as e:
            error_msg = str(e)
            print(f'[Registration] Error: {error_msg}, Exception: {e}')
            return Response(
                {'message': error_msg},
                status.HTTP_400_BAD_REQUEST)
        driver_ob = CabDriver.objects.filter(id=driver_id).first()
        if not driver_ob:
            error_msg = "Driver Id is wrong, No such Driver"
            print(f'[Registration] Error: {error_msg}')
            return Response(
                {'message': error_msg},
                status.HTTP_400_BAD_REQUEST)

        position = CabPosition.objects.filter(cab_id=driver_ob.id).first()
        if not position:
            pos = CabPosition.objects.create(cab=driver_ob,latitude=latitude,longitude=longitude)
            print(pos)
        else:
            position.latitude=latitude
            position.longitude=longitude
            position.save()
            print("YES")
        return Response({"message":"Location Updated"}, status=status.HTTP_200_OK)


class SearchLocation(APIView):
    def post(self, request):
        print(f'[UpdateLocation] POST, Data: {request.data}')
        try:
            request_data = request.data
            if request_data is None:
                raise Exception('Required data not given!')
            latitude = request_data.get('latitude', None)
            if latitude is None:
                raise Exception('latitude not provided!')
            longitude = request_data.get('longitude', None)
            if longitude is None:
                raise Exception('longitude Information not given!')
        except Exception as e:
            error_msg = str(e)
            print(f'[Registration] Error: {error_msg}, Exception: {e}')
            return Response(
                {'message': error_msg},
                status.HTTP_400_BAD_REQUEST)
        ans = self.get_distance(latitude,longitude)
        if not ans:
            message = "NO cab Nearby"
        else:
            ans = [str(x) for x in ans]
            message = "Cabs around you are (these are driver id)->"
            message += ", ".join(ans)
        return Response({"message":message}, status=status.HTTP_200_OK)


    def get_distance(self, latitude, longitude):
        final_ans = []
        all_positions = CabPosition.objects.all()
        for item in all_positions:

            lat2_part = item.latitude
            lon2_part = item.longitude
            # print(latitude,longitude,lat2_part,lon2_part)

            lat1 = re.findall(r"[-+]?\d*\.\d+|\d+", latitude)[0]
            lon1 = re.findall(r"[-+]?\d*\.\d+|\d+", longitude)[0]
            lat2 = re.findall(r"[-+]?\d*\.\d+|\d+", lat2_part)[0]
            lon2 = re.findall(r"[-+]?\d*\.\d+|\d+", lon2_part)[0]

            # print(lat1,)
            if not lat1 or not lon1 or not lat2 or not lon2:
                return False

            direction_lat1 = re.findall(r'[a-zA-Z]+', longitude)[0]
            direction_lon1 = re.findall(r'[a-zA-Z]+', latitude)[0]
            direction_lat2 = re.findall(r'[a-zA-Z]+', lat2_part)[0]
            direction_lon2 = re.findall(r'[a-zA-Z]+', lon2_part)[0]

            if not direction_lat1 or not direction_lon1 or not direction_lat2 or not direction_lon2:
                return False

            lat1 = float(lat1) if direction_lat1 == "N" else -float(lat1)
            lon1 = float(lon1) if direction_lat1 == "E" else -float(lon1)
            lat2 = float(lat2) if direction_lat1 == "N" else -float(lat2)
            lon2 = float(lon2) if direction_lat1 == "E" else -float(lon2)

            if not lat1 or not lon1 or not lat2 or not lon2:
                return False


            ans = self.distance(lat1, lat2, lon1, lon2)
            if int(ans) <= 4:
                final_ans.append(item.cab_id)

        return final_ans

    def distance(self, lat1, lat2, lon1, lon2):
        # radians which converts from degrees to radians.
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371
        # calculate the result
        return(c * r)


