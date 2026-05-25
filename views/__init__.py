"""
Módulo de vistas de la aplicación
"""
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.client_view import ClientView
from views.plant_view import PlantView
from views.equipment_view import EquipmentView
from views.inspection_view import InspectionView
from views.report_view import ReportView
from views.user_view import UserView

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