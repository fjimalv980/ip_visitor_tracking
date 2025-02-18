from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

class VisitorTracking(models.Model):
    _name = 'visitor.tracking'
    _description = 'Visitor Tracking Information'
    _rec_name = 'ip_address'

    ip_address = fields.Char(string='IP Address', readonly=True)
    country = fields.Char(string='Country', readonly=True)
    city = fields.Char(string='City', readonly=True)
    longitude = fields.Float(string='Longitude', readonly=True)
    latitude = fields.Float(string='Latitude', readonly=True)
    isp = fields.Char(string='ISP', readonly=True)
    organization = fields.Char(string='Organization', readonly=True)
    visit_time = fields.Datetime(string='Visit Time', readonly=True)
    api_key = fields.Char(string='API Key', required=True)

    def get_geolocation_data(self):
        api_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={self.api_key}&ip={self.ip_address}"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                self.write({
                    'country': data.get('country_name'),
                    'city': data.get('city'),
                    'longitude': data.get('longitude'),
                    'latitude': data.get('latitude'),
                    'isp': data.get('isp'),
                    'organization': data.get('organization'),
                    'visit_time': fields.Datetime.now(),
                })
            elif response.status_code == 403:
                _logger.error("Acceso prohibido a la API de geolocalización: %s", response.text)
            else:
                raise UserError(f"Error al obtener los datos de geolocalización. Código de respuesta: {response.status_code}")
        except requests.exceptions.RequestException as e:
            _logger.error("Error al intentar obtener los datos de geolocalización: %s", str(e))
            raise UserError("Hubo un error al conectarse a la API de ipgeolocation.io")