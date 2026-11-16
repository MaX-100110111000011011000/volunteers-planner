import flet as ft
import datetime
from theme import AppTheme


class EventDialog(ft.AlertDialog):
    def __init__(self, event_data=None, default_date="", on_save=None, on_delete=None):
        super().__init__()
        self.event_data = event_data
        self.on_save = on_save
        self.on_delete = on_delete
        self.is_edit = event_data is not None

        self.modal = True
        self.bgcolor = AppTheme.BG_SURFACE
        self.shape = ft.RoundedRectangleBorder(radius=AppTheme.RADIUS_LARGE)

        self.title = ft.Text(
            "Редактировать мероприятие" if self.is_edit else "Создать мероприятие",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=AppTheme.TEXT_MAIN,
        )

        self.title_field = ft.TextField(
            label="Название мероприятия",
            value=event_data.get("title", "") if self.is_edit else "",
            text_size=14,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
        )

        self.date_field = ft.TextField(
            label="Дата (ДД.ММ.ГГГГ)",
            value=event_data.get("date", "") if self.is_edit else default_date,
            text_size=14,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
        )

        self.start_hour_field = ft.TextField(
            label="Начало (ЧЧ)",
            value=str(event_data.get("start_hour", "")) if self.is_edit else "",
            text_size=14,
            expand=True,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.end_hour_field = ft.TextField(
            label="Окончание (ЧЧ)",
            value=str(event_data.get("end_hour", "")) if self.is_edit else "",
            text_size=14,
            expand=True,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.needed_count_field = ft.TextField(
            label="Количество волонтёров",
            value=str(event_data.get("needed_count", "")) if self.is_edit else "",
            text_size=14,
            border_radius=AppTheme.RADIUS_MEDIUM,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.error_label = ft.Text(
            "",
            size=12,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.RED_700,
            visible=False,
        )

        self.content = ft.Column(
            tight=True,
            width=380,
            spacing=12,
            controls=[
                self.title_field,
                self.date_field,
                ft.Row(
                    spacing=12,
                    controls=[self.start_hour_field, self.end_hour_field],
                ),
                self.needed_count_field,
                self.error_label,
            ],
        )

        self.actions_alignment = ft.MainAxisAlignment.END
        self.actions = self._build_actions()

    def _build_actions(self):
        buttons = []

        if self.is_edit:
            buttons.append(
                ft.Container(
                    bgcolor=AppTheme.EVENT_PINK,
                    border=ft.Border.all(1, AppTheme.PRIMARY),
                    border_radius=AppTheme.RADIUS_MEDIUM,
                    padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                    on_click=self._handle_delete,
                    content=ft.Text(
                        "Удалить",
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=AppTheme.TEXT_MAIN,
                    ),
                )
            )

        buttons.extend([
            ft.Container(
                bgcolor=AppTheme.BG_WINDOW,
                border=ft.Border.all(1, AppTheme.PRIMARY),
                border_radius=AppTheme.RADIUS_MEDIUM,
                padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                on_click=self._close,
                content=ft.Text(
                    "Отмена",
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=AppTheme.TEXT_MAIN,
                ),
            ),
            ft.Container(
                bgcolor=AppTheme.PRIMARY,
                border_radius=AppTheme.RADIUS_MEDIUM,
                padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                on_click=self._handle_save,
                content=ft.Text(
                    "Сохранить",
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=AppTheme.TEXT_LIGHT,
                ),
            ),
        ])
        return buttons

    def _show_error(self, message):
        self.error_label.value = message
        self.error_label.visible = True
        self.update()

    def _close(self, e=None):
        if hasattr(self.page, "pop_dialog"):
            self.page.pop_dialog()
        else:
            self.page.close(self)

    def _handle_save(self, e):
        title = (self.title_field.value or "").strip()
        date_str = (self.date_field.value or "").strip()

        if not title:
            self._show_error("Введите название мероприятия")
            return

        try:
            datetime.datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            self._show_error("Укажите дату в формате ДД.ММ.ГГГГ")
            return

        try:
            start_hour = int((self.start_hour_field.value or "").strip())
            end_hour = int((self.end_hour_field.value or "").strip())
            needed_count = int((self.needed_count_field.value or "").strip())
        except ValueError:
            self._show_error("Часы и количество волонтёров должны быть числами")
            return

        if not (0 <= start_hour < end_hour <= 24):
            self._show_error("Часы от 0 до 24, окончание должно быть позже начала")
            return

        if needed_count < 0:
            self._show_error("Количество волонтёров не может быть отрицательным")
            return

        event_payload = {
            "title": title,
            "date": date_str,
            "start_hour": start_hour,
            "end_hour": end_hour,
            "needed_count": needed_count,
            "shifts": self.event_data.get("shifts", []) if self.is_edit else [],
        }

        if self.on_save:
            self.on_save(event_payload)

        self._close()

    def _handle_delete(self, e):
        if self.on_delete:
            self.on_delete()
        self._close()
