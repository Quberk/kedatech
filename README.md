Module Overview \n
    This module provides a REST API to manage materials that are intended for sale. It includes:

    - Creating a material
    - Listing materials (with optional filtering by material type)
    - Updating material information
    - Deleting a material
    - Each material record includes:
    - Material Code
    - Material Name
    - Material Type (Fabric, Jeans, Cotton)
    - Buy Price (must be ≥ 100)
    - Related Supplier

API Endpoints
    All endpoints use type='json' and support POST only methods.
    endpoints:
    - "/api/materials/create"
            params: code, name, material_type, buy_price, supplier_id
    - "/api/materials/get"
            params: material_type
    - "/api/materials/update"
            params: material_id, code, name, material_type, buy_price, supplier_id
    - "/api/materials/delete"
            params: maaterial_id

HOW TO RUN Unit Tests:
    ./odoo-bin -d <your_database_name> -i <your_module_name> --test-enable --stop-after-init
