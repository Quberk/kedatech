Module Overview
This module provides a REST API to manage materials that are intended for sale. It includes:

Creating a material

Listing materials (with optional filtering by material type)

Updating material information

Deleting a material

Each material record includes:

Material Code

Material Name

Material Type (Fabric, Jeans, Cotton)

Buy Price (must be ≥ 100)

Related Supplier

API Endpoints
All endpoints use type='json' and support POST only methods.
endpoints:
1. /api/materials/create
    params: code, name, material_type, buy_price, supplier_id
2. /api/materials/get
    params: material_type
3. /api/materials/update
    params: material_id, code, name, material_type, buy_price, supplier_id
4. /api/materials/delete
    params: maaterial_id