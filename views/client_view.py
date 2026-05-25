"""
Vista de Clientes
"""
import flet as ft


class ClientView:
    """Vista de gestión de clientes"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.clients = []  # TODO: Cargar desde BD
        
    def build(self) -> ft.Container:
        """Construir vista de clientes"""
        
        # Barra de herramientas
        toolbar = ft.Row(
            [
                ft.TextField(
                    hint_text="Buscar cliente...",
                    prefix_icon=ft.icons.SEARCH,
                    width=300,
                    on_change=lambda e: self.search_clients(e.control.value)
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Nuevo Cliente",
                    icon=ft.icons.ADD,
                    on_click=lambda e: self.show_add_client_dialog()
                )
            ]
        )
        
        # Tabla de clientes
        clients_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("RUC")),
                ft.DataColumn(ft.Text("Ciudad")),
                ft.DataColumn(ft.Text("Contacto")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Plantas")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[
                # TODO: Cargar datos reales
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("CLI001")),
                        ft.DataCell(ft.Text("Empresa Industrial S.A.")),
                        ft.DataCell(ft.Text("0992345678001")),
                        ft.DataCell(ft.Text("Guayaquil")),
                        ft.DataCell(ft.Text("Juan Pérez")),
                        ft.DataCell(ft.Text("04-2345678")),
                        ft.DataCell(ft.Text("3")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar",
                                    icon_size=20,
                                    on_click=lambda e: self.edit_client(1)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_size=20,
                                    icon_color=ft.colors.RED,
                                    on_click=lambda e: self.delete_client(1)
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
                    "Gestión de Clientes",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(height=20),
                toolbar,
                ft.Container(height=20),
                ft.Container(
                    content=clients_table,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=5,
                    padding=10
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
    
    def show_add_client_dialog(self):
        """Mostrar diálogo para agregar cliente"""
        
        code_field = ft.TextField(label="Código", width=200)
        name_field = ft.TextField(label="Nombre", width=400)
        ruc_field = ft.TextField(label="RUC", width=200)
        city_field = ft.TextField(label="Ciudad", width=200)
        phone_field = ft.TextField(label="Teléfono", width=200)
        email_field = ft.TextField(label="Email", width=300)
        contact_field = ft.TextField(label="Persona de Contacto", width=300)
        
        def save_client(e):
            # TODO: Implementar guardado en BD
            dlg.open = False
            self.page.update()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Cliente creado exitosamente")
            )
            self.page.snack_bar.open = True
            self.page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("Nuevo Cliente"),
            content=ft.Column([
                ft.Row([code_field, ruc_field]),
                name_field,
                ft.Row([city_field, phone_field]),
                ft.Row([email_field, contact_field]),
            ], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(dlg)),
                ft.ElevatedButton("Guardar", on_click=save_client),
            ]
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def edit_client(self, client_id: int):
        """Editar cliente"""
        # TODO: Implementar edición
        pass
    
    def delete_client(self, client_id: int):
        """Eliminar cliente"""
        # TODO: Implementar eliminación con confirmación
        pass
    
    def search_clients(self, query: str):
        """Buscar clientes"""
        # TODO: Implementar búsqueda
        pass
    
    def close_dialog(self, dialog):
        """Cerrar diálogo"""
        dialog.open = False
        self.page.update()