from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventRegistrationForm


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
        'seats_left': 0,  # Для демонстрації {% if %}
        'price': 500,
        'level': 'All levels'
    },
]


def home(request):
    """
    Головна сторінка.
    Демонструє передачу рядка, числа та списку елементів.
    """
    context = {
        'page_title': 'CyberEvents Hub — Платформа освітніх та професійних подій',
        'hero_subtitle': 'Офіційний майданчик реєстрації на заходи кафедри інформаційної та кібернетичної безпеки',
        'attendees_count': 1450,
        'speaker_count': 18,
        'featured_highlights': [
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
        ],
    }
    return render(request, 'events/home.html', context)


def event_list(request):
    """
    Сторінка каталогу подій.
    Передає контекст: рядкову змінну, числове значення та список словників.
    У шаблоні використовуються цикли for, if та DTL фільтри (truncatewords, date, length, default).
    """
    context = {
        'section_title': 'Розклад подій та воркшопів конференції',
        'total_events': len(SAMPLE_EVENTS),
        'discount_rate': 15,
        'events': SAMPLE_EVENTS,
    }
    return render(request, 'events/event_list.html', context)


def register(request):
    """
    Сторінка реєстрації з формою та серверною валідацією:
    - GET: відображення порожньої форми;
    - POST: валідація, збереження, повідомлення flash і redirect при успіху;
      або повернення форми з помилками при некоректних даних.
    """
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            ticket_type_label = dict(EventRegistrationForm.PARTICIPATION_CHOICES).get(
                form.cleaned_data['ticket_type']
            )
            # Flash-повідомлення через django.contrib.messages
            messages.success(
                request,
                f"Успішна реєстрація! Учасника «{full_name}» зареєстровано у форматі «{ticket_type_label}». "
                f"Електронний квиток надіслано на адресу {email}."
            )
            return redirect('events:register')
        else:
            messages.error(request, "Помилка валідації! Перевірте правильність заповнення полів форми.")
    else:
        form = EventRegistrationForm()

    context = {
        'page_title': 'Реєстрація учасника конференції',
        'open_slots': 42,
        'form': form,
    }
    return render(request, 'events/register.html', context)
