import flet as ft
from theme import AppTheme
from views.calendar_view import CalendarView
from views.event_view import EventView
from data.storage import load_events, save_events


async def main(page: ft.Page):
    page.title = "Планировщик волонтеров"
    page.padding = 24
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = AppTheme.BG_WINDOW
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.window.width = 1200
    page.window.height = 780
    page.window.min_width = 1000
    page.window.min_height = 680
    page.update()
    await page.window.center()

    # Загружаем локальные события (если файла нет — вернётся пустой список [])
    events = load_events()

    def persist():
        save_events(events)

    def show_event(event_data):
        page.controls.clear()
        page.add(
            EventView(
                event_data=event_data,
                on_back=show_calendar,
                on_change=persist,
            )
        )
        page.update()

    def show_calendar():
        page.controls.clear()
        page.add(
            CalendarView(
                events=events,
                on_open_event=show_event,
                on_change=persist,
            )
        )
        page.update()

    show_calendar()


ft.run(main)
