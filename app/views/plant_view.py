"""
Vista de Plantas
"""
import flet as ft


class PlantView:
    """Vista de gestión de plantas"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.plants = []
        self.clients = []  # TODO: Cargar desde BD
        
    def build(self) -> ft.Container:
        """Construir vista de plantas"""
        
        # Barra de herramientas
        toolbar = ft.Row(
            [
                ft.TextField(
                    hint_text="Buscar planta...",
                    prefix_icon=ft.icons.SEARCH,
                    width=300,
                    on_change=lambda e: self.search_plants(e.control.value)
                ),
                ft.Dropdown(
                    label="Filtrar por Cliente",
                    width=250,
                    options=[
                        ft.dropdown.Option("Todos"),
                        # TODO: Cargar clientes desde BD
                        ft.dropdown.Option("Empresa Industrial S.A."),
                    ],
                    on_change=lambda e: self.filter_by_client(e.control.value)
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Nueva Planta",
                    icon=ft.icons.ADD,
                    on_click=lambda e: self.show_add_plant_dialog()
                )
            ]
        )
        
        # Tabla de plantas
        plants_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Ciudad")),
                ft.DataColumn(ft.Text("Responsable")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Ubicaciones")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("PLT001")),
                        ft.DataCell(ft.Text("Planta Norte")),
                        ft.DataCell(ft.Text("Empresa Industrial S.A.")),
                        ft.DataCell(ft.Text("Guayaquil")),
                        ft.DataCell(ft.Text("María González")),
                        ft.DataCell(ft.Text("04-2345679")),
                        ft.DataCell(ft.Text("5")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text("Activa", color=ft.colors.WHITE, size=12),
                                bgcolor=ft.colors.GREEN,
                                padding=5,
                                border_radius=5
                            )
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.VISIBILITY,
                                    tooltip="Ver Detalles",
                                    icon_size=20,
                                    on_click=lambda e: self.view_plant_details(1)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar",
                                    icon_size=20,
                                    on_click=lambda e: self.edit_plant(1)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_size=20,
                                    icon_color=ft.colors.RED,
                                    on_click=lambda e: self.delete_plant(1)
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
                ft.Text(
                    "Gestión de Plantas",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Divider(),
                ft.Container(height=10),
                toolbar,
                ft.Container(height=20),
                ft.Container(
                    content=plants_table,
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
    
    def show_add_plant_dialog(self):
        """Mostrar diálogo para agregar planta"""
        
        client_dropdown = ft.Dropdown(
            label="Cliente *",
            width=400,
            options=[
                # TODO: Cargar desde BD
                ft.dropdown.Option("1", "Empresa Industrial S.A."),
            ]
        )
        
        code_field = ft.TextField(
            label="Código *",
            width=150,
            hint_text="PLT001"
        )
        
        name_field = ft.TextField(
            label="Nombre *",
            width=400,
            hint_text="Planta Norte"
        )
        
        address_field = ft.TextField(
            label="Dirección",
            width=400,
            multiline=True,
            min_lines=2,
            max_lines=3
        )
        
        city_field = ft.TextField(
            label="Ciudad",
            width=200
        )
        
        manager_field = ft.TextField(
            label="Responsable",
            width=250
        )
        
        phone_field = ft.TextField(
            label="Teléfono",
            width=150
        )
        
        latitude_field = ft.TextField(
            label="Latitud",
            width=150,
            hint_text="-2.1234567"
        )
        
        longitude_field = ft.TextField(
            label="Longitud",
            width=150,
            hint_text="-79.1234567"
        )
        
        notes_field = ft.TextField(
            label="Notas",
            width=400,
            multiline=True,
            min_lines=3,
            max_lines=5
        )
        
        def save_plant(e):
            # Validar campos requeridos
            if not client_dropdown.value:
                self.show_snackbar("Debe seleccionar un cliente", ft.colors.RED)
                return
            
            if not code_field.value or not name_field.value:
                self.show_snackbar("Código y Nombre son obligatorios", ft.colors.RED)
                return
            
            # TODO: Implementar guardado en BD con PlantService
            dlg.open = False
            self.page.update()
            self.show_snackbar("Planta creada exitosamente", ft.colors.GREEN)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Nueva Planta"),
            content=ft.Container(
                content=ft.Column([
                    client_dropdown,
                    ft.Row([code_field, city_field]),
                    name_field,
                    address_field,
                    ft.Row([manager_field, phone_field]),
                    ft.Text("Ubicación GPS (Opcional):", weight=ft.FontWeight.BOLD),
                    ft.Row([latitude_field, longitude_field]),
                    notes_field,
                ], tight=True, spacing=15, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=500
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(dlg)),
                ft.ElevatedButton("Guardar", on_click=save_plant),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def view_plant_details(self, plant_id: int):
        """Ver detalles de planta"""
        # TODO: Mostrar vista detallada con ubicaciones técnicas
        self.show_snackbar(f"Ver detalles de planta {plant_id}", ft.colors.BLUE)
    
    def edit_plant(self, plant_id: int):
        """Editar planta"""
        # TODO: Implementar edición
        self.show_snackbar(f"Editar planta {plant_id}", ft.colors.ORANGE)
    
    def delete_plant(self, plant_id: int):
        """Eliminar planta con confirmación"""
        def confirm_delete(e):
            # TODO: Implementar eliminación en BD
            confirm_dlg.open = False
            self.page.update()
            self.show_snackbar("Planta eliminada exitosamente", ft.colors.GREEN)
        
        confirm_dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Está seguro que desea eliminar esta planta?\n\nEsta acción eliminará también todas las ubicaciones técnicas, equipos y componentes asociados."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(confirm_dlg)),
                ft.ElevatedButton(
                    "Eliminar",
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                    on_click=confirm_delete
                ),
            ]
        )
        
        self.page.dialog = confirm_dlg
        confirm_dlg.open = True
        self.page.update()
    
    def search_plants(self, query: str):
        """Buscar plantas"""
        # TODO: Implementar búsqueda
        pass
    
    def filter_by_client(self, client_name: str):
        """Filtrar plantas por cliente"""
        # TODO: Implementar filtro
        pass
    
    def close_dialog(self, dialog):
        """Cerrar diálogo"""
        dialog.open = False
        self.page.update()
    
    def show_snackbar(self, message: str, color):
        """Mostrar mensaje snackbar"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()