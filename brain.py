import re
from typing import Dict, List, Optional, Tuple

KNOWLEDGE_BASE = {
    "speed_limit_sign": {
        "keywords": ["speed limit sign", "maximum speed limit sign"],
        "material_name": "Speed Limit Sign Board (Retroreflective)",
        "logic": "count",
        "default_unit": "each",
        "regex": [r'(\d+)\s*sign', r'(\d+)\s*board']
    },
    "school_ahead_sign": {
        "keywords": ["school ahead sign", "school zone sign"],
        "material_name": "School Ahead Warning Sign (Standard IRC:67-2022)",
        "logic": "count",
        "default_unit": "each",
        "regex": [r'(\d+)\s*sign', r'(\d+)\s*board']
    },
    "fuel_station_sign": {
        "keywords": ["fuel station ahead sign", "fuel pump sign"],
        "material_name": "Informatory Fuel Pump Sign (IRC:67-2022)",
        "logic": "count",
        "default_unit": "each",
        "regex": [r'(\d+)\s*sign', r'(\d+)\s*board']
    },
    "side_road_sign": {
        "keywords": ["side road ahead sign", "side road sign"],
        "material_name": "Side Road Ahead Warning Sign (IRC:67-2022)",
        "logic": "count",
        "default_unit": "each",
        "regex": [r'(\d+)\s*sign', r'(\d+)\s*board']
    },
    "no_parking_sign": {
        "keywords": ["no parking sign", "parking sign"],
        "material_name": "No Parking Regulatory Sign (IRC:67-2022)",
        "logic": "count",
        "default_unit": "each",
        "regex": [r'(\d+)\s*sign', r'(\d+)\s*board']
    },
    "pedestrian_crossing_sign": {
        "keywords": ["pedestrian crossing sign", "crossing sign"],
        "material_name": "Pedestrian Crossing Warning Sign (IRC:67-2022)",
        "logic": "count",
        "default_unit": "each",
        "regex": [r'(\d+)\s*sign', r'(\d+)\s*board']
    },
    "longitudinal_marking": {
        "keywords": ["longitudinal marking", "edge line", "lane marking"],
        "material_name": "Thermoplastic Road Marking Paint (White/Yellow)",
        "logic": "calculate_area",
        "default_unit": "sqm",
        "regex": [
            r'(\d+\.?\d*)\s*m\b',
            r'(\d+\.?\d*)\s*meter',
            r'about\s+(\d+\.?\d*)\s*m'
        ]
    },
    "pedestrian_crossing_marking": {
        "keywords": ["pedestrian crossing", "crossing marking", "zebra crossing"],
        "material_name": "Thermoplastic Pedestrian Crossing Paint (White)",
        "logic": "calculate_area",
        "default_unit": "sqm",
        "regex": [
            r'(\d+\.?\d*)\s*m\s+width',
            r'(\d+\.?\d*)\s*sqm',
            r'(\d+\.?\d*)\s*sq\s*m'
        ]
    },
    "road_stud": {
        "keywords": ["road stud", "retroreflective stud", "bidirectional stud"],
        "material_name": "Retroreflective Red-White Bidirectional Road Stud",
        "logic": "count",
        "default_unit": "each",
        "regex": [r'(\d+)\s*stud', r'(\d+)\s*m', r'(\d+)\s*meter']
    },
    "pothole_repair": {
        "keywords": ["pothole", "potholes", "pavement damage"],
        "material_name": "Bituminous Mix (for Pothole Repair)",
        "logic": "calculate_volume",
        "default_unit": "m³",
        "regex": [
            r'(\d+\.?\d*)\s*sqm',
            r'(\d+\.?\d*)\s*sq\s*m',
            r'(\d+\.?\d*)\s*mm\s+depth',
            r'area\s+(\d+\.?\d*)\s*sqm'
        ]
    },
    "solar_blinker": {
        "keywords": ["solar blinker", "blinker", "median notch"],
        "material_name": "Solar LED Blinker (Amber) with Maintenance",
        "logic": "count",
        "default_unit": "each",
        "regex": [r'(\d+)\s*blinker', r'(\d+)\s*notch']
    },
    "streetlight": {
        "keywords": ["streetlight", "street light", "lighting facilities", "illumination"],
        "material_name": "LED Streetlight (30W Solar) with Pole",
        "logic": "calculate_length",
        "default_unit": "each",
        "regex": [
            r'(\d+\.?\d*)\s*m',
            r'(\d+\.?\d*)\s*meter',
            r'entire\s+stretch',
            r'(\d+\.?\d*)\s*km'
        ]
    },
    "fmm": {
        "keywords": ["fmm", "flexible marker", "bridge marker"],
        "material_name": "Flexible Mounting Marker (FMM) - IRC:79-2019",
        "logic": "calculate_length",
        "default_unit": "each",
        "regex": [
            r'(\d+\.?\d*)\s*m\s+length',
            r'bridge\s+of\s+(\d+\.?\d*)\s*m',
            r'(\d+\.?\d*)\s*meter'
        ]
    },
    "delineator": {
        "keywords": ["delineator", "guide pole", "roadway indicator"],
        "material_name": "Roadway Delineator Post (Retroreflective) - IRC:79-2019",
        "logic": "calculate_length",
        "default_unit": "each",
        "regex": [
            r'(\d+\.?\d*)\s*to\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*m',
            r'(\d+\.?\d*)\s*meter'
        ]
    }
}

def extract_quantities(sentence: str, regex_patterns: List[str]) -> List[float]:
    quantities = []
    for pattern in regex_patterns:
        matches = re.findall(pattern, sentence, re.IGNORECASE)
        for match in matches:
            try:
                if isinstance(match, tuple):
                    for m in match:
                        if m:
                            quantities.append(float(m))
                else:
                    quantities.append(float(match))
            except (ValueError, TypeError):
                continue
    return quantities

def calculate_volume(quantities: List[float]) -> Tuple[float, str]:
    if len(quantities) >= 2:
        area = quantities[0]
        depth_mm = quantities[1]
        depth_m = depth_mm / 1000
        volume = area * depth_m
        return volume, "m³"
    elif len(quantities) == 1:
        area = quantities[0]
        depth_m = 0.05
        volume = area * depth_m
        return volume, "m³"
    else:
        return 1.0, "m³"

def calculate_area(quantities: List[float]) -> Tuple[float, str]:
    if len(quantities) >= 2:
        length = quantities[0]
        width = quantities[1] if quantities[1] < 10 else 0.15
        area = length * width
        return area, "sqm"
    elif len(quantities) == 1:
        value = quantities[0]
        if value > 50:
            area = value * 0.15
            return area, "sqm"
        else:
            return value, "sqm"
    else:
        return 10.0, "sqm"

def calculate_length(quantities: List[float]) -> Tuple[float, str]:
    if len(quantities) >= 2:
        length = quantities[1] - quantities[0]
    elif len(quantities) == 1:
        length = quantities[0]
    else:
        length = 100
    if length > 1000:
        length = length * 1000
    count = max(1, int(length / 30))
    return float(count), "each"

def count_items(quantities: List[float]) -> Tuple[float, str]:
    if quantities:
        return sum(quantities), "each"
    else:
        return 1.0, "each"

def process_intervention(intervention_data: Dict, knowledge_base: Dict) -> Dict:
    intervention_type = intervention_data['intervention_type']
    sentence = intervention_data['sentence']
    if intervention_type not in knowledge_base:
        return None
    config = knowledge_base[intervention_type]
    quantities = extract_quantities(sentence, config['regex'])
    logic = config['logic']
    if logic == "calculate_volume":
        quantity, unit = calculate_volume(quantities)
    elif logic == "calculate_area":
        quantity, unit = calculate_area(quantities)
    elif logic == "calculate_length":
        quantity, unit = calculate_length(quantities)
    elif logic == "count":
        quantity, unit = count_items(quantities)
    else:
        quantity, unit = 1.0, config['default_unit']
    return {
        'intervention_type': intervention_type,
        'material_name': config['material_name'],
        'quantity': round(quantity, 2),
        'unit': unit,
        'sentence': sentence
    }

def process_all_interventions(found_interventions: List[Dict]) -> List[Dict]:
    processed = []
    for intervention in found_interventions:
        result = process_intervention(intervention, KNOWLEDGE_BASE)
        if result:
            processed.append(result)
    return processed
