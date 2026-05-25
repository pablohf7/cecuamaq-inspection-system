"""
Vista de Inspecciones
"""
import flet as ft
from datetime import datetime


class InspectionView:
    """Vista de gestión de inspecciones"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self) -> ft.Container:
        """Construir vista de inspecciones"""
        
        # Filtros
        filter_row = ft.Row(
            [
                ft.Dropdown(
                    label="Cliente",
                    width=200,
                    options=[
                        ft.dropdown.Option("Todos"),
                        # TODO: Cargar clientes desde BD
                    ]
                ),
                ft.Dropdown(
                    label="Estado",
                    width=150,
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("Pendiente"),
                        ft.dropdown.Option("En Progreso"),
                        ft.dropdown.Option("Completada"),
                        ft.dropdown.Option("Cancelada"),
                    ]
                ),
                ft.TextField(
                    label="Fecha Desde",
                    width=150,
                    hint_text="dd/mm/yyyy"
                ),
                ft.TextField(
                    label="Fecha Hasta",
                    width=150,
                    hint_text="dd/mm/yyyy"
                ),
                ft.ElevatedButton(
                    "Buscar",
                    icon=ft.icons.SEARCH
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Nueva Inspección",
                    icon=ft.icons.ADD,
                    on_click=lambda e: self.show_new_inspection_dialog()
                )
            ],
            wrap=True,
            spacing=10
        )
        
        # Tabla de inspecciones
        inspections_table = self.create_inspections_table()
        
        content = ft.Column(
            [
                ft.Text(
                    "Gestión de Inspecciones",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(height=20),
                filter_row,
                ft.Container(height=20),
                inspections_table
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        return ft.Container(
            content=content,
            padding=20,
            expand=True
        )
    
    def create_inspections_table(self):
        """Crear tabla de inspecciones"""
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("N° Inspección")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Equipo")),
                ft.DataColumn(ft.Text("Inspector")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Parámetros")),
                ft.DataColumn(ft.Text("Fotos")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],  # TODO: Cargar datos
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5,
            heading_row_color=ft.colors.BLUE_50,
        )
    
    def show_new_inspection_dialog(self):
        """Mostrar diálogo para nueva inspección"""
        # TODO: Implementar formulario completo de inspección
        pass