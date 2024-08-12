from odoo import models, fields, api

class ShippingCompany(models.Model):
    _name='shipping.company'
    _description='Shipping company'

    name = fields.Char(string='Name', required=True)
    api_url = fields.Char(string='API URL', required=True, help="Base URL of the API for tracking shipments.")
    username = fields.Char(string='Username', help="Username for the API authentication.")
    password = fields.Char(string='Password', help="Password for the API authentication.")


    @api.model
    def create(self, vals):
        # Normaliza la api_url eliminando el slash al final si existe
        if 'api_url' in vals:
            vals['api_url'] = self._normalize_api_url(vals['api_url'])
        return super(ShippingCompany, self).create(vals)

    def write(self, vals):
        # Normaliza la api_url eliminando el slash al final si existe
        if 'api_url' in vals:
            vals['api_url'] = self._normalize_api_url(vals['api_url'])
        return super(ShippingCompany, self).write(vals)

    @api.model
    def _normalize_api_url(self, url):
        """
        Elimina el slash al final de la URL si existe.
        """
        if url.endswith('/'):
            url = url[:-1]
        return url

