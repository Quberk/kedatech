from odoo import http
from odoo.http import request, Response
import json

class MaterialController(http.Controller):


    @http.route(['/api/materials/create'], type='json', auth='public', 
                methods=["POST"], csrf=False)
    def create_material(self, code=None, name=None, material_type=None, 
                        buy_price=None, supplier_id=None):
        print("Create Material")
        code = code or ''
        name = name or ''
        material_type = material_type or ''
        buy_price = buy_price or 0.0
        supplier_id = supplier_id or 0

        if buy_price < 100:
            return {"error": "Buy Price must be >= 100"}

        material = request.env['material.material'].sudo().create({
            'code': code,
            'name': name,
            'material_type': material_type,
            'buy_price': buy_price,
            'supplier_id': supplier_id
        })
        return {"status": "success", "data": {"id": material.id}}
    

    @http.route('/api/materials/get', type='json', auth='public', 
                methods=['POST'], csrf=False)
    def list_materials(self, material_type=None):
        domain = []
        print("material_type:", str(material_type))
        if material_type:
            domain.append(('material_type', '=', material_type))
        print("domain:", str(domain))
        materials = request.env['material.material'].sudo().search_read(
            domain,
            fields=['id', 'code', 'name', 'material_type', 'buy_price', 'supplier_id']
        )

        for m in materials:
            if isinstance(m.get('supplier_id'), list):
                m['supplier_id'] = {
                    'id': m['supplier_id'][0],
                    'name': m['supplier_id'][1]
                }

        return {
            "status": "success",
            "data": materials
        }


    @http.route('/api/materials/update', type='json', auth='public',
                methods=['POST'], csrf=False)
    def update_material(self, material_id=None, code=None, name=None,
                        material_type=None, buy_price=None, supplier_id=None):
        print("Update Material")
        if not material_id:
            return {"error": "material_id is required."}
        material = request.env['material.material'].sudo().browse(material_id)
        code = code or ''
        name = name or ''
        material_type = material_type or ''
        buy_price = buy_price or 0.0
        supplier_id = supplier_id or 0
        if not material.exists():
            return {"error": "Material not found."}
        if buy_price < 100:
            return {"error": "Buy Price must be >= 100"}
        material.write({
            'code': code,
            'name': name,
            'material_type': material_type,
            'buy_price': buy_price,
            'supplier_id': supplier_id
        })
        return {"success": True}
    

    @http.route('/api/materials/delete', type='json', auth='public', 
                methods=['POST'], csrf=False)
    def delete_material(self, material_id):
        material = request.env['material.material'].sudo().browse(material_id)
        if not material.exists():
            return {"error": "Material not found."}
        material.unlink()
        return {"success": True}
