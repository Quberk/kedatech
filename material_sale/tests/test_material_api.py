from odoo.tests.common import TransactionCase, HttpCase, tagged
import json


@tagged('-at_install', 'post_install')
class TestMaterialApi(HttpCase):

    def setUp(self):
        print("Test Setup")
        super().setUp()
        self.env = self.env(context=dict(self.env.context, test_queue_job_no_delay=True))
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier'
        })
        self.test_material_data = {
            "code": "M001",
            "name": "Test Cotton",
            "material_type": "cotton",
            "buy_price": 150.0,
            "supplier_id": self.supplier.id
        }

    def _call_json(self, route, params=None, method='POST'):
        """Helper to call JSON endpoint in test"""
        print("Test _call_json")

        params = params or {}
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "call",
            "params": params,
            "id": 1
        })

        response = self.url_open(
            url=route,
            data=payload,
            headers=headers
        )
        print("response:", response)
        if hasattr(response, 'content'):
            response_text = response.content.decode('utf-8')
            
        else:
            response_text = ""

        print("response_text:", response_text)
        return json.loads(response_text)

    def test_01_create_material(self):
        print("Test test_01_create_material")
        
        res = self._call_json('/api/materials/create', self.test_material_data)
        self.assertEqual(res["result"].get("status"), "success")
        material_id = res["result"]["data"]["id"]
        material = self.env['material.material'].browse(material_id)
        self.assertEqual(material.code, "M001")

    def test_02_create_invalid_price(self):
        print("Test test_02_create_invalid_price")
        
        invalid_data = self.test_material_data.copy()
        invalid_data["buy_price"] = 50
        res = self._call_json('/api/materials/create', invalid_data)
        res = res["result"]
        self.assertIn("error", res)
        self.assertEqual(res["error"], "Buy Price must be >= 100")

    def test_03_list_materials(self):
        print("Test test_03_list_materials")
        
        # Create a test material
        self._call_json('/api/materials/create', self.test_material_data)
        res = self._call_json('/api/materials/get', {"material_type": "cotton"})
        res = res["result"]
        self.assertEqual(res.get("status"), "success")
        self.assertTrue(any(m["material_type"] == "cotton" for m in res["data"]))

    def test_04_update_material(self):
        print("Test test_04_update_material")
        
        create_res = self._call_json('/api/materials/create', self.test_material_data)
        create_res = create_res["result"]
        mat_id = create_res["data"]["id"]
        update_data = {
            "material_id": mat_id,
            "code": "M001-UPDATED",
            "name": "Updated Cotton",
            "material_type": "cotton",
            "buy_price": 200.0,
            "supplier_id": self.supplier.id,
        }
        update_res = self._call_json('/api/materials/update', update_data)
        update_res = update_res["result"]
        self.assertTrue(update_res.get("success"), True)
        updated_mat = self.env['material.material'].browse(mat_id)
        self.assertEqual(updated_mat.name, "Updated Cotton")

    def test_05_delete_material(self):
        print("Test test_05_delete_material")
        
        create_res = self._call_json('/api/materials/create', self.test_material_data)
        create_res = create_res["result"]
        mat_id = create_res["data"]["id"]
        delete_res = self._call_json('/api/materials/delete', {"material_id": mat_id}, method='DELETE')
        delete_res = delete_res["result"]
        print("delete_res:", delete_res)
        self.assertTrue(delete_res.get("success"))
        self.assertFalse(self.env['material.material'].browse(mat_id).exists())
