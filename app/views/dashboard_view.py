"""
Vista de Dashboard
"""
import flet as ft
from typing import Callable


class DashboardView:
    """Vista del dashboard principal"""
    
    def __init__(self, page: ft.Page, on_navigate: Callable):
        self.page = page
        self.on_navigate = on_navigate
        
        
    def build(self) -> ft.Container:
        """Construir vista de dashboard"""
        
        # Estadísticas
        stats_row = ft.Row(
            [
                self.create_stat_card(
                    "Total Clientes",
                    "15",
                    ft.icons.BUSINESS,
                    ft.colors.BLUE
                ),
                self.create_stat_card(
                    "Inspecciones",
                    "248",
                    ft.icons.FACT_CHECK,
                    ft.colors.GREEN
                ),
                self.create_stat_card(
                    "Equipos",
                    "342",
                    ft.icons.PRECISION_MANUFACTURING,
                    ft.colors.ORANGE
                ),
                self.create_stat_card(
                    "Pendientes",
                    "12",
                    ft.icons.WARNING,
                    ft.colors.RED
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            wrap=True
        )
        
        # Contenido principal
        content = ft.Column(
            [
                ft.Text(
                    "Bienvenido al Sistema de Inspecciones",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(height=30),
                stats_row,
                ft.Container(height=30),
                ft.Row([
                    ft.Text(
                        "Inspecciones Recientes",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.IconButton(
                        icon=ft.icons.REFRESH,
                        tooltip="Actualizar",
                        on_click=lambda e: self.refresh_data()
                    )
                ]),
                ft.Container(height=10),
                self.create_recent_inspections_table(),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.START
        )
        
        return ft.Container(
            content=content,
            padding=ft.padding.only(left=20, right=20, top=0, bottom=20),
            expand=True
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
                                    ft.Text(
                                        value,
                                        size=28,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        title,
                                        size=14,
                                        color=ft.colors.GREY
                                    ),
                                ],
                                spacing=0
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=15
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=250,
            height=120,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            padding=15,
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=1,
                color=ft.colors.BLUE_GREY_100
            )
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
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("INS-2024-000001")),
                        ft.DataCell(ft.Text("Empresa Industrial S.A.")),
                        ft.DataCell(ft.Text("Bomba Centrífuga BCP-001")),
                        ft.DataCell(ft.Text("Juan Pérez")),
                        ft.DataCell(ft.Text("15/05/2024")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    "Completada",
                                    color=ft.colors.WHITE,
                                    size=12
                                ),
                                bgcolor=ft.colors.GREEN,
                                padding=5,
                                border_radius=5
                            )
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.VISIBILITY,
                                    tooltip="Ver",
                                    icon_size=20
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DOWNLOAD,
                                    tooltip="Descargar",
                                    icon_size=20
                                )
                            ], spacing=0)
                        ),
                    ]
                ),
            ],
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5,
            heading_row_color=ft.colors.BLUE_50,
        )
    
    def refresh_data(self):
        """Actualizar datos del dashboard"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Datos actualizados"),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()