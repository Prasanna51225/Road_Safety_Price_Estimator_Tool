from typing import Dict

MATERIAL_PRICES = {
    "Speed Limit Sign Board (Retroreflective)": 2500.00,
    "School Ahead Warning Sign (Standard IRC:67-2022)": 2700.00,
    "Informatory Fuel Pump Sign (IRC:67-2022)": 2300.00,
    "Side Road Ahead Warning Sign (IRC:67-2022)": 2500.00,
    "No Parking Regulatory Sign (IRC:67-2022)": 2100.00,
    "Pedestrian Crossing Warning Sign (IRC:67-2022)": 2600.00,
    "Thermoplastic Road Marking Paint (White/Yellow)": 300.00,
    "Thermoplastic Pedestrian Crossing Paint (White)": 320.00,
    "Retroreflective Red-White Bidirectional Road Stud": 160.00,
    "Bituminous Mix (for Pothole Repair)": 5700.00,
    "Solar LED Blinker (Amber) with Maintenance": 3000.00,
    "LED Streetlight (30W Solar) with Pole": 12000.00,
    "Flexible Mounting Marker (FMM) - IRC:79-2019": 600.00,
    "Roadway Delineator Post (Retroreflective) - IRC:79-2019": 800.00,
}

def get_prices() -> Dict[str, float]:
    return MATERIAL_PRICES

def get_price_for_material(material_name: str) -> float:
    prices = get_prices()
    return prices.get(material_name, 0.0)
