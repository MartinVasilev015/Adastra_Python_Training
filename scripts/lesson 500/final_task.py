'''
-Use Composite pattern to create a virtual city
    -a city has streets in it
    -a street has buildings on it
    -a building has floors in it
    -a floor has estates on it (apartments, offices, etc)
    -an estate has rooms in it
-Use Factory pattern to create 2 factories:
    -one to generate cities randomly
    -one that lets users create cities by inputting values
-Use Facade pattern to make a repo class that can:
    -create cities randomly
    -create cities by hand
    -store created cities
    -print stored cities
'''
from abc import ABC, abstractmethod
from enum import Enum
import random
import datetime

#region Composites
class Component (ABC):
    @abstractmethod
    def print_info(self, indentation: int):
        pass

    @abstractmethod
    def to_json(self) -> str:
        pass


class City(Component):
    name = ''
    
    #east to west
    longitude = 0.0

    #north to south
    latitude = 0.0
    streets = [Component]
    
    def __init__(self) -> None:
        super().__init__()

    def __init__(self, name: str, longitude: float, latitude: float, streets: list) -> None:
        super().__init__()
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.streets = streets
    
    def print_info(self, indentation):

        info = ' ' * indentation + f'"{self.name}", longitude: {self.longitude}, latitude: {self.latitude}'
        print(info)

        if len(self.streets) == 0:
            print(' ' * indentation + 'Nothing here. For now...')
        else:
            print(' ' * indentation + 'Streets here: ')
            for i in self.streets:
                i.print_info(indentation + 1)

    def to_json(self):

        streets_str = ''

        for id, i in enumerate(self.streets):
            streets_str += i.to_json()
            if not(id == len(self.streets) - 1):
                streets_str += ','

        output = f"'name':'{self.name}','longitude':{self.longitude},'latitude':{self.latitude},'streets':[{streets_str}]"

        return '{' + output + '}'


class StreetType(str, Enum): 
    Boulevard = 'boulevard'
    Avenue = 'avenue'
    Basic = 'street'
    Highway = 'highway'
    Pedestrian_str = 'pedestrian street'

class Street(Component):
    name = ''
    street_type = ''
    builings = [Component]
    
    def __init__(self) -> None:
        super().__init__()

    def __init__(self, name: str, street_type: StreetType, buildings: list) -> None:
        super().__init__()
        self.name = name
        self.street_type = street_type
        self.builings = buildings

    def print_info(self, indentation):
        prep = 'a'

        if self.street_type.lower().startswith(('a', 'o', 'e', 'u', 'i')):
            prep = 'an'

        info = ' ' * indentation + f'"{self.name}" is {prep} {self.street_type.value}.'
        print(info)

        if len(self.builings) == 0:
            print(' ' * indentation + 'No buildings here. Yet...')
        else:
            print(' ' * indentation + 'Buildings here: ')
            for i in self.builings:
                i.print_info(indentation + 1)

    def to_json(self):

        builings_str = ''

        for id, i in enumerate(self.builings):
            builings_str += i.to_json()
            if not(id == len(self.builings) - 1):
                builings_str += ','

        output = f"'name':'{self.name}','street_type':'{self.street_type.value}','builings':[{builings_str}]"

        return '{' + output + '}'


class BuildingType(str, Enum): 
    Block = 'block'
    House = 'house'
    Commercial = 'commercial building'
    Business = 'business building'
    Municipal = 'municipal building'

class Building(Component):

    name = ''
    num = 0
    year_built = 0
    builing_type = ''
    floors = [Component]
    
    def __init__(self) -> None:
        super().__init__()

    def __init__(self, name: str, num: int, year_built: int, builing_type:BuildingType, floors: list) -> None:
        super().__init__()
        self.name = name
        self.num = num
        self.year_built = year_built
        self.builing_type = builing_type
        self.floors = floors

    def print_info(self, indentation):
        floor_form = 'floor'
        if not (len(self.floors) == 1):
            floor_form = 'floors'

        info = ' ' * indentation + f'№{self.num}, "{self.name}" is a {self.builing_type.value}. It was built in {self.year_built} and has {len(self.floors)} {floor_form}'

        print(info)

        self.floors.sort(key = lambda x: x.floor_num)

        for i in self.floors:
            i.print_info(indentation + 1)
        
    def to_json(self):

        floor_str = ''

        for id, i in enumerate(self.floors):
            floor_str += i.to_json()
            if not(id == len(self.floors) - 1):
                floor_str += ','

        output = f"'name':'{self.name}','num':{self.num},'year_built':{self.year_built},'builing_type':'{self.builing_type.value}','floors':[{floor_str}]"

        return '{' + output + '}'


class Floor(Component):

    floor_num = 0
    estates = [Component]
    
    def __init__(self) -> None:
        super().__init__()

    def __init__(self, floor_num: int, estates: list) -> None:
        super().__init__()
        self.floor_num = floor_num
        self.estates = estates

    def print_info(self, indentation):

        floor_num_format = f'floor {self.floor_num}'

        if self.floor_num == 0:
            floor_num_format = 'ground floor'

        print(' ' * indentation + floor_num_format)

        if len(self.estates) > 0:
            print(' ' * indentation + 'estates: ')
            for i in self.estates:
                i.print_info(indentation + 1)
        else:
            print(' ' * indentation + 'No estates here. Yet...')

    def to_json(self):

        estates_str = ''

        for id, i in enumerate(self.estates):
            estates_str += i.to_json()
            if not(id == len(self.estates) - 1):
                estates_str += ','

        output = f"'floor_num':{self.floor_num},'estates':[{estates_str}]"

        return '{' + output + '}'


class EstateType(str, Enum): 
    Apartment = 'apartment'
    Office = 'office'
    Shop = 'shop'

class Estate(Component):

    estate_num = 0
    estate_type = ''
    quadrature = 0.0
    rooms = [Component]
    
    def __init__(self) -> None:
        super().__init__()

    def __init__(self, estate_num: int, estate_type: EstateType, quadrature: float, rooms: list) -> None:
        super().__init__()
        self.estate_num = estate_num
        self.estate_type = estate_type
        self.quadrature = quadrature
        self.rooms = rooms

    def print_info(self, indentation):
        prep = 'a'
        if self.estate_type.lower().startswith(('a', 'o', 'e', 'u', 'i')):
            prep = 'an'

        print(' ' * indentation + f'№{self.estate_num} - {prep} {self.estate_type.value}, {self.quadrature} m²')
        print(' ' * indentation + 'rooms:')

        for i in self.rooms:
            i.print_info(indentation + 1)

    def to_json(self):

        rooms_str = ''

        for id, i in enumerate(self.rooms):
            rooms_str += i.to_json()
            if not(id == len(self.rooms) - 1):
                rooms_str += ','

        output = f"'estate_num':{self.estate_num},'estate_type':'{self.estate_type.value}','quadrature':{self.quadrature},'rooms':[{rooms_str}]"

        return '{' + output + '}'


class RoomType(str, Enum): 
    Living = 'living room'
    Kitchen = 'kitchen'
    Bedroom = 'bedroom'
    Office = 'office'
    Storage = 'storage room'
    Workshop = 'workshop'
    Classroom = 'classroom'
    Bathroom = 'bathroom'
    Toilet = 'toilet'
    Shop = 'shop'

class Room(Component):

    room_type = ''
    
    def __init__(self) -> None:
        super().__init__()

    def __init__(self, room_type: RoomType) -> None:
        super().__init__()
        self.room_type = room_type

    def print_info(self, indentation):
        print(' ' * indentation + self.room_type)

    def to_json(self):

        output = f"'room_type':'{self.room_type.value}'"

        return '{' + output + '}'
#endregion

#------------------------------------------------

#region Factories
class CityFactory (ABC):
    @abstractmethod
    def create_city(self):
        pass


class RandomCityFactory(CityFactory):

    #static for now, could be replaced by an API or a DB
    #wanted to consume an API but all are either paid or have limited use
    city_names = ['Brecaster','Vrodale','Zlucbus','Briburgh','Chimouth','Phinas','Vlul','Brurgh','Isonmery','Ertonsey','Yuvale','Idemond','Xaekling','Kleving','Chuisas','Rento','Holn','Phark','Egobury','Ingmore','Goiginia Doton','Himouth', 'Vrasas', 'Tobridge', 'Yront', 'Anont', 'Strolk', 'Agomore', 'Orkcaster']
    street_names = ['Middle Street','Forest Route','Farmer Lane','Ash Way','Meadow Row','Star Lane','Walnut Lane','Anchor Street','North Street','Museum Avenue','Sugarplum Lane','Hope Avenue','Hawthorn Street','Stone Route','King Row','Frost Lane','Cross Street','Paradise Avenue','Diamond Lane','Colonel Boulevard','Bridgeway Street','Hazelnut Street','Rosemary Lane','Canal Way','Amber Row','Spring Row','Long Avenue','Sapphire Street','Farmer Avenue','Feathers Street']
    building_names = ['Antique Store','Arcade','Bakery','Bank','Bookstore','Botanical Garden','Brewery','Cafe','Casino','Club','Fire Department','Gym','Hospital','Hotel','Mall','Municipality','Police','Prison','Pizzeria','Restaurant','School','University']

    street_types = list(StreetType)
    building_types = list(BuildingType)
    estate_types = list(EstateType)
    room_types = list(RoomType)

    def create_city(self):

        streets_num_lower_limit = 0
        streets_num_upper_limit = 4
        builings_num_lower_limit = 0
        builings_num_upper_limit = 4
        street_num_lower_limit = 0
        street_num_upper_limit = 100
        year_built_lower_limit = 1950
        year_built_upper_limit = datetime.date.today().year
        floors_num_lower_limit = 1
        floors_num_upper_limit = 4
        estates_num_lower_limit = 0
        estates_num_upper_limit = 4
        estate_num_lower_limit = 1
        estate_num_upper_limit = 15
        quadrature_lower_limit = 20.0
        quadrature_upper_limit = 150.0
        rooms_num_lower_limit = 1
        rooms_num_upper_limit = 4


        city_name = random.choice(self.city_names)

        #lower and upper limits are hard-coded here because they won't ever change
        longitude = "%.4f" % random.uniform(-180.0, 180.0)
        latitude = "%.4f" % random.uniform(-90.0, 90.0)
        
        streets = []
        streets_num = random.randrange(streets_num_lower_limit, streets_num_upper_limit)

        for i in range(streets_num):
            street_name = random.choice(self.street_names)
            street_type = random.choice(self.street_types)
            
            builings = []
            builings_num = random.randrange(builings_num_lower_limit, builings_num_upper_limit)
            
            for j in range(builings_num):
                building_name = random.choice(self.building_names)
                street_num =  random.randrange(street_num_lower_limit, street_num_upper_limit)
                year_built = random.randrange(year_built_lower_limit, year_built_upper_limit)
                building_type = random.choice(self.building_types)
                
                floors = []
                floors_num = random.randrange(floors_num_lower_limit, floors_num_upper_limit)

                for h in range(floors_num):
                    floor_num = h
                    
                    estates = []
                    estates_num = random.randrange(estates_num_lower_limit, estates_num_upper_limit)
                    
                    for g in range(estates_num):
                        estate_num = random.randrange(estate_num_lower_limit, estate_num_upper_limit)
                        estate_type = random.choice(self.estate_types)
                        quadrature = "%.2f" % random.uniform(quadrature_lower_limit, quadrature_upper_limit)
                       
                        rooms = []
                        rooms_num = random.randrange(rooms_num_lower_limit, rooms_num_upper_limit)
                        for k in range(rooms_num):
                            room_type = random.choice(self.room_types)
                            rooms.append(Room(room_type))

                        estates.append(Estate(estate_num, estate_type, quadrature, rooms))
                    
                    floors.append(Floor(floor_num, estates))

                builings.append(Building(building_name, street_num, year_built, building_type, floors))

            streets.append(Street(street_name, street_type, builings))

        return City(city_name, longitude, latitude, streets)


class ByHandCityFactory(CityFactory):
    
    street_types = list(StreetType)
    building_types = list(BuildingType)
    estate_types = list(EstateType)
    room_types = list(RoomType)

    def getInputNumberInRange(self, prop_name, lower_range, upper_range, is_whole):
        x = -10000
        while x < lower_range or x > upper_range:
            print(f'Enter {prop_name} (from {lower_range} to {upper_range}):')
            try:
                if is_whole:
                    x = int(input())
                else:
                    x = float(input())
            except:
                print('Only numbers, please :)')
                continue
        return x
    

    def getPositiveIntInput(self, upper_range, inner_component: str, outer_component: str):
        x = -10000

        preposition = 'in'

        if outer_component in ('street', 'floor'):
            preposition = 'on'

        while x < 0 or x > upper_range:
            print(f'Enter how many {inner_component} you\'d like {preposition} this {outer_component}:')
            try:
                x = int(input())
            except:
                print('Only numbers, please :)')
        return x


    def getEnumOption(self, enum_list):
        
        x = -1
       
        while x < 0 or x > len(enum_list):

            for id, i in enumerate(enum_list): 
                print(str(id) + ": " + i.value)
            try:
                x = int(input())
                
            except ValueError:
                print('Only numbers, please :)')
                continue
            except IndexError: 
                print('Please, only from the list')
                continue
        return enum_list[x]


    def createRooms(self, floor_num, estate_num):

        rooms_num_upper_limit = 4

        print(f'Rooms in estate[{estate_num}] on floor[{floor_num}]:')
        rooms_num = self.getPositiveIntInput(rooms_num_upper_limit, 'rooms', 'estate')

        result = []

        if rooms_num == 0:
            return result

        for i in range(rooms_num):
            print(f'Enter the type of room[{i}]:')
            room_type = self.getEnumOption(self.room_types)

            result.append(Room(room_type))

        return result


    def createEstates(self, building_name, floor_num):

        estates_num_upper_limit = 4
        estate_num_lower_range = 0
        estate_num_upper_range = 15
        quadrature_lower_range = 20.0
        quadrature_upper_range = 130.0


        print(f'Estates on floor[{floor_num}] in "{building_name}":')
        estates_num = self.getPositiveIntInput(estates_num_upper_limit, 'estates', 'floor')

        result = []

        if estates_num == 0:
            return result

        for i in range(estates_num):

            print(f'Enter an estate number for estate[{i}]:')
            estate_num = self.getInputNumberInRange('estate number', estate_num_lower_range, estate_num_upper_range, True)

            print(f'Enter the estate type for estate[{i}]:')
            estate_type = self.getEnumOption(self.estate_types)

            print(f'Enter quadrature for estate[{i}]:')
            quadrature = self.getInputNumberInRange('quadrature', quadrature_lower_range, quadrature_upper_range, False)
            
            rooms = self.createRooms(floor_num, i)

            result.append(Estate(estate_num, estate_type, quadrature, rooms))

        return result            


    def createFloors(self, building_name):

        floors_num_upper_limit = 4

        print(f'Floors in "{building_name}":')
        floors_num = self.getPositiveIntInput(floors_num_upper_limit, 'floors', 'building')

        result = []

        if floors_num == 0:
            return result

        for i in range(floors_num):
            estates = self.createEstates(building_name, i)
            result.append(Floor(i, estates))

        return result


    def createBuildings(self, street_name):

        buildings_num_upper_limit = 4
        street_num_lower_limit = 0
        street_num_upper_limit = 100
        year_built_lower_limit = 1950
        year_built_upper_limit = datetime.date.today().year

        print(f'Buildings on "{street_name}":')
        buildings_num = self.getPositiveIntInput(buildings_num_upper_limit, 'buildings', 'street')

        result = []

        if buildings_num == 0:
            return result

        for i in range(buildings_num):
            print(f'Enter a name for building[{i}]:')
            building_name = input()

            print(f'Enter a street number for "{building_name}":')
            num = self.getInputNumberInRange('street number', street_num_lower_limit, street_num_upper_limit, True)

            print(f'Enter the year "{building_name}" was built in:')
            year_built = self.getInputNumberInRange('year built', year_built_lower_limit, year_built_upper_limit, True)

            print(f'Enter the building type of "{building_name}":')
            building_type = self.getEnumOption(self.building_types)

            floors = self.createFloors(building_name)

            result.append(Building(building_name, num, year_built, building_type, floors))

        return result


    def create_city(self):

        print('Enter a city name:')
        city_name = input()

        #lower and upper limits are hard-coded because they won't ever change
        longitude = self.getInputNumberInRange('longitude', -180.0, 180.0, False)
        latitude = self.getInputNumberInRange('latitude', -90.0, 90.0, False)

        streets = []
        streets_num_upper_limit = 4
        streets_num = self.getPositiveIntInput(streets_num_upper_limit, 'streets', 'city')

        for i in range(streets_num):
            print(f'Enter a name for street[{i}]:')
            street_name = input()

            print(f'Enter a street type for {street_name}:')
            street_type = self.getEnumOption(self.street_types)

            buildings = self.createBuildings(street_name)

            streets.append(Street(street_name, street_type, buildings))

        return City(city_name, longitude, latitude, streets)
#endregion

#------------------------------------------------

#region Facade
class CityRepo:

    cities = []
    rcf = RandomCityFactory()
    bhcf = ByHandCityFactory()

    def add_random_city(self):
        self.cities.append(self.rcf.create_city())

    def add_city_by_hand(self):
        city = self.bhcf.create_city()
        self.cities.append(city)

    def print_cities_details_as_text(self):
        if len(self.cities) == 0:
            print("No cities. Yet...")
        else:
            for c in self.cities:
                c.print_info(0)

    def print_cities_details_as_json(self):
        if len(self.cities) == 0:
            return '{}'
        else:
            result = ''
            separator = ','
            for i, c in enumerate(self.cities):

                if i == len(self.cities) - 1:
                    separator = ''

                result += c.to_json() + separator
            return '{[' + result + ']}'
    
    #For Future Development:
    #def get_city_by_name()
    #def update_city()
    #def delete_city()
#endregion

#------------------------------------------------

repo = CityRepo()

repo.add_random_city()
repo.add_city_by_hand()

print(repo.print_cities_details_as_json())