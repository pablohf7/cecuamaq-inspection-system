"""
CECUAMAQ - Sistema de Inspecciones Industriales
Aplicación principal
"""
import sys
from pathlib import Path

# FIX: Agregar la raíz del proyecto al PYTHONPATH
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

import flet as ft

try:
    from app.config import check_db_connection, init_db, settings
    from app.utils import logger
    from app.views.login_view import LoginView
    from app.views.dashboard_view import DashboardView
    from app.views.client_view import ClientView
    from app.views.plant_view import PlantView
    from app.views.equipment_view import EquipmentView
    from app.views.inspection_view import InspectionView
    from app.views.report_view import ReportView
    from app.views.user_view import UserView
except ImportError as e:
    print(f"ERROR: No se pueden importar los módulos necesarios: {e}")
    print(f"Asegúrate de que:")
    print(f"1. Estás en la carpeta raíz del proyecto")
    print(f"2. La carpeta 'app' existe")
    print(f"3. Los archivos __init__.py existen en app/ y subcarpetas")
    sys.exit(1)


class CecuamaqApp:
    """Aplicación principal"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_user = None
        self.current_view = None
        self.configure_page()
        
    def configure_page(self):
        """Configurar página principal"""
        self.page.title = settings.APP_NAME
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        
        # Verificar conexión a BD
        if not check_db_connection():
            self.show_error("No se pudo conectar a la base de datos")
            return
        
        # Inicializar BD
        try:
            init_db()
            logger.info("Base de datos inicializada correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar BD: {e}")
            self.show_error(f"Error al inicializar base de datos: {e}")
            return
        
        # Mostrar pantalla de login
        self.show_login()
    
    def show_login(self):
        """Mostrar pantalla de login"""
        
        # Campos de formulario
        username_field = ft.TextField(
            label="Usuario",
            prefix_icon=ft.icons.PERSON,
            width=300,
            autofocus=True
        )
        
        password_field = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=300
        )
        
        error_text = ft.Text(value="", color=ft.colors.RED, size=12)
        
        def on_login(e):
            """Manejar login"""
            if not username_field.value or not password_field.value:
                error_text.value = "Por favor ingrese usuario y contraseña"
                self.page.update()
                return
            
            # TODO: Implementar autenticación real
            # Por ahora login simple para demostración
            if username_field.value == "admin" and password_field.value == "admin":
                self.current_user = username_field.value
                logger.info(f"Login exitoso: {username_field.value}")
                self.show_dashboard()
            else:
                error_text.value = "Usuario o contraseña incorrectos"
                self.page.update()
        
        login_button = ft.ElevatedButton(
            "Iniciar Sesión",
            width=300,
            on_click=on_login
        )
        
        # Layout de login
        login_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=50),
                    ft.Icon(ft.icons.FACTORY, size=80, color=ft.colors.BLUE),
                    ft.Text(
                        "CECUAMAQ",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE
                    ),
                    ft.Text(
                        "Sistema de Inspecciones Industriales",
                        size=16,
                        color=ft.colors.GREY
                    ),
                    ft.Container(height=30),
                    username_field,
                    password_field,
                    error_text,
                    ft.Container(height=10),
                    login_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.BLUE_50, ft.colors.BLUE_100]
            )
        )
        
        self.page.controls.clear()
        self.page.add(login_container)
        self.page.update()
    
    def show_dashboard(self):
        """Mostrar dashboard principal con navegación"""
        
        # AppBar
        app_bar = ft.AppBar(
            title=ft.Text("CECUAMAQ - Dashboard"),
            center_title=False,
            bgcolor=ft.colors.BLUE,
            actions=[
                ft.IconButton(
                    ft.icons.NOTIFICATIONS,
                    tooltip="Notificaciones",
                    icon_color=ft.colors.WHITE
                ),
                ft.IconButton(
                    ft.icons.SETTINGS,
                    tooltip="Configuración",
                    icon_color=ft.colors.WHITE
                ),
                ft.IconButton(
                    ft.icons.LOGOUT,
                    tooltip="Cerrar Sesión",
                    icon_color=ft.colors.WHITE,
                    on_click=lambda e: self.logout()
                ),
            ]
        )
        
        # Menú lateral con navegación funcional
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.icons.DASHBOARD,
                    label="Dashboard"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.BUSINESS_OUTLINED,
                    selected_icon=ft.icons.BUSINESS,
                    label="Clientes"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.FACTORY_OUTLINED,
                    selected_icon=ft.icons.FACTORY,
                    label="Plantas"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PRECISION_MANUFACTURING_OUTLINED,
                    selected_icon=ft.icons.PRECISION_MANUFACTURING,
                    label="Equipos"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.FACT_CHECK_OUTLINED,
                    selected_icon=ft.icons.FACT_CHECK,
                    label="Inspecciones"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ASSESSMENT_OUTLINED,
                    selected_icon=ft.icons.ASSESSMENT,
                    label="Reportes"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE_OUTLINED,
                    selected_icon=ft.icons.PEOPLE,
                    label="Usuarios"
                ),
            ],
            on_change=lambda e: self.on_navigation_change(e.control.selected_index)
        )
        
        # Contenedor para contenido dinámico
        self.content_container = ft.Container(
            expand=True,
            padding=0
        )
        
        # Layout principal
        main_layout = ft.Row(
            [
                self.nav_rail,
                ft.VerticalDivider(width=1),
                self.content_container
            ],
            expand=True,
            spacing=0
        )
        
        # Configurar página
        self.page.controls.clear()
        self.page.appbar = app_bar
        self.page.add(main_layout)
        
        # Mostrar vista inicial (Dashboard)
        self.navigate_to("dashboard")
    
    def on_navigation_change(self, index: int):
        """Manejar cambio de navegación"""
        views = {
            0: "dashboard",
            1: "clients",
            2: "plants",
            3: "equipment",
            4: "inspections",
            5: "reports",
            6: "users"
        }
        
        view_name = views.get(index, "dashboard")
        self.navigate_to(view_name)
    
    def navigate_to(self, view_name: str):
        """Navegar a una vista específica"""
        
        # Actualizar título del AppBar
        titles = {
            "dashboard": "CECUAMAQ - Dashboard",
            "clients": "CECUAMAQ - Clientes",
            "plants": "CECUAMAQ - Plantas",
            "equipment": "CECUAMAQ - Equipos",
            "inspections": "CECUAMAQ - Inspecciones",
            "reports": "CECUAMAQ - Reportes",
            "users": "CECUAMAQ - Usuarios"
        }
        
        if self.page.appbar:
            self.page.appbar.title = ft.Text(titles.get(view_name, "CECUAMAQ"))
        
        # Crear la vista correspondiente
        try:
            if view_name == "dashboard":
                # Vista dashboard con las tarjetas de estadísticas
                view_content = self.create_dashboard_content()
            elif view_name == "clients":
                view = ClientView(self.page)
                view_content = view.build()
            elif view_name == "plants":
                view = PlantView(self.page)
                view_content = view.build()
            elif view_name == "equipment":
                view = EquipmentView(self.page)
                view_content = view.build()
            elif view_name == "inspections":
                view = InspectionView(self.page)
                view_content = view.build()
            elif view_name == "reports":
                view = ReportView(self.page)
                view_content = view.build()
            elif view_name == "users":
                view = UserView(self.page)
                view_content = view.build()
            else:
                view_content = self.create_dashboard_content()
            
            # Actualizar contenido
            self.content_container.content = view_content
            self.current_view = view_name
            self.page.update()
            
            logger.info(f"Navegando a: {view_name}")
            
        except Exception as e:
            logger.error(f"Error al cargar vista {view_name}: {e}")
            self.show_snackbar(f"Error al cargar vista: {e}", ft.colors.RED)
    
    def create_dashboard_content(self):
        """Crear contenido del dashboard - AJUSTADO AL TOPE"""
        # Estadísticas
        stats_row = ft.Row(
            [
                self.create_stat_card("Total Clientes", "15", ft.icons.BUSINESS, ft.colors.BLUE),
                self.create_stat_card("Inspecciones", "248", ft.icons.FACT_CHECK, ft.colors.GREEN),
                self.create_stat_card("Equipos", "342", ft.icons.PRECISION_MANUFACTURING, ft.colors.ORANGE),
                self.create_stat_card("Pendientes", "12", ft.icons.WARNING, ft.colors.RED),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            wrap=True
        )
        
        # Contenido principal del dashboard - SIN ESPACIOS SUPERIORES
        main_content = ft.Column(
            [
                ft.Text(
                    "Bienvenido al Sistema de Inspecciones",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(height=15),
                stats_row,
                ft.Container(height=20),
                ft.Text(
                    "Inspecciones Recientes",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(height=10),
                self.create_recent_inspections_table(),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.START
        )
        
        return ft.Container(
            content=main_content,
            expand=True,
            padding=ft.padding.only(left=20, right=20, top=0, bottom=20)
        )
    
    def create_stat_card(self, title: str, value: str, icon, color):
        """Crear tarjeta de estadística"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(icon, size=40, color=color),
                            ft.Column(
                                [
                                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD),
                                    ft.Text(title, size=14, color=ft.colors.GREY),
                                ],
                                spacing=0
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            width=250,
            height=120,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.BLUE_GREY_100)
        )
    
    def create_recent_inspections_table(self):
        """Crear tabla de inspecciones recientes"""
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("N° Inspección")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Equipo")),
                ft.DataColumn(ft.Text("Inspector")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Estado")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("INS-2024-000001")),
                        ft.DataCell(ft.Text("Empresa Industrial S.A.")),
                        ft.DataCell(ft.Text("Bomba Centrífuga BCP-001")),
                        ft.DataCell(ft.Text("Juan Pérez")),
                        ft.DataCell(ft.Text("15/05/2024")),
                        ft.DataCell(ft.Container(
                            content=ft.Text("Completada", color=ft.colors.WHITE),
                            bgcolor=ft.colors.GREEN,
                            padding=5,
                            border_radius=5
                        )),
                    ]
                ),
            ],
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5,
        )
    
    def logout(self):
        """Cerrar sesión"""
        self.current_user = None
        self.current_view = None
        logger.info("Sesión cerrada")
        self.show_login()
    
    def show_error(self, message: str):
        """Mostrar mensaje de error"""
        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.close_dialog(error_dialog))
            ]
        )
        self.page.dialog = error_dialog
        error_dialog.open = True
        self.page.update()
    
    def close_dialog(self, dialog):
        """Cerrar diálogo"""
        dialog.open = False
        self.page.update()
    
    def show_snackbar(self, message: str, color=ft.colors.BLUE):
        """Mostrar snackbar"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()


def main(page: ft.Page):
    """Función principal"""
    CecuamaqApp(page)


if __name__ == "__main__":
    logger.info("Iniciando aplicación CECUAMAQ...")
    ft.app(target=main)