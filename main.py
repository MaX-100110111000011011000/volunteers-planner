import flet as ft

def main(page: ft.Page):
    # Настройки главного окна приложения
    page.title = "Планировщик волонтеров"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Размеры окна через современный объект window
    page.window.width = 500
    page.window.height = 600
    
    # Приветственный текст на старте
    welcome_text = ft.Text(
        "Каркас приложения запущен! 🚀", 
        size=18, 
        weight=ft.FontWeight.BOLD
    )
    
    page.add(
        ft.Column(
            [
                welcome_text,
                # Используем актуальный класс ft.Button вместо ElevatedButton
                ft.Button("Нажми меня", on_click=lambda e: print("Кнопка нажата!"))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# Запуск приложения
ft.run(main)
