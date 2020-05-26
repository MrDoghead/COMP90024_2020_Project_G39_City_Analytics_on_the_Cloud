import math

class Cities:
    def __init__(self):
        self.city_map = {
                'Melbourne': [[144.946457,-37.840935],'24600'],
                'Launceston': [[147.157135,-41.429825],'64010'],
                'Hobart': [[147.324997,-42.880554],'62810'],
                'Devonport': [[146.346390,-41.180557],'61610'],
                'Canberra': [[149.128998,-35.282001],'89399'],
                'Perth': [[115.857048,-31.953512],'57080'],
                'Mandurah': [[115.723053,-32.528889],'55110'],
                'Joondalup': [[115.766113,-31.745001],'54170'],
                'Alice Springs': [[133.8836,-23.6975],'70200'],
                'Ballarat': [[143.850006,-37.549999,],'20570'],
                'Sydney': [[151.209900,-33.865143],'17200'],
                'Wollongong': [[150.893143,-34.425072],'18450'],
                'New Castle': [[151.750000,-32.916668],'15900'],
                'Port Lincoln': [[135.850479,-34.730194],'40070'],
                'Adelaide': [[138.599503,-34.921230],'46300'],
                'Gold Coast': [[153.399994,-28.016666],'33430'],
                'Brisbane': [[153.021072,-27.470125],'31000']
                }

    def is_au(self,loc):
        au_loc = [112.9211,-54.6403,159.2787,-9.2288]
        lo = loc[0]
        la = loc[1]
        if au_loc[0] < lo < au_loc[2] and au_loc[1] < la < au_loc[3]:
            return True
        else:
            return False

    def loc2city(self,loc):
        city = None
        min_dis = None
        for k,v in self.city_map.items():
            coo = v[0]
            dis = self.__distance(coo,loc)
            if not city:
                min_dis = dis
                city = k
                continue
            if dis < min_dis:
                min_dis = dis
                city = k

        return city

    def lga2city(self,code):
        city = None
        for k,v in self.city_map.items():
            lga = v[1]
            if str(code) == lga:
                city = k
                break
        return city
    
    def lga2loc(self,code):
        loc = None
        for k,v in self.city_map.items():
            lga = v[1]
            if str(code) == lga:
                loc = v[0]
                break
        return loc

    def loc2lga(self,loc):
        city = self.loc2city(loc)
        lga = self.city_map[city][1]
        return lga

    def __distance(self,loc1,loc2):
        lo1,la1 = loc1
        lo2,la2 = loc2
        dis = math.sqrt((lo1 - lo2) ** 2 + (la1 - la2) ** 2)
        return dis


if __name__ == '__main__':
    # sample1: given coordinates, return city 
    cities = Cities()
    loc = [144.946457,-37.840935]   # melbourne 24600
    city1 = cities.loc2city(loc)
    lga_code = cities.loc2lga(loc)
    print(city1)
    print(lga_code)

    # sample2: given lga code, return city
    code = '31000'  # Brisbane
    city2 = cities.lga2city(code)
    print(city2)

    # sample3: given code, return coordinates
    code2 = '57080'  # Perth 115.857048,-31.953512
    coo = cities.lga2loc(code2)
    print(coo)

    # sample4: check if located in au
    loc2 = [151.209900,-33.865143]   # sydney
    print(cities.is_au(loc2))


