import flet as ft
from theme import AppTheme


class EventView(ft.Column):
    def __init__(self, event_data=None, on_back=None):
        super().__init__(expand=True, spacing=16)
        self.event_data = event_data or {}
        self.on_back = on_back
        self.controls = [self._build_header()]

    def _build_header(self):
        return ft.Container(
            bgcolor=AppTheme.BG_SURFACE,
            border=ft.Border.all(AppTheme.BORDER_WIDTH, AppTheme.PRIMARY),
            border_radius=AppTheme.RADIUS_LARGE,
            padding=20,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        spacing=12,
                        controls=[
                            ft.Container(
                                bgcolor=AppTheme.BG_WINDOW,
                                border=ft.Border.all(1, AppTheme.PRIMARY),
                                border_radius=AppTheme.RADIUS_MEDIUM,
                                padding=10,
                                content=ft.Icon(ft.Icons.ARROW_BACK, color=AppTheme.TEXT_MAIN, size=20),
                                on_click=lambda e: self.on_back() if self.on_back else None,
                            ),
                            ft.Container(
                                bgcolor=AppTheme.SECONDARY,
                                border_radius=AppTheme.RADIUS_MEDIUM,
                                padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                                content=ft.Text(
                                    self.event_data.get("date", "Дата не указана"),
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=AppTheme.TEXT_MAIN,
                                ),
                            ),
                        ],
                    ),
                    
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text(
                            self.event_data.get("title", "Название не указано"),
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_MAIN,),
                            ),

                    ft.Container(
                        bgcolor=AppTheme.PRIMARY,
                        border_radius=AppTheme.RADIUS_MEDIUM,
                        padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                        content=ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.ADD, color=AppTheme.TEXT_LIGHT, size=20),
                                ft.Text(
                                    "Запись волонтера",
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    color=AppTheme.TEXT_LIGHT,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )
