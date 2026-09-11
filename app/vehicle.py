class Vehicle:
    def __init__(self,registration_number: str, make: str, model: str, fuel_type: str, odometer_km: int = 0):
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.fuel_type = fuel_type
        if not self.validate_fuel_type():
            raise ValueError("Invalid Fuel type")
        self.odometer_km = odometer_km
        if odometer_km < 0:
            raise ValueError("The km cannot be less than 0")

        

    def update_odometer(self, new_odometer_km):
        if new_odometer_km <0:
            raise ValueError("The updated km can't be less than 0") 
        self.odometer_km = new_odometer_km

    def validate_fuel_type(self):
        return self.fuel_type in ["Petrol", "Electric", "Diesel"]
        


vehicle = Vehicle(registration_number= "KJ 43629", make= "Toyota",model = "Rav 4", fuel_type = "Petrol", odometer_km=23000)

if vehicle.validate_fuel_type():
    print("Correct fueltype")
else:
    print("Invalid fueltype")    

print(vehicle.odometer_km)
vehicle.update_odometer(-50)
print(vehicle.odometer_km)
