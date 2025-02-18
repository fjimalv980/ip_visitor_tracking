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

    def obtener_ip_publica(self):
        """Obtener la IP pública del visitante utilizando un servicio externo."""
        try:
            ip = requests.get("https://api.ipify.org").text
            return ip
        except requests.exceptions.RequestException as e:
            _logger.error("Error al obtener la IP pública: %s", str(e))
            return None

    def get_geolocation_data(self):
        """Obtiene la geolocalización de la IP proporcionada o la IP pública si no se proporciona."""
        if not self.ip_address:
            # Si no se proporciona la IP, obtenerla automáticamente
            self.ip_address = self.obtener_ip_publica()
            if not self.ip_address:
                raise UserError("No se pudo obtener la dirección IP del visitante.")

        _logger.info("Obteniendo geolocalización para la IP: %s", self.ip_address)

        # URL de la API de geolocalización
        api_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={self.api_key}&ip={self.ip_address}"
        try:
            # Solicitar la geolocalización
            response = requests.get(api_url)
            
            # Verificar la respuesta de la API
            if response.status_code == 200:
                data = response.json()
                _logger.info("Datos obtenidos de la API: %s", data)
                
                # Actualizar los campos del modelo con los datos de geolocalización
                self.write({
                    'country': data.get('country_name'),
                    'city': data.get('city'),
                    'longitude': data.get('longitude'),
                    'latitude': data.get('latitude'),
                    'isp': data.get('isp'),
                    'organization': data.get('organization'),
                    'visit_time': fields.Datetime.now(),
                })
                _logger.info("Datos de geolocalización actualizados exitosamente.")
            elif response.status_code == 403:
                _logger.error("Acceso prohibido a la API de geolocalización: %s", response.text)
                raise UserError(f"Acceso prohibido a la API de geolocalización. Código 403: {response.text}")
            else:
                _logger.error("Error en la API de geolocalización: %s", response.text)
                raise UserError(f"Error al obtener los datos de geolocalización. Código de respuesta: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            _logger.error("Error al intentar obtener los datos de geolocalización: %s", str(e))
            raise UserError("Hubo un error al conectarse a la API de ipgeolocation.io")

