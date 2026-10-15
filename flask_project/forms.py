import re
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class EventRegistrationForm(FlaskForm):
    """
    Форма реєстрації на базі Flask-WTF (WTForms).
    Містить 4 різнотипні поля з декларативними валідаторами українською мовою
    та кастомними методами валідації validate_*().
    """

    PARTICIPATION_CHOICES = [
        ('', '-- Оберіть формат участі --'),
        ('online', 'Онлайн-участь (Вільний доступ)'),
        ('offline', 'Офлайн у залі (м. Київ, HUB Cyberspace)'),
        ('vip', 'VIP (Воркшопи, сертифікат та нетворкінг)'),
    ]

    # 1. Текстове поле з обмеженням довжини
    full_name = StringField(
        'ПІБ учасника',
        validators=[
            DataRequired(message="Поле «ПІБ учасника» є обов'язковим для заповнення."),
            Length(min=4, max=50, message="Довжина ПІБ повинна становити від 4 до 50 символів.")
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Шевченко Тарас Григорович'
        }
    )

    # 2. Поле електронної пошти
    email = EmailField(
        'Електронна пошта',
        validators=[
            DataRequired(message="Поле «Електронна пошта» є обов'язковим для заповнення."),
            Email(message="Введено некоректний формат адреси електронної пошти.")
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'taras@cyber.ua'
        }
    )

    # 3. Поле вибору зі списку варіантів
    ticket_type = SelectField(
        'Формат участі',
        choices=PARTICIPATION_CHOICES,
        validators=[
            DataRequired(message="Будь ласка, оберіть дійсний формат участі.")
        ],
        render_kw={
            'class': 'form-select'
        }
    )

    # 4. Багаторядкове текстове поле
    message = TextAreaField(
        'Мотиваційний лист або коментар',
        validators=[
            DataRequired(message="Будь ласка, заповніть мотиваційний лист або запитання."),
            Length(min=10, max=500, message="Довжина тексту має бути від 10 до 500 символів.")
        ],
        render_kw={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Чому ви бажаєте взяти участь у конференції та які теми вас найбільше цікавлять?'
        }
    )

    def validate_full_name(self, field):
        """
        Кастомна валідація ПІБ:
        - перевірка наявності щонайменше двох слів (прізвище та ім'я);
        - заборона цифр та спеціальних символів.
        """
        val = (field.data or '').strip()
        words = val.split()

        if len(words) < 2:
            raise ValidationError("ПІБ повинно містити щонайменше два слова (ім'я та прізвище).")

        if not re.match(r"^[A-Za-zА-Яа-яІіЇїЄєҐґ'\-\s]+$", val):
            raise ValidationError(
                "ПІБ може містити лише літери, пробіли, дефіси та апострофи (без цифр та спецсимволів)."
            )

    def validate_message(self, field):
        """
        Кастомна валідація тексту повідомлення:
        - перевірка на мінімальну кількість слів (бізнес-правило: не менше 3 слів).
        """
        val = (field.data or '').strip()
        words = val.split()

        if len(words) < 3:
            raise ValidationError(
                f"Повідомлення занадто коротке ({len(words)} сл.). Мінімальна кількість слів — 3."
            )
