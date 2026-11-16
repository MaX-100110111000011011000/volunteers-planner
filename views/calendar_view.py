import flet as ft
import calendar
import datetime
from theme import AppTheme

MONTHS = (
    "", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
)
WEEKDAYS = ("ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС")


class CalendarView(ft.Column):
    def __init__(self):
        super().__init__(expand=True, spacing=16)
        self.year = datetime.datetime.now().year
        self.month = datetime.datetime.now().month

        self.month_title = ft.Text(
            f"{MONTHS[self.month]} {self.year}",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=AppTheme.TEXT_MAIN,
        )
        self.days_grid = ft.Column(expand=True, spacing=6)

        self.controls = [
            self._build_header(),
            self._build_body(),
        ]
        self._render_days()

    def _build_header(self) -> ft.Container:
        now_btn = ft.Container(
            bgcolor=AppTheme.BG_WINDOW,
            border=ft.Border.all(1, AppTheme.PRIMARY),
            border_radius=AppTheme.RADIUS_MEDIUM,
            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            on_click=self._go_to_current_month,
            content=ft.Text("Текущий месяц", size=14, weight=ft.FontWeight.W_600, color=AppTheme.TEXT_MAIN),
            )

        return ft.Container(
            bgcolor=AppTheme.BG_SURFACE,
            border=ft.Border.all(AppTheme.BORDER_WIDTH, AppTheme.PRIMARY),
            border_radius=AppTheme.RADIUS_LARGE,
            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    now_btn,
                    ft.Text(
                        "Главная страница",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_MAIN,
                    ),
                    ft.Container(
                        bgcolor=AppTheme.SECONDARY,
                        border_radius=AppTheme.RADIUS_MEDIUM,
                        padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                        content=self.month_title,
                    ),
                ],
            ),
        )

    def _build_body(self) -> ft.Row:
        
        prev_btn = ft.Container(
            bgcolor=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
            padding=12,
            on_click=lambda e: self._change_month(-1),
            content=ft.Icon(ft.Icons.CHEVRON_LEFT, color=AppTheme.TEXT_LIGHT, size=28),
        )

        next_btn = ft.Container(
            bgcolor=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
            padding=12,
            on_click=lambda e: self._change_month(1),
            content=ft.Icon(ft.Icons.CHEVRON_RIGHT, color=AppTheme.TEXT_LIGHT, size=28),
        )

        calendar_box = ft.Container(
            expand=True,
            bgcolor=AppTheme.BG_SURFACE,
            border=ft.Border.all(AppTheme.BORDER_WIDTH, AppTheme.PRIMARY),
            border_radius=AppTheme.RADIUS_LARGE,
            padding=16,
            content=ft.Column(
                expand=True,
                spacing=8,
                controls=[
                    self._build_weekdays_header(),
                    self.days_grid,
                ],
            ),
        )

        return ft.Row(
            expand=True,
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[prev_btn, calendar_box, next_btn],
        )

    def _build_weekdays_header(self) -> ft.Container:
        return ft.Container(
            bgcolor=AppTheme.SECONDARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
            padding=ft.Padding.symmetric(vertical=10),
            content=ft.Row(
                spacing=6,
                controls=[
                    ft.Container(
                        expand=1,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text(
                            day_name,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_MAIN,
                        ),
                    )
                    for day_name in WEEKDAYS
                ],
            ),
        )

    def _render_days(self):
        self.days_grid.controls.clear()
        weeks = calendar.monthcalendar(self.year, self.month)

        for week in weeks:
            week_row = ft.Row(
                expand=1,
                spacing=6,
                controls=[self._build_day_cell(day) for day in week],
            )
            self.days_grid.controls.append(week_row)

    def _build_day_cell(self, day: int) -> ft.Container:
        now = datetime.datetime.now()
        is_today = (day == now.day and self.month == now.month and self.year == now.year)

        if day == 0:
            return ft.Container(
                expand=1,
                bgcolor=AppTheme.BG_SUBTLE,
                border_radius=AppTheme.RADIUS_SMALL,
            )

        cell_items = [
            ft.Text(
                str(day),
                size=14,
                weight=ft.FontWeight.BOLD,
                color=AppTheme.TEXT_MAIN,
            )
        ]

        # Временная заглушка для визуальной проверки розовых плашек мероприятий
        if day in {1, 4, 9, 28}:
            cell_items.append(
                ft.Container(
                    bgcolor=AppTheme.EVENT_PINK,
                    border=ft.Border.all(1, AppTheme.PRIMARY),
                    border_radius=AppTheme.RADIUS_SMALL,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                    content=ft.Text(
                        "Меропр.",
                        size=12,
                        weight=ft.FontWeight.W_600,
                        color=AppTheme.TEXT_MAIN,
                    ),
                )
            )

        return ft.Container(
            expand=1,
            bgcolor=ft.Colors.with_opacity(0.11, AppTheme.TODAY_HIGHLIGHT) if is_today else AppTheme.BG_SURFACE,
            border=ft.Border.all(1.5, AppTheme.TODAY_HIGHLIGHT) if is_today else ft.Border.all(1, AppTheme.BG_WINDOW),
            border_radius=AppTheme.RADIUS_SMALL,
            padding=8,
            content=ft.Column(spacing=4, controls=cell_items),
        )

    def _change_month(self, delta: int):
        self.month += delta
        if self.month == 0:
            self.month = 12
            self.year -= 1
        elif self.month == 13:
            self.month = 1
            self.year += 1

        self.month_title.value = f"{MONTHS[self.month]} {self.year}"
        self._render_days()
        self.update()

    def _go_to_current_month(self, e):
        now = datetime.datetime.now()
        self.year = now.year
        self.month = now.month
        self.month_title.value = f"{MONTHS[self.month]} {self.year}"
        self._render_days()
        self.update()

