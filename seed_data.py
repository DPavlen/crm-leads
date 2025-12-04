import random

from src.database import SessionLocal, init_db
from src.models import Appeal, Lead, Operator, OperatorSourceWeight, Source


def clear_database(db):
    """Clear all data from database."""
    db.query(Appeal).delete()
    db.query(OperatorSourceWeight).delete()
    db.query(Lead).delete()
    db.query(Source).delete()
    db.query(Operator).delete()
    db.commit()


def create_operators(db):
    """Create operators."""
    print("\nCreating operators...")
    operators_data = [
        {"name": "Колесник Петр", "is_active": True, "max_load": 10},
        {"name": "Василий Никипоренков", "is_active": True, "max_load": 15},
        {"name": "Игнатьева Анна", "is_active": True, "max_load": 8},
    ]

    operators = []
    for op_data in operators_data:
        operator = Operator(**op_data)
        db.add(operator)
        operators.append(operator)

    db.commit()
    for op in operators:
        db.refresh(op)
        print(f"  - {op.name} (ID: {op.id}, max_load: {op.max_load})")

    return operators


def create_sources(db):
    """Create sources (bots/channels)."""
    print("\nCreating sources...")
    sources_data = [
        {"name": "Telegram Bot", "description": "Основной Telegram бот для поддержки"},
        {"name": "WhatsApp Bot", "description": "WhatsApp канал"},
        {"name": "Viber Bot", "description": "Viber канал связи"},
        {"name": "Web Chat", "description": "Виджет чата на сайте"},
        {"name": "Instagram Direct", "description": "Сообщения из Instagram"},
    ]

    sources = []
    for src_data in sources_data:
        source = Source(**src_data)
        db.add(source)
        sources.append(source)

    db.commit()
    for src in sources:
        db.refresh(src)
        print(f"  - {src.name} (ID: {src.id})")

    return sources


def create_weights(db, operators, sources):
    """Configure operator weights for sources."""
    print("\nConfiguring operator weights...")

    # Telegram Bot - все операторы
    weights_telegram = [
        {"operator_id": operators[0].id, "source_id": sources[0].id, "weight": 20},
        {"operator_id": operators[1].id, "source_id": sources[0].id, "weight": 50},
        {"operator_id": operators[2].id, "source_id": sources[0].id, "weight": 30},
    ]

    # WhatsApp Bot - только Василий и Анна
    weights_whatsapp = [
        {"operator_id": operators[1].id, "source_id": sources[1].id, "weight": 60},
        {"operator_id": operators[2].id, "source_id": sources[1].id, "weight": 40},
    ]

    # Viber Bot - только Петр и Анна
    weights_viber = [
        {"operator_id": operators[0].id, "source_id": sources[2].id, "weight": 50},
        {"operator_id": operators[2].id, "source_id": sources[2].id, "weight": 50},
    ]

    # Web Chat - все операторы равномерно
    weights_web = [
        {"operator_id": operators[0].id, "source_id": sources[3].id, "weight": 33},
        {"operator_id": operators[1].id, "source_id": sources[3].id, "weight": 34},
        {"operator_id": operators[2].id, "source_id": sources[3].id, "weight": 33},
    ]

    # Instagram - только Анна (специалист по соцсетям)
    weights_instagram = [
        {"operator_id": operators[2].id, "source_id": sources[4].id, "weight": 100},
    ]

    all_weights = (
        weights_telegram + weights_whatsapp + weights_viber + weights_web + weights_instagram
    )

    for weight_data in all_weights:
        weight = OperatorSourceWeight(**weight_data)
        db.add(weight)

    db.commit()
    print(f"  - Configured weights for {len(sources)} sources")


def create_leads(db):
    """Create leads."""
    print("\nCreating leads...")
    leads_data = [
        {
            "external_id": "tg_user_12345",
            "name": "Иван Сидоров",
            "phone": "+79001234567",
            "email": "ivan@example.com",
        },
        {
            "external_id": "wa_user_98765",
            "name": "Мария Петрова",
            "phone": "+79009876543",
            "email": "maria@example.com",
        },
        {
            "external_id": "web_user_11111",
            "name": "Алексей Смирнов",
            "phone": "+79001111111",
            "email": "alex@example.com",
        },
        {
            "external_id": "vb_user_22222",
            "name": "Екатерина Козлова",
            "phone": "+79002222222",
            "email": None,
        },
        {
            "external_id": "ig_user_33333",
            "name": "Дмитрий Новиков",
            "phone": None,
            "email": "dmitry@example.com",
        },
        {
            "external_id": "tg_user_44444",
            "name": "Ольга Волкова",
            "phone": "+79004444444",
            "email": "olga@example.com",
        },
        {
            "external_id": "wa_user_55555",
            "name": "Сергей Лебедев",
            "phone": "+79005555555",
            "email": None,
        },
        {
            "external_id": "web_user_66666",
            "name": "Наталья Морозова",
            "phone": "+79006666666",
            "email": "natasha@example.com",
        },
        {
            "external_id": "tg_user_77777",
            "name": "Андрей Павлов",
            "phone": "+79007777777",
            "email": "andrey@example.com",
        },
        {
            "external_id": "ig_user_88888",
            "name": "Юлия Соколова",
            "phone": "+79008888888",
            "email": "julia@example.com",
        },
    ]

    leads = []
    for lead_data in leads_data:
        lead = Lead(**lead_data)
        db.add(lead)
        leads.append(lead)

    db.commit()
    for lead in leads:
        db.refresh(lead)
        print(f"  - {lead.name} (ID: {lead.id}, external_id: {lead.external_id})")

    return leads


def create_appeals(db, leads, sources, operators):
    """Create appeals."""
    print("\nCreating appeals...")

    # Получаем веса для каждого источника
    weights = db.query(OperatorSourceWeight).all()
    source_operators = {}
    for weight in weights:
        if weight.source_id not in source_operators:
            source_operators[weight.source_id] = []
        source_operators[weight.source_id].append(weight.operator_id)

    appeals_data = [
        # СПЕЦИАЛЬНО СОЗДАЕМ 10 АКТИВНЫХ ОБРАЩЕНИЙ ДЛЯ КОЛЕСНИКА ПЕТРА (operator_id=1)
        # чтобы довести его до max_load=10
        {
            "lead_id": leads[0].id,
            "source_id": sources[2].id,
            "message": "Обращение 1 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        {
            "lead_id": leads[1].id,
            "source_id": sources[2].id,
            "message": "Обращение 2 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        {
            "lead_id": leads[2].id,
            "source_id": sources[2].id,
            "message": "Обращение 3 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        {
            "lead_id": leads[3].id,
            "source_id": sources[2].id,
            "message": "Обращение 4 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        {
            "lead_id": leads[4].id,
            "source_id": sources[2].id,
            "message": "Обращение 5 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        {
            "lead_id": leads[5].id,
            "source_id": sources[2].id,
            "message": "Обращение 6 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        {
            "lead_id": leads[6].id,
            "source_id": sources[2].id,
            "message": "Обращение 7 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        {
            "lead_id": leads[7].id,
            "source_id": sources[2].id,
            "message": "Обращение 8 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        {
            "lead_id": leads[8].id,
            "source_id": sources[2].id,
            "message": "Обращение 9 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        {
            "lead_id": leads[9].id,
            "source_id": sources[2].id,
            "message": "Обращение 10 для Петра",
            "is_active": True,
            "operator_id": 1,
        },
        # Остальные обращения для других операторов
        {
            "lead_id": leads[0].id,
            "source_id": sources[0].id,
            "message": "Здравствуйте! Хочу узнать о вашем продукте",
            "is_active": True,
        },
        {
            "lead_id": leads[1].id,
            "source_id": sources[1].id,
            "message": "Добрый день! Интересует цена",
            "is_active": True,
        },
        {
            "lead_id": leads[4].id,
            "source_id": sources[4].id,
            "message": "Увидел в сторис, расскажите подробнее",
            "is_active": True,
        },
        {
            "lead_id": leads[9].id,
            "source_id": sources[4].id,
            "message": "Красивые фото! Где купить?",
            "is_active": True,
        },
    ]

    appeals = []
    for appeal_data in appeals_data:
        # Если operator_id уже указан (для тестовых обращений Петра), используем его
        # Иначе назначаем оператора на основе весов
        if "operator_id" not in appeal_data:
            source_id = appeal_data["source_id"]
            if source_id in source_operators:
                available_ops = source_operators[source_id]
                operator_id = random.choice(available_ops)
                appeal_data["operator_id"] = operator_id

        appeal = Appeal(**appeal_data)
        db.add(appeal)
        appeals.append(appeal)

    db.commit()

    # Статистика по операторам
    print(f"  - Created {len(appeals)} appeals")
    print("\nAppeals distribution:")
    for operator in operators:
        count = sum(1 for a in appeals if a.operator_id == operator.id)
        active_count = sum(1 for a in appeals if a.operator_id == operator.id and a.is_active)
        print(f"  - {operator.name}: {count} total ({active_count} active)")

    return appeals


def main():
    """Main function to seed database."""
    print("=" * 60)
    print("SEEDING DATABASE WITH TEST DATA")
    print("=" * 60)

    # Initialize database
    init_db()

    # Create session
    db = SessionLocal()

    try:
        # Clear existing data
        clear_database(db)

        # Create entities
        operators = create_operators(db)
        sources = create_sources(db)
        create_weights(db, operators, sources)
        leads = create_leads(db)
        appeals = create_appeals(db, leads, sources, operators)

        print("\n" + "=" * 60)
        print("DATABASE SEEDED SUCCESSFULLY!")
        print("=" * 60)
        print("\nSummary:")
        print(f"  - Operators: {len(operators)}")
        print(f"  - Sources: {len(sources)}")
        print(f"  - Leads: {len(leads)}")
        print(f"  - Appeals: {len(appeals)}")
        print("\nYou can now test the API at http://localhost:8000/docs\n")

    except Exception as e:
        print(f"\nError: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
