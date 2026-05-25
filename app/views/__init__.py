"""
Módulo de vistas de la aplicación
"""
from app.views.login_view import LoginView
from app.views.dashboard_view import DashboardView
from app.views.client_view import ClientView
from app.views.plant_view import PlantView
from app.views.equipment_view import EquipmentView
from app.views.inspection_view import InspectionView
from app.views.report_view import ReportView
from app.views.user_view import UserView

__all__ = [
    'LoginView',
    'DashboardView',
    'ClientView',
    'PlantView',
    'EquipmentView',
    'InspectionView',
    'ReportView',
    'UserView'
]