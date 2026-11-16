import flet as ft
from theme import AppTheme


class VolunteerDialog(ft.AlertDialog):
    def __init__(
        self,
        shift_data=None,
        default_start="09:00",
        default_end="13:00",
        on_save=None,
        on_delete=None,
    ):
        super().__init__()
        self.shift_data = shift_data
        self.on_save = on_save
        self.on_delete = on_delete
        self.is_edit = shift_data is not None

        self.modal = True
        self.bgcolor = AppTheme.BG_SURFACE
        self.shape = ft.RoundedRectangleBorder(radius=AppTheme.RADIUS_LARGE)

        self.title = ft.Text(
            "Редактировать смену" if self.is_edit else "Записать волонтёра",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=AppTheme.TEXT_MAIN,
        )

        self.name_field = ft.TextField(
            label="Имя и фамилия волонтёра",
            value=shift_data.get("name", "") if self.is_edit else "",
            text_size=14,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
        )

        self.group_field = ft.TextField(
            label="Академическая группа",
            value=shift_data.get("group", "") if self.is_edit else "",
            text_size=14,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
        )

        self.start_field = ft.TextField(
            label="Начало (ЧЧ:ММ)",
            value=shift_data.get("start", default_start) if self.is_edit else default_start,
            text_size=14,
            expand=True,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
        )

        self.end_field = ft.TextField(
            label="Окончание (ЧЧ:ММ)",
            value=shift_data.get("end", default_end) if self.is_edit else default_end,
            text_size=14,
            expand=True,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.PRIMARY,
            border_radius=AppTheme.RADIUS_MEDIUM,
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
            width=360,
            spacing=14,
            controls=[
                self.name_field,
                self.group_field,
                ft.Row(
                    spacing=12,
                    controls=[self.start_field, self.end_field],
                ),
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

    def _parse_time(self, raw_value):
        parts = raw_value.strip().split(":")
        if len(parts) != 2:
            return None
        try:
            hours = int(parts[0])
            minutes = int(parts[1])
        except ValueError:
            return None
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            return None
        return hours * 60 + minutes, f"{hours:02d}:{minutes:02d}"

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
        name = (self.name_field.value or "").strip()
        group = (self.group_field.value or "").strip()

        if not name:
            self._show_error("Введите имя и фамилию волонтёра")
            return

        if not group:
            self._show_error("Укажите академическую группу")
            return

        parsed_start = self._parse_time(self.start_field.value or "")
        parsed_end = self._parse_time(self.end_field.value or "")

        if not parsed_start or not parsed_end:
            self._show_error("Укажите время в формате ЧЧ:ММ (например, 09:30)")
            return

        start_min, start_str = parsed_start
        end_min, end_str = parsed_end

        if end_min <= start_min:
            self._show_error("Время окончания должно быть позже начала")
            return

        shift_payload = {
            "name": name,
            "group": group,
            "start": start_str,
            "end": end_str,
        }

        if self.on_save:
            self.on_save(shift_payload)

        self._close()

    def _handle_delete(self, e):
        if self.on_delete:
            self.on_delete()
        self._close()
