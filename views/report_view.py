"""
Vista de Reportes
"""
import flet as ft
from datetime import datetime


class ReportView:
    """Vista de generación de reportes"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self) -> ft.Container:
        """Construir vista de reportes"""
        
        # Sección de filtros
        filters_section = ft.Container(
            content=ft.Column([
                ft.Text("Filtros de Reporte", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                
                ft.Row([
                    ft.Dropdown(
                        label="Tipo de Reporte",
                        width=250,
                        value="inspecciones",
                        options=[
                            ft.dropdown.Option("inspecciones", "Inspecciones"),
                            ft.dropdown.Option("clientes", "Clientes"),
                            ft.dropdown.Option("equipos", "Equipos"),
                            ft.dropdown.Option("parametros", "Parámetros"),
                            ft.dropdown.Option("estadisticas", "Estadísticas"),
                        ],
                        on_change=lambda e: self.change_report_type(e.control.value)
                    ),
                    ft.Dropdown(
                        label="Cliente",
                        width=250,
                        options=[
                            ft.dropdown.Option("todos", "Todos"),
                            ft.dropdown.Option("1", "Empresa Industrial S.A."),
                        ]
                    ),
                ]),
                
                ft.Row([
                    ft.TextField(
                        label="Fecha Desde",
                        width=200,
                        hint_text="dd/mm/yyyy",
                        value=datetime.now().strftime("%d/%m/%Y")
                    ),
                    ft.TextField(
                        label="Fecha Hasta",
                        width=200,
                        hint_text="dd/mm/yyyy",
                        value=datetime.now().strftime("%d/%m/%Y")
                    ),
                    ft.Dropdown(
                        label="Estado",
                        width=200,
                        options=[
                            ft.dropdown.Option("todos", "Todos"),
                            ft.dropdown.Option("completada", "Completada"),
                            ft.dropdown.Option("pendiente", "Pendiente"),
                            ft.dropdown.Option("en_progreso", "En Progreso"),
                        ]
                    ),
                ]),
                
                ft.Row([
                    ft.Dropdown(
                        label="Inspector",
                        width=250,
                        options=[
                            ft.dropdown.Option("todos", "Todos"),
                            ft.dropdown.Option("1", "Juan Pérez"),
                        ]
                    ),
                    ft.Dropdown(
                        label="Equipo",
                        width=250,
                        options=[
                            ft.dropdown.Option("todos", "Todos"),
                        ]
                    ),
                ]),
                
                ft.Container(height=10),
                ft.Row([
                    ft.ElevatedButton(
                        "Generar Vista Previa",
                        icon=ft.icons.PREVIEW,
                        on_click=lambda e: self.generate_preview()
                    ),
                    ft.ElevatedButton(
                        "Exportar a Excel",
                        icon=ft.icons.DOWNLOAD,
                        on_click=lambda e: self.export_to_excel()
                    ),
                    ft.ElevatedButton(
                        "Exportar a PDF",
                        icon=ft.icons.PICTURE_AS_PDF,
                        on_click=lambda e: self.export_to_pdf()
                    ),
                ], spacing=10),
            ]),
            padding=20,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            bgcolor=ft.colors.WHITE
        )
        
        # Vista previa
        preview_section = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Vista Previa", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.icons.REFRESH,
                        tooltip="Actualizar",
                        on_click=lambda e: self.generate_preview()
                    )
                ]),
                ft.Divider(),
                
                # Tabla de preview
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("N° Inspección")),
                        ft.DataColumn(ft.Text("Fecha")),
                        ft.DataColumn(ft.Text("Cliente")),
                        ft.DataColumn(ft.Text("Equipo")),
                        ft.DataColumn(ft.Text("Inspector")),
                        ft.DataColumn(ft.Text("Estado")),
                        ft.DataColumn(ft.Text("Parámetros")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("INS-2024-000001")),
                                ft.DataCell(ft.Text("15/05/2024")),
                                ft.DataCell(ft.Text("Empresa Industrial S.A.")),
                                ft.DataCell(ft.Text("BCP-001")),
                                ft.DataCell(ft.Text("Juan Pérez")),
                                ft.DataCell(ft.Text("Completada")),
                                ft.DataCell(ft.Text("8")),
                            ]
                        ),
                    ],
                    border=ft.border.all(1, ft.colors.GREY_300),
                    heading_row_color=ft.colors.BLUE_50,
                ),
                
                ft.Container(height=20),
                ft.Text("Total de registros: 1", color=ft.colors.GREY),
            ], scroll=ft.ScrollMode.AUTO),
            padding=20,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            expand=True
        )
        
        # Reportes predefinidos
        predefined_section = ft.Container(
            content=ft.Column([
                ft.Text("Reportes Predefinidos", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                
                ft.ListTile(
                    leading=ft.Icon(ft.icons.DESCRIPTION),
                    title=ft.Text("Inspecciones del Mes"),
                    subtitle=ft.Text("Todas las inspecciones del mes actual"),
                    trailing=ft.IconButton(
                        icon=ft.icons.PLAY_ARROW,
                        on_click=lambda e: self.run_predefined_report("month")
                    )
                ),
                
                ft.ListTile(
                    leading=ft.Icon(ft.icons.DESCRIPTION),
                    title=ft.Text("Equipos Críticos"),
                    subtitle=ft.Text("Equipos con parámetros fuera de rango"),
                    trailing=ft.IconButton(
                        icon=ft.icons.PLAY_ARROW,
                        on_click=lambda e: self.run_predefined_report("critical")
                    )
                ),
                
                ft.ListTile(
                    leading=ft.Icon(ft.icons.DESCRIPTION),
                    title=ft.Text("Inspecciones Pendientes"),
                    subtitle=ft.Text("Inspecciones no completadas"),
                    trailing=ft.IconButton(
                        icon=ft.icons.PLAY_ARROW,
                        on_click=lambda e: self.run_predefined_report("pending")
                    )
                ),
                
                ft.ListTile(
                    leading=ft.Icon(ft.icons.DESCRIPTION),
                    title=ft.Text("Reporte por Inspector"),
                    subtitle=ft.Text("Estadísticas por inspector"),
                    trailing=ft.IconButton(
                        icon=ft.icons.PLAY_ARROW,
                        on_click=lambda e: self.run_predefined_report("inspector")
                    )
                ),
            ]),
            padding=20,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            bgcolor=ft.colors.WHITE
        )
        
        content = ft.Column(
            [
                ft.Row([
                    ft.Icon(ft.icons.ASSESSMENT, size=30, color=ft.colors.BLUE),
                    ft.Text(
                        "Generación de Reportes",
                        size=24,
                        weight=ft.FontWeight.BOLD
                    ),
                ]),
                ft.Divider(),
                ft.Container(height=10),
                
                ft.Row([
                    ft.Container(
                        content=filters_section,
                        width=400
                    ),
                    ft.Container(width=20),
                    ft.Container(
                        content=predefined_section,
                        width=350
                    ),
                ], vertical_alignment=ft.CrossAxisAlignment.START),
                
                ft.Container(height=20),
                preview_section,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        return ft.Container(
            content=content,
            padding=20,
            expand=True
        )
    
    def change_report_type(self, report_type: str):
        """Cambiar tipo de reporte"""
        # TODO: Ajustar campos según tipo
        pass
    
    def generate_preview(self):
        """Generar vista previa del reporte"""
        # TODO: Consultar datos y mostrar preview
        self.show_snackbar("Generando vista previa...", ft.colors.BLUE)
    
    def export_to_excel(self):
        """Exportar reporte a Excel"""
        # TODO: Usar ExportService para generar Excel
        self.show_snackbar("Exportando a Excel...", ft.colors.GREEN)
        
        # Simular exportación
        import time
        time.sleep(1)
        self.show_snackbar("Reporte exportado: exports/reporte_20240525.xlsx", ft.colors.GREEN)
    
    def export_to_pdf(self):
        """Exportar reporte a PDF"""
        # TODO: Implementar exportación a PDF
        self.show_snackbar("Exportación a PDF en desarrollo", ft.colors.ORANGE)
    
    def run_predefined_report(self, report_type: str):
        """Ejecutar reporte predefinido"""
        # TODO: Implementar reportes predefinidos
        self.show_snackbar(f"Ejecutando reporte: {report_type}", ft.colors.BLUE)
    
    def show_snackbar(self, message: str, color):
        """Mostrar snackbar"""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()