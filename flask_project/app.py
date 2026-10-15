from datetime import date, datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from config import Config
from forms import EventRegistrationForm

app = Flask(__name__)
app.config.from_object(Config)

# Забезпечення захисту від CSRF (Завдання 1.2, 5, 6)
csrf = CSRFProtect(app)

SAMPLE_EVENTS = [
    {
        'id': 1,
        'title': 'Аналіз сучасних загроз та векторів кібератак у 2026 році',
        'speaker': 'д-р техн. наук Олександр Коваленко',
        'date': date(2026, 11, 14),
        'category': 'Кіберрозвідка (CTI)',
        'description': (
            'Комплексний огляд новітніх методів виявлення цільових атак APT, '
            'використання штучного інтелекту зловмисниками та превентивні механізми '
            'моніторингу інфраструктури критичних об’єктів.'
        ),
        'seats_left': 15,
        'price': 0,
        'level': 'Advanced'
    },
    {
        'id': 2,
        'title': 'Побудова захищених Web-додатків: від CSRF до витоків пам’яті',
        'speaker': 'Марія Мельник (Lead AppSec Engineer)',
        'date': date(2026, 11, 15),
        'category': 'Application Security',
        'description': (
            'Практичний воркшоп з безпечної розробки на Python, архітектури безпеки сесій, '
            'запобігання XSS, CSRF-атакам та впровадження стандарту безпеки OWASP Top 10.'
        ),
        'seats_left': 8,
        'price': 450,
        'level': 'Intermediate'
    },
    {
        'id': 3,
        'title': 'Криптографічний захист каналів зв’язку та постквантові алгоритми',
        'speaker': 'проф. Дмитро Василенко',
        'date': date(2026, 11, 20),
        'category': 'Криптографія',
        'description': (
            'Аналіз нових криптографічних стандартів, оцінка стійкості до атак квантових комп’ютерів '
            'та рекомендації щодо міграції корпоративних систем на нові протоколи шифрування.'
        ),
        'seats_left': 25,
        'price': 300,
        'level': 'Advanced'
    },
    {
        'id': 4,
        'title': 'DevSecOps: інтеграція перевірок коду в автоматизовані CI/CD пайплайни',
        'speaker': 'Ігор Ткачук (Senior DevOps & SecOps)',
        'date': date(2026, 11, 22),
        'category': 'DevSecOps',
        'description': (
            'Покроковий посібник з автоматизації SAST/DAST сканування у GitHub Actions та GitLab CI, '
            'контроль вразливих залежностей та управління секретами у хмарних середовищах.'
        ),
        'seats_left': 0,
        'price': 500,
        'level': 'All levels'
    },
]


@app.context_processor
def inject_globals():
    """Глобальні змінні для шаблонів Jinja2 (наприклад, поточний рік для підвалу)."""
    return {
        'current_year': datetime.now().year,
        'app_framework': 'Flask 3.x / Jinja2'
    }


@app.route('/')
def home():
    """
    Головна сторінка Flask.
    Передає контекстні змінні: рядок, числа, список словників.
    """
    featured_highlights = [
        {
            'title': 'Провідні експерти галузі',
            'description': 'Доповіді від практикуючих інженерів та науковців з міжнародною сертифікацією OSCP, CISSP.',
            'badge': 'Якість'
        },
        {
            'title': 'Практичні воркшопи',
            'description': 'Реальні симуляції кібератак на тестових стендах та захист корпоративного периметра.',
            'badge': 'Практика'
        },
        {
            'title': 'Сертифікація учасників',
            'description': 'Офіційний сертифікат про підвищення кваліфікації або проходження інтенсиву.',
            'badge': 'Сертифікат'
        },
    ]
    return render_template(
        'home.html',
        page_title='CyberEvents Hub — Платформа освітніх та професійних подій',
        hero_subtitle='Офіційний майданчик реєстрації на заходи кафедри інформаційної та кібернетичної безпеки',
        attendees_count=1450,
        speaker_count=18,
        featured_highlights=featured_highlights
    )


@app.route('/events/')
def event_list():
    """
    Сторінка каталогу подій Flask.
    Демонструє Jinja2 конструкції (включно з арифмецевтичними виразами та викликом методів).
    """
    return render_template(
        'event_list.html',
        section_title='Розклад подій та воркшопів конференції',
        total_events=len(SAMPLE_EVENTS),
        discount_rate=15,
        events=SAMPLE_EVENTS
    )


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Маршрут реєстрації з формою Flask-WTF:
    - GET: рендеринг порожньої форми;
    - POST: перевірка validate_on_submit();
      при успіху — flash() та redirect(url_for('register'));
      при помилках — повернення форми з помилками та збереженими даними.
    """
    form = EventRegistrationForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        # Отримання читабельного імені вибору
        ticket_label = dict(EventRegistrationForm.PARTICIPATION_CHOICES).get(form.ticket_type.data, form.ticket_type.data)

        flash(
            f"Успішна реєстрація! Учасника «{full_name}» зареєстровано у форматі «{ticket_label}». "
            f"Електронний квиток надіслано на адресу {email}.",
            'success'
        )
        return redirect(url_for('register'))
    elif request.method == 'POST':
        flash("Помилка валідації! Перевірте правильність заповнення полів форми.", "danger")

    return render_template(
        'register.html',
        page_title='Реєстрація учасника конференції',
        open_slots=42,
        form=form
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
