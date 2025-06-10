# -*- coding: utf-8 -*-
# from odoo import http


# class MaterialSale(http.Controller):
#     @http.route('/material_sale/material_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/material_sale/material_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('material_sale.listing', {
#             'root': '/material_sale/material_sale',
#             'objects': http.request.env['material_sale.material_sale'].search([]),
#         })

#     @http.route('/material_sale/material_sale/objects/<model("material_sale.material_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('material_sale.object', {
#             'object': obj
#         })
