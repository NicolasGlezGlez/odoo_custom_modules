from odoo import models, fields, api
import base64
import requests # type: ignore

class ShippingOrderWizard(models.TransientModel):
    _name = 'shipping.order.wizard'
    _description = 'Shipping Order Wizard'

    shipping_company_id = fields.Many2one('shipping.company', string='Shipping Company', required=True)
    order_number = fields.Char(string='Order Number', required=True)

    def confirm_order(self):
        # Obtener la URL de la API de la compañía seleccionada
        api_url = self.shipping_company_id.api_url

        if not api_url:
            raise ValueError("No API URL configured for this shipping company.")

        # Llama a la API usando la URL configurada
        response = self._call_shipping_api(api_url, self.order_number)

        # Maneja la respuesta de la API según sea necesario
        if response:
            # Aquí podrías crear un registro en otro modelo, mostrar un mensaje, etc.
            pass

        return {'type': 'ir.actions.act_window_close'}

    def _call_shipping_api(self, api_url, order_number):
        """
        Llama a la API utilizando la URL configurada y el número de pedido.
        """
        # Formatea la URL completa con el número de pedido
        url = f"{api_url}/{order_number}"
        if self.shipping_company_id.name == 'Correos':
            return self._call_correos_api(order_number, self.shipping_company_id.username, self.shipping_company_id.password)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to fetch data from API. Status code: {response.status_code}")

    def _call_correos_api(self, order_number, username, password):
        api_url = "https://localizador.correos.es/canonico/eventos_envio_servicio_auth"
        auth_str = f"{username}:{password}"
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(auth_str.encode()).decode(),
            'Content-Type': 'application/json',
        }
        params = {
            'codIdioma': 'ES',
            'indUltEvento': 'N'
        }
        response = requests.get(f"{api_url}/{order_number}", headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error {response.status_code}: {response.text}")
