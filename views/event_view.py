import flet as ft
from theme import AppTheme
from views.volunteer_dialog import VolunteerDialog
from views.event_dialog import EventDialog


class EventView(ft.Column):
    def __init__(self, event_data=None, on_back=None, on_change=None, on_delete_event=None):
        super().__init__(expand=True, spacing=16)
        self.event_data = event_data or {}
        self.event_data.setdefault("shifts", [])
        self.on_back = on_back
        self.on_change = on_change
        self.on_delete_event = on_delete_event

        # Границы таймлайна и шаг сетки (по умолчанию 60 минут = 1 час)
        self.start_hour = self.event_data.get("start_hour", 9)
        self.end_hour = self.event_data.get("end_hour", 21)
        self.step_minutes = 60
        self.is_editing_grid = False

        self._rebuild()

    def _rebuild(self):
        self.controls = [
            self._build_header(),
            self._build_body(),
        ]

    def _toggle_grid_editor(self, e):
        self.is_editing_grid = not self.is_editing_grid
        self._rebuild()
        self.update()

    def _apply_grid_step(self, e):
        raw_value = (self.step_input.value or "").strip()
        try:
            minutes = int(raw_value)
        except ValueError:
            return

        if minutes < 1 or minutes > 240:
            return

        self.step_minutes = minutes
        self.is_editing_grid = False
        self._rebuild()
        self.update()

    def _add_shift(self, shift_data):
        self.event_data["shifts"].append(shift_data)
        if self.on_change:
            self.on_change()
        self._rebuild()
        self.update()

    def _update_shift(self, index, shift_data):
        self.event_data["shifts"][index] = shift_data
        if self.on_change:
            self.on_change()
        self._rebuild()
        self.update()

    def _delete_shift(self, index):
        self.event_data["shifts"].pop(index)
        if self.on_change:
            self.on_change()
        self._rebuild()
        self.update()

    def _update_event(self, updated_data):
        self.event_data.update(updated_data)
        self.start_hour = self.event_data.get("start_hour", 9)
        self.end_hour = self.event_data.get("end_hour", 21)
        if self.on_change:
            self.on_change()
        self._rebuild()
        self.update()

    def _open_edit_event_dialog(self, e=None):
        dialog = EventDialog(
            event_data=self.event_data,
            on_save=self._update_event,
            on_delete=self.on_delete_event,
        )
        if hasattr(self.page, "show_dialog"):
            self.page.show_dialog(dialog)
        else:
            self.page.open(dialog)

    def _open_volunteer_dialog(self, e=None, shift_index=None):
        is_edit = shift_index is not None
        shift_data = self.event_data["shifts"][shift_index] if is_edit else None

        default_start = f"{self.start_hour:02d}:00"
        default_end = f"{min(self.start_hour + 4, self.end_hour):02d}:00"

        dialog = VolunteerDialog(
            shift_data=shift_data,
            default_start=default_start,
            default_end=default_end,
            on_save=(
                (lambda data: self._update_shift(shift_index, data))
                if is_edit
                else self._add_shift
            ),
            on_delete=(lambda: self._delete_shift(shift_index)) if is_edit else None,
        )

        if hasattr(self.page, "show_dialog"):
            self.page.show_dialog(dialog)
        else:
            self.page.open(dialog)

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
                                bgcolor=ft.Colors.with_opacity(0.5, AppTheme.SECONDARY),
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
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.Text(
                                self.event_data.get("title", "Название не указано"),
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_MAIN,
                            ),
                            ft.Container(
                                bgcolor=AppTheme.BG_WINDOW,
                                border=ft.Border.all(1, AppTheme.PRIMARY),
                                border_radius=AppTheme.RADIUS_MEDIUM,
                                padding=8,
                                on_click=self._open_edit_event_dialog,
                                content=ft.Icon(
                                    ft.Icons.EDIT,
                                    size=18,
                                    color=AppTheme.TEXT_MAIN,
                                ),
                            ),
                        ],
                    ),
                    ft.Container(
                        bgcolor=AppTheme.PRIMARY,
                        border_radius=AppTheme.RADIUS_MEDIUM,
                        padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                        on_click=lambda e: self._open_volunteer_dialog(),
                        content=ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.ADD, color=AppTheme.TEXT_LIGHT, size=20),
                                ft.Text(
                                    "Записать волонтёра",
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

    def _build_body(self):
        return ft.Container(
            expand=True,
            bgcolor=AppTheme.BG_SURFACE,
            border=ft.Border.all(AppTheme.BORDER_WIDTH, AppTheme.PRIMARY),
            border_radius=AppTheme.RADIUS_LARGE,
            padding=20,
            content=ft.Row(
                expand=True,
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    self._build_timeline(),
                    ft.Column(
                        width=180,
                        spacing=10,
                        controls=[
                            self._build_stats(),
                            self._build_grid_controls(),
                        ],
                    ),
                ],
            ),
        )

    def _build_stats(self):
        needed = self.event_data.get("needed_count", 0)
        shifts = self.event_data.get("shifts", [])
        found = len(shifts)
        remaining = needed - found

        card_bgcolor = AppTheme.EVENT_PINK if remaining > 0 else AppTheme.BG_WINDOW
        status_text = f"Нужно найти: {remaining}" if remaining > 0 else "Все волонтёры записаны"

        return ft.Container(
            bgcolor=card_bgcolor,
            border=ft.Border.all(1.5, AppTheme.PRIMARY),
            border_radius=AppTheme.RADIUS_MEDIUM,
            padding=12,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(
                        f"Всего нужно: {needed}",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_MAIN,
                    ),
                    ft.Container(height=1, bgcolor=AppTheme.PRIMARY),
                    ft.Text(
                        status_text,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_MAIN,
                    ),
                ],
            ),
        )

    def _build_grid_controls(self):
        items = [
            ft.Container(
                bgcolor=AppTheme.BG_WINDOW,
                border=ft.Border.all(1, AppTheme.PRIMARY),
                border_radius=AppTheme.RADIUS_MEDIUM,
                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                on_click=self._toggle_grid_editor,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            f"Сетка: {self.step_minutes} мин",
                            size=12,
                            weight=ft.FontWeight.W_600,
                            color=AppTheme.TEXT_MAIN,
                        ),
                        ft.Icon(ft.Icons.TUNE, size=16, color=AppTheme.PRIMARY),
                    ],
                ),
            )
        ]

        if self.is_editing_grid:
            self.step_input = ft.TextField(
                value=str(self.step_minutes),
                label="Шаг (мин)",
                text_size=13,
                border_color=AppTheme.PRIMARY,
                focused_border_color=AppTheme.PRIMARY,
                border_radius=AppTheme.RADIUS_MEDIUM,
                keyboard_type=ft.KeyboardType.NUMBER,
                on_submit=self._apply_grid_step,
            )
            items.append(
                ft.Container(
                    bgcolor=AppTheme.BG_WINDOW,
                    border=ft.Border.all(1, AppTheme.PRIMARY),
                    border_radius=AppTheme.RADIUS_MEDIUM,
                    padding=10,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            self.step_input,
                            ft.Container(
                                bgcolor=AppTheme.PRIMARY,
                                border_radius=AppTheme.RADIUS_MEDIUM,
                                padding=ft.Padding.symmetric(vertical=7),
                                alignment=ft.Alignment.CENTER,
                                on_click=self._apply_grid_step,
                                content=ft.Text(
                                    "Применить",
                                    size=12,
                                    weight=ft.FontWeight.W_600,
                                    color=AppTheme.TEXT_LIGHT,
                                ),
                            ),
                        ],
                    ),
                )
            )

        return ft.Column(spacing=8, controls=items)

    def _time_to_minutes(self, time_str):
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

    def _build_shift_column(self, shift, index, px_per_min):
        day_start = self.start_hour * 60
        day_end = self.end_hour * 60

        start_min = max(day_start, self._time_to_minutes(shift["start"]))
        end_min = min(day_end, self._time_to_minutes(shift["end"]))
        duration = max(15, end_min - start_min)

        top_offset = (start_min - day_start) * px_per_min
        card_height = duration * px_per_min

        card_color = (
            ft.Colors.with_opacity(0.5, AppTheme.SECONDARY)
            if index % 2 == 0
            else AppTheme.BG_WINDOW
        )
        group = shift.get("group", "").strip()

        time_badge = ft.Container(
            bgcolor=AppTheme.BG_SURFACE,
            border_radius=AppTheme.RADIUS_SMALL,
            padding=ft.Padding.symmetric(horizontal=8, vertical=4),
            content=ft.Text(
                f"{shift['start']} - {shift['end']}",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=AppTheme.TEXT_MAIN,
            ),
        )

        if card_height < 80:
            title_label = f"{shift['name']} ({group})" if group else shift["name"]
            card_content = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        title_label,
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_MAIN,
                        expand=True,
                    ),
                    time_badge,
                ],
            )
        else:
            column_items = [
                ft.Text(
                    shift["name"],
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=AppTheme.TEXT_MAIN,
                ),
            ]
            if group:
                column_items.append(
                    ft.Text(
                        group,
                        size=12,
                        weight=ft.FontWeight.W_500,
                        color=AppTheme.TEXT_MUTED,
                    )
                )
            column_items.append(time_badge)

            card_content = ft.Column(
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=column_items,
            )

        card = ft.Container(
            width=165,
            height=card_height,
            bgcolor=card_color,
            border=ft.Border.all(1, AppTheme.PRIMARY),
            border_radius=AppTheme.RADIUS_MEDIUM,
            padding=12 if card_height >= 80 else 6,
            content=card_content,
        )

        interactive_card = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=lambda e, idx=index: self._open_volunteer_dialog(shift_index=idx),
            on_secondary_tap=lambda e, idx=index: self._open_volunteer_dialog(shift_index=idx),
            content=card,
        )

        return ft.Column(
            width=165,
            spacing=0,
            controls=[
                ft.Container(height=top_offset),
                interactive_card,
            ],
        )

    def _build_timeline(self):
        total_minutes = (self.end_hour - self.start_hour) * 60
        step_height = 60 if self.step_minutes >= 60 else 40
        offsets = list(range(0, total_minutes, self.step_minutes))
        total_height = len(offsets) * step_height

        time_labels = []
        grid_lines = []

        for offset in offsets:
            current_min = self.start_hour * 60 + offset
            hour = current_min // 60
            minute = current_min % 60
            is_whole_hour = minute == 0

            time_labels.append(
                ft.Container(
                    height=step_height,
                    alignment=ft.Alignment.TOP_LEFT,
                    content=ft.Text(
                        f"{hour:02d}:{minute:02d}",
                        size=13 if is_whole_hour else 12,
                        weight=ft.FontWeight.BOLD if is_whole_hour else ft.FontWeight.NORMAL,
                        color=AppTheme.TEXT_MAIN if is_whole_hour else AppTheme.TEXT_MUTED,
                    ),
                )
            )

            grid_lines.append(
                ft.Container(
                    height=step_height,
                    alignment=ft.Alignment.TOP_LEFT,
                    content=ft.Container(
                        height=1,
                        bgcolor=ft.Colors.with_opacity(
                            0.35 if is_whole_hour else 0.14, AppTheme.PRIMARY
                        ),
                    ),
                )
            )

        time_labels.append(
            ft.Container(
                height=20,
                alignment=ft.Alignment.TOP_LEFT,
                content=ft.Text(
                    f"{self.end_hour:02d}:00",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=AppTheme.TEXT_MAIN,
                ),
            )
        )
        grid_lines.append(ft.Container(height=1.5, bgcolor=AppTheme.PRIMARY))

        px_per_min = step_height / self.step_minutes
        shifts = self.event_data.get("shifts", [])

        shifts_controls = (
            [
                self._build_shift_column(shift, i, px_per_min)
                for i, shift in enumerate(shifts)
            ]
            if shifts
            else [
                ft.Container(
                    padding=ft.Padding.only(top=24),
                    content=ft.Text(
                        "Пока нет записанных волонтёров",
                        size=14,
                        color=AppTheme.TEXT_MUTED,
                    ),
                )
            ]
        )

        shifts_row = ft.Row(
            scroll=ft.ScrollMode.AUTO,
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=shifts_controls,
        )

        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(width=55, spacing=0, controls=time_labels),
                        ft.Container(
                            padding=ft.Padding.only(top=8),
                            content=ft.Container(
                                width=1.5,
                                height=total_height,
                                bgcolor=AppTheme.PRIMARY,
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            padding=ft.Padding.only(top=8),
                            content=ft.Stack(
                                height=total_height + 2,
                                controls=[
                                    ft.Column(spacing=0, controls=grid_lines),
                                    ft.Container(
                                        padding=ft.Padding.only(left=16),
                                        content=shifts_row,
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            ],
        )