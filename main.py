import flet as ft
from theme import AppTheme
from views.calendar_view import CalendarView
from views.event_view import EventView


async def main(page: ft.Page):
    # Базовые настройки окна и палитры
    page.title = "Планировщик волонтеров"
    page.padding = 24
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = AppTheme.BG_WINDOW
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Размеры окна под ноутбук и выравнивание по центру монитора
    page.window.width = 1200
    page.window.height = 780
    page.window.min_width = 1000
    page.window.min_height = 680
    page.update()
    await page.window.center()

    page.add(EventView())


ft.run(main)
