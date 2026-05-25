"""
Vista de Equipos
"""
import flet as ft


class EquipmentView:
    """Vista de gestión de equipos"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self) -> ft.Container:
        """Construir vista de equipos"""
        
        # Filtros y búsqueda
        filter_bar = ft.Row(
            [
                ft.TextField(
                    hint_text="Buscar por TAG o nombre...",
                    prefix_icon=ft.icons.SEARCH,
                    width=300,
                    on_change=lambda e: self.search_equipment(e.control.value)
                ),
                ft.Dropdown(
                    label="Cliente",
                    width=200,
                    options=[ft.dropdown.Option("Todos")],
                    on_change=lambda e: self.filter_equipment()
                ),
                ft.Dropdown(
                    label="Tipo de Equipo",
                    width=200,
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("Bomba Centrífuga"),
                        ft.dropdown.Option("Motor Eléctrico"),
                        ft.dropdown.Option("Compresor"),
                        ft.dropdown.Option("Ventilador"),
                    ],
                    on_change=lambda e: self.filter_equipment()
                ),
                ft.Dropdown(
                    label="Estado",
                    width=150,
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("Activo"),
                        ft.dropdown.Option("Inactivo"),
                    ],
                    on_change=lambda e: self.filter_equipment()
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Nuevo Equipo",
                    icon=ft.icons.ADD,
                    on_click=lambda e: self.show_add_equipment_dialog()
                )
            ],
            wrap=True,
            spacing=10
        )
        
        # Tabla de equipos
        equipment_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("TAG")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Ubicación")),
                ft.DataColumn(ft.Text("Fabricante")),
                ft.DataColumn(ft.Text("Modelo")),
                ft.DataColumn(ft.Text("Serie")),
                ft.DataColumn(ft.Text("Conjuntos")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("BCP-001", weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text("Bomba Centrífuga Principal")),
                        ft.DataCell(ft.Text("Bomba Centrífuga")),
                        ft.DataCell(ft.Text("Zona de Bombeo")),
                        ft.DataCell(ft.Text("Goulds")),
                        ft.DataCell(ft.Text("3196")),
                        ft.DataCell(ft.Text("GB-2024-001")),
                        ft.DataCell(ft.Text("3")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text("Activo", color=ft.colors.WHITE, size=12),
                                bgcolor=ft.colors.GREEN,
                                padding=5,
                                border_radius=5
                            )
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.VISIBILITY,
                                    tooltip="Ver Ficha Técnica",
                                    icon_size=20,
                                    on_click=lambda e: self.view_equipment_details(1)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.BUILD,
                                    tooltip="Ver Conjuntos",
                                    icon_size=20,
                                    on_click=lambda e: self.view_assemblies(1)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar",
                                    icon_size=20,
                                    on_click=lambda e: self.edit_equipment(1)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_size=20,
                                    icon_color=ft.colors.RED,
                                    on_click=lambda e: self.delete_equipment(1)
                                ),
                            ], spacing=0)
                        ),
                    ]
                ),
            ],
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5,
            heading_row_color=ft.colors.BLUE_50,
        )
        
        content = ft.Column(
            [
                ft.Row([
                    ft.Icon(ft.icons.PRECISION_MANUFACTURING, size=30, color=ft.colors.BLUE),
                    ft.Text(
                        "Gestión de Equipos",
                        size=24,
                        weight=ft.FontWeight.BOLD
                    ),
                ]),
                ft.Divider(),
                filter_bar,
                ft.Container(height=20),
                ft.Container(
                    content=equipment_table,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    bgcolor=ft.colors.WHITE
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        return ft.Container(
            content=content,
            padding=20,
            expand=True
        )
    
    def show_add_equipment_dialog(self):
        """Mostrar diálogo para agregar equipo"""
        
        # Campos jerárquicos (Cliente > Planta > Ubicación)
        client_dropdown = ft.Dropdown(
            label="Cliente *",
            width=250,
            options=[ft.dropdown.Option("1", "Empresa Industrial S.A.")],
            on_change=lambda e: self.load_plants(e.control.value)
        )
        
        plant_dropdown = ft.Dropdown(
            label="Planta *",
            width=250,
            options=[],
            on_change=lambda e: self.load_locations(e.control.value)
        )
        
        location_dropdown = ft.Dropdown(
            label="Ubicación Técnica *",
            width=250,
            options=[]
        )
        
        # Información básica
        code_field = ft.TextField(label="Código *", width=150)
        tag_field = ft.TextField(label="TAG *", width=150, hint_text="BCP-001")
        name_field = ft.TextField(label="Nombre *", width=400)
        
        equipment_type_dropdown = ft.Dropdown(
            label="Tipo de Equipo",
            width=250,
            options=[
                ft.dropdown.Option("Bomba Centrífuga"),
                ft.dropdown.Option("Bomba de Desplazamiento Positivo"),
                ft.dropdown.Option("Motor Eléctrico"),
                ft.dropdown.Option("Compresor"),
                ft.dropdown.Option("Ventilador"),
                ft.dropdown.Option("Turbina"),
                ft.dropdown.Option("Generador"),
                ft.dropdown.Option("Transformador"),
                ft.dropdown.Option("Otro"),
            ]
        )
        
        # Información del fabricante
        manufacturer_field = ft.TextField(label="Fabricante", width=200)
        model_field = ft.TextField(label="Modelo", width=150)
        serial_field = ft.TextField(label="Número de Serie", width=200)
        year_field = ft.TextField(label="Año Fabricación", width=120, hint_text="2020")
        
        # Especificaciones técnicas
        capacity_field = ft.TextField(label="Capacidad", width=150, hint_text="100 m³/h")
        power_field = ft.TextField(label="Potencia", width=150, hint_text="75 HP")
        voltage_field = ft.TextField(label="Voltaje", width=120, hint_text="460 V")
        current_field = ft.TextField(label="Corriente", width=120, hint_text="100 A")
        rpm_field = ft.TextField(label="RPM", width=120, hint_text="1750")
        
        notes_field = ft.TextField(
            label="Notas / Observaciones",
            width=550,
            multiline=True,
            min_lines=3,
            max_lines=5
        )
        
        def save_equipment(e):
            # Validaciones
            if not all([client_dropdown.value, plant_dropdown.value, 
                       location_dropdown.value, code_field.value, 
                       tag_field.value, name_field.value]):
                self.show_snackbar("Complete todos los campos obligatorios (*)", ft.colors.RED)
                return
            
            # TODO: Guardar en BD
            dlg.open = False
            self.page.update()
            self.show_snackbar("Equipo creado exitosamente", ft.colors.GREEN)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Nuevo Equipo"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Ubicación", weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([client_dropdown, plant_dropdown]),
                    location_dropdown,
                    ft.Divider(),
                    
                    ft.Text("Información Básica", weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([code_field, tag_field]),
                    name_field,
                    equipment_type_dropdown,
                    ft.Divider(),
                    
                    ft.Text("Fabricante", weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([manufacturer_field, model_field]),
                    ft.Row([serial_field, year_field]),
                    ft.Divider(),
                    
                    ft.Text("Especificaciones Técnicas", weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([capacity_field, power_field]),
                    ft.Row([voltage_field, current_field, rpm_field]),
                    ft.Divider(),
                    
                    notes_field,
                ], tight=True, spacing=10, scroll=ft.ScrollMode.AUTO),
                width=600,
                height=600
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(dlg)),
                ft.ElevatedButton("Guardar", on_click=save_equipment),
            ]
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def view_equipment_details(self, equipment_id: int):
        """Ver ficha técnica completa del equipo"""
        # TODO: Mostrar vista detallada
        self.show_snackbar(f"Ver ficha técnica {equipment_id}", ft.colors.BLUE)
    
    def view_assemblies(self, equipment_id: int):
        """Ver conjuntos del equipo"""
        # TODO: Mostrar lista de conjuntos y componentes
        self.show_snackbar(f"Ver conjuntos del equipo {equipment_id}", ft.colors.BLUE)
    
    def edit_equipment(self, equipment_id: int):
        """Editar equipo"""
        # TODO: Implementar edición
        pass
    
    def delete_equipment(self, equipment_id: int):
        """Eliminar equipo"""
        # TODO: Confirmación y eliminación
        pass
    
    def search_equipment(self, query: str):
        """Buscar equipos"""
        # TODO: Implementar búsqueda
        pass
    
    def filter_equipment(self):
        """Filtrar equipos"""
        # TODO: Implementar filtros
        pass
    
    def load_plants(self, client_id: str):
        """Cargar plantas del cliente"""
        # TODO: Cargar desde BD
        pass
    
    def load_locations(self, plant_id: str):
        """Cargar ubicaciones técnicas"""
        # TODO: Cargar desde BD
        pass
    
    def close_dialog(self, dialog):
        """Cerrar diálogo"""
        dialog.open = False
        self.page.update()
    
    def show_snackbar(self, message: str, color):
        """Mostrar snackbar"""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()