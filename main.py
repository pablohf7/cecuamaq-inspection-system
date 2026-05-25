"""
CECUAMAQ - Sistema de Inspecciones Industriales
Aplicación principal
"""
import flet as ft
from .config import check_db_connection, init_db, settings
from .utils import logger


class CecuamaqApp:
    """Aplicación principal"""
    
    def __init__(self, page: ft.Page):
        self.page = page
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
            if username_field.value == "admin" and password_field.value == "Admin123!":
                logger.info(f"Login exitoso: {username_field.value}")
                self.show_dashboard()
            else:
                error_text.value = "Usuario o contraseña incorrectos"
                self.page.update()
        
        login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
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
        """Mostrar dashboard principal"""
        
        # AppBar
        app_bar = ft.AppBar(
            title=ft.Text("CECUAMAQ - Dashboard"),
            center_title=False,
            bgcolor=ft.colors.BLUE,
            actions=[
                ft.IconButton(ft.icons.NOTIFICATIONS, tooltip="Notificaciones"),
                ft.IconButton(ft.icons.SETTINGS, tooltip="Configuración"),
                ft.IconButton(ft.icons.LOGOUT, tooltip="Cerrar Sesión", on_click=lambda e: self.show_login()),
            ]
        )
        
        # Estadísticas
        stats_row = ft.Row(
            [
                self.create_stat_card("Total Clientes", "15", ft.icons.BUSINESS, ft.colors.BLUE),
                self.create_stat_card("Inspecciones", "248", ft.icons.FACT_CHECK, ft.colors.GREEN),
                self.create_stat_card("Equipos", "342", ft.icons.PRECISION_MANUFACTURING, ft.colors.ORANGE),
                self.create_stat_card("Pendientes", "12", ft.icons.WARNING, ft.colors.RED),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
        
        # Menú lateral
        nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.DASHBOARD,
                    selected_icon=ft.icons.DASHBOARD,
                    label="Dashboard"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.BUSINESS,
                    selected_icon=ft.icons.BUSINESS,
                    label="Clientes"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.FACTORY,
                    selected_icon=ft.icons.FACTORY,
                    label="Plantas"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PRECISION_MANUFACTURING,
                    selected_icon=ft.icons.PRECISION_MANUFACTURING,
                    label="Equipos"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.FACT_CHECK,
                    selected_icon=ft.icons.FACT_CHECK,
                    label="Inspecciones"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ASSESSMENT,
                    selected_icon=ft.icons.ASSESSMENT,
                    label="Reportes"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE,
                    selected_icon=ft.icons.PEOPLE,
                    label="Usuarios"
                ),
            ],
        )
        
        # Contenido principal
        main_content = ft.Column(
            [
                ft.Container(height=20),
                ft.Text("Bienvenido al Sistema de Inspecciones", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                stats_row,
                ft.Container(height=30),
                ft.Text("Inspecciones Recientes", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                self.create_recent_inspections_table(),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        # Layout principal
        main_layout = ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(width=1),
                ft.Container(
                    content=main_content,
                    expand=True,
                    padding=20
                )
            ],
            expand=True
        )
        
        self.page.controls.clear()
        self.page.appbar = app_bar
        self.page.add(main_layout)
        self.page.update()
    
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
                                ]
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
                # Más filas de ejemplo...
            ],
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5,
        )
    
    def show_error(self, message: str):
        """Mostrar mensaje de error"""
        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.close(error_dialog))
            ]
        )
        self.page.dialog = error_dialog
        error_dialog.open = True
        self.page.update()


def main(page: ft.Page):
    """Función principal"""
    CecuamaqApp(page)


if __name__ == "__main__":
    logger.info("Iniciando aplicación CECUAMAQ...")
    ft.app(target=main)
