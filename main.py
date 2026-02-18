from src.user_interaction import user_interaction

if __name__ == "__main__":
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
