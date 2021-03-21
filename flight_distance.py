import re
from math import radians, cos, sin, asin, sqrt
class DistanceCalculate:
    def distance(self, lat1, lat2, lon1, lon2):
        # radians which converts from degrees to radians.
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371
        # calculate the result
        return(c * r)


if __name__ == '__main__':
    city_1 = input("City 1:")
    city_2 = input("City 2:")
    try:
        lat1_part = city_1.split(",")[0]
        lon1_part = city_1.split(",")[1]
        lat2_part = city_2.split(",")[0]
        lon2_part = city_2.split(",")[1]

        lat1 = re.findall(r"[-+]?\d*\.\d+|\d+", lat1_part)[0]
        lon1 = re.findall(r"[-+]?\d*\.\d+|\d+", lon1_part)[0]
        lat2 = re.findall(r"[-+]?\d*\.\d+|\d+", lat2_part)[0]
        lon2 = re.findall(r"[-+]?\d*\.\d+|\d+", lon2_part)[0]

        direction_lat1 = re.findall(r'[a-zA-Z]+', lat1_part)[0]
        direction_lon1 = re.findall(r'[a-zA-Z]+', lon1_part)[0]
        direction_lat2 = re.findall(r'[a-zA-Z]+', lat2_part)[0]
        direction_lon2 = re.findall(r'[a-zA-Z]+', lon2_part)[0]

        lat1 = float(lat1) if direction_lat1 == "N" else -float(lat1)
        lon1 = float(lon1) if direction_lat1 == "W" else -float(lon1)
        lat2 = float(lat2) if direction_lat1 == "N" else -float(lat2)
        lon2 = float(lon2) if direction_lat1 == "W" else -float(lon2)
        # print(lat1, lon1, lat2, lon2)
        if not lat1 or not lon1 or not lat2 or not lon2:
            print("Wrong Input, please enter input in correct format")
        distance_ob = DistanceCalculate()
        print(distance_ob.distance(lat1, lat2, lon1, lon2))
    except Exception as e:
        print("\ne",e)
        print("Wrong Input, Please give input in correct format")
