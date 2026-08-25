from datetime import datetime


class Vehicle:
    def __init__(self,registration_number: str, make: str, model: str, fuel_type: str, operational_status: str = "AVAILABLE", odometer_km: int = 0):
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.fuel_type = fuel_type
        self.operational_status = operational_status
        self.blocks = []
        if not self.validate_fuel_type():
            raise ValueError("Invalid Fuel type")
        self.odometer_km = odometer_km
        if odometer_km < 0:
            raise ValueError("The km cannot be less than 0")
        if not self.validate_operational_status():
            raise ValueError("Invalid Status")

    def add_block(self, block):
        self.blocks.append(block)    


    def update_odometer(self, new_odometer_km):
        if new_odometer_km <0:
            raise ValueError("The updated km can't be less than 0") 
        self.odometer_km = new_odometer_km

    def validate_fuel_type(self):
        return self.fuel_type in ["Petrol", "Electric", "Diesel"]

    def validate_operational_status(self):
        return self.operational_status in ["AVAILABLE","RESERVED","RENTED"]

    def get_blocks(self):
        return self.blocks 

class VehicleBlock:
    def __init__(self, block_type: str, start: datetime, end: datetime, block_reason: str ):
        self.block_type = block_type
        self.start = start
        self.end = end
        self.block_reason = block_reason    

      

        
# Test Code

vehicle = Vehicle(registration_number= "KJ 43629", make= "Toyota",model = "Rav 4", fuel_type = "Petrol", odometer_km=23000, operational_status="AVAILABLE")

if vehicle.validate_fuel_type():
    print("Correct fueltype")
else:
    print("Invalid fueltype")    

print(vehicle.odometer_km)

vehicle.update_odometer(25000)

print(vehicle.odometer_km)
print(vehicle.operational_status)


vehicle_block = VehicleBlock(block_type= "MAINTENANCE", start= datetime(2026,9,21,17,0), end= datetime(2026,9,30,17,0), block_reason="Punctured tire",)
vehicle.add_block(vehicle_block)



        
print(vehicle.get_blocks())
        
       





