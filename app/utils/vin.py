from vininfo import Vin
car = Vin("1HGCM82633A123456")
print(car.manufacturer, car.brand, car.country, car.region, car.vds, car.vis, car.wmi, car.years[-1], sep="\n") 
