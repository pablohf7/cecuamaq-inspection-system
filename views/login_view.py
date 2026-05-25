"""
Vista de Login
"""
import flet as ft
from typing import Callable


class LoginView:
    """Vista de autenticación"""
    
    def __init__(self, page: ft.Page, on_login_success: Callable):
        self.page = page
        self.on_login_success = on_login_success
        
    def build(self) -> ft.Container:
        """Construir vista de login"""
        
        # Campos de formulario
        self.username_field = ft.TextField(
            label="Usuario",
            prefix_icon=ft.icons.PERSON,
            width=300,
            autofocus=True
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=300,
            on_submit=lambda e: self.handle_login()
        )
        
        self.error_text = ft.Text(
            value="",
            color=ft.colors.RED,
            size=12,
            visible=False
        )
        
        login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            width=300,
            on_click=lambda e: self.handle_login(),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE
            )
        )
        
        # Layout de login
        login_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=50),
                    ft.Icon(
                        ft.icons.FACTORY,
                        size=80,
                        color=ft.colors.BLUE
                    ),
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
                    self.username_field,
                    self.password_field,
                    self.error_text,
                    ft.Container(height=10),
                    login_button,
                    ft.Container(height=20),
                    ft.TextButton(
                        "¿Olvidaste tu contraseña?",
                        on_click=lambda e: self.show_forgot_password()
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.BLUE_50, ft.colors.BLUE_100]
            )
        )
        
        return login_container
    
    def handle_login(self):
        """Manejar proceso de login"""
        username = self.username_field.value
        password = self.password_field.value
        
        # Validar campos
        if not username or not password:
            self.show_error("Por favor ingrese usuario y contraseña")
            return
        
        # TODO: Implementar autenticación con AuthService
        # Por ahora, login simple
        if username == "admin" and password == "Admin123!":
            self.on_login_success(username)
        else:
            self.show_error("Usuario o contraseña incorrectos")
    
    def show_error(self, message: str):
        """Mostrar mensaje de error"""
        self.error_text.value = message
        self.error_text.visible = True
        self.page.update()
    
    def show_forgot_password(self):
        """Mostrar diálogo de recuperación de contraseña"""
        # TODO: Implementar recuperación de contraseña
        dlg = ft.AlertDialog(
            title=ft.Text("Recuperar Contraseña"),
            content=ft.Text("Contacte al administrador del sistema para restablecer su contraseña."),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.close_dialog(dlg))
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def close_dialog(self, dialog):
        """Cerrar diálogo"""
        dialog.open = False
        self.page.update()