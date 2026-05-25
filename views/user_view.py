"""
Vista de Usuarios
"""
import flet as ft


class UserView:
    """Vista de gestión de usuarios"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self) -> ft.Container:
        """Construir vista de usuarios"""
        
        # Barra de herramientas
        toolbar = ft.Row(
            [
                ft.TextField(
                    hint_text="Buscar usuario...",
                    prefix_icon=ft.icons.SEARCH,
                    width=300,
                    on_change=lambda e: self.search_users(e.control.value)
                ),
                ft.Dropdown(
                    label="Filtrar por Rol",
                    width=200,
                    options=[
                        ft.dropdown.Option("todos", "Todos"),
                        ft.dropdown.Option("admin", "Administrador"),
                        ft.dropdown.Option("supervisor", "Supervisor"),
                        ft.dropdown.Option("inspector", "Inspector"),
                        ft.dropdown.Option("consulta", "Consulta"),
                    ],
                    on_change=lambda e: self.filter_by_role(e.control.value)
                ),
                ft.Dropdown(
                    label="Estado",
                    width=150,
                    options=[
                        ft.dropdown.Option("todos", "Todos"),
                        ft.dropdown.Option("active", "Activo"),
                        ft.dropdown.Option("inactive", "Inactivo"),
                        ft.dropdown.Option("suspended", "Suspendido"),
                    ],
                    on_change=lambda e: self.filter_by_status(e.control.value)
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Nuevo Usuario",
                    icon=ft.icons.PERSON_ADD,
                    on_click=lambda e: self.show_add_user_dialog()
                )
            ]
        )
        
        # Tabla de usuarios
        users_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Nombre Completo")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Rol")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Último Login")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("admin", weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text("Administrador Sistema")),
                        ft.DataCell(ft.Text("admin@cecuamaq.com")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text("Administrador", color=ft.colors.WHITE, size=12),
                                bgcolor=ft.colors.PURPLE,
                                padding=5,
                                border_radius=5
                            )
                        ),
                        ft.DataCell(ft.Text("-")),
                        ft.DataCell(ft.Text("25/05/2024 14:30")),
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
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar",
                                    icon_size=20,
                                    on_click=lambda e: self.edit_user(1)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.LOCK_RESET,
                                    tooltip="Restablecer Contraseña",
                                    icon_size=20,
                                    on_click=lambda e: self.reset_password(1)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.BLOCK,
                                    tooltip="Suspender",
                                    icon_size=20,
                                    icon_color=ft.colors.ORANGE,
                                    on_click=lambda e: self.suspend_user(1)
                                ),
                            ], spacing=0)
                        ),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("jperez")),
                        ft.DataCell(ft.Text("Juan Pérez")),
                        ft.DataCell(ft.Text("jperez@cecuamaq.com")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text("Inspector", color=ft.colors.WHITE, size=12),
                                bgcolor=ft.colors.BLUE,
                                padding=5,
                                border_radius=5
                            )
                        ),
                        ft.DataCell(ft.Text("0987654321")),
                        ft.DataCell(ft.Text("24/05/2024 09:15")),
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
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar",
                                    icon_size=20,
                                    on_click=lambda e: self.edit_user(2)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.LOCK_RESET,
                                    tooltip="Restablecer Contraseña",
                                    icon_size=20,
                                    on_click=lambda e: self.reset_password(2)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_size=20,
                                    icon_color=ft.colors.RED,
                                    on_click=lambda e: self.delete_user(2)
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
                    ft.Icon(ft.icons.PEOPLE, size=30, color=ft.colors.BLUE),
                    ft.Text(
                        "Gestión de Usuarios",
                        size=24,
                        weight=ft.FontWeight.BOLD
                    ),
                ]),
                ft.Divider(),
                ft.Container(height=10),
                toolbar,
                ft.Container(height=20),
                ft.Container(
                    content=users_table,
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