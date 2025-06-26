from pydantic import BaseModel
from typing import List

class Vendor(BaseModel):
    id: int
    name: str
    logo: str
    rating: float
    category: int  # Use category id

class VendorCategory(BaseModel):
    id: int
    name: str

VENDOR_CATEGORIES: List[VendorCategory] = [
    VendorCategory(id=0, name="All"),
    VendorCategory(id=1, name="Books"),
    VendorCategory(id=2, name="Poems"),
    VendorCategory(id=3, name="Special for you"),
    VendorCategory(id=4, name="Stationery"),
]

VENDORS: List[Vendor] = [
    Vendor(id=1, name="Wattpad", logo="https://example.com/wattpad_logo.png", rating=4.0, category=1),
    Vendor(id=2, name="Kuromi", logo="https://example.com/kuromi_logo.png", rating=5.0, category=3),
    Vendor(id=3, name="Crane & Co", logo="https://example.com/crane_logo.png", rating=4.0, category=4),
    Vendor(id=4, name="GooDay", logo="https://example.com/gooday_logo.png", rating=4.0, category=1),
    Vendor(id=5, name="Warehouse", logo="https://example.com/warehouse_logo.png", rating=3.0, category=4),
    Vendor(id=6, name="Peppa Pig", logo="https://example.com/peppapig_logo.png", rating=5.0, category=3),
    Vendor(id=7, name="Jstor", logo="https://example.com/jstor_logo.png", rating=4.0, category=1),
    Vendor(id=8, name="Peloton", logo="https://example.com/peloton_logo.png", rating=5.0, category=3),
    Vendor(id=9, name="Haymarket", logo="https://example.com/haymarket_logo.png", rating=4.0, category=1),
]
