import re
from django import forms


class EventRegistrationForm(forms.Form):
    PARTICIPATION_CHOICES = [
        ('', '-- Оберіть формат участі --'),
        ('online', 'Онлайн-участь (Вільний доступ)'),
        ('offline', 'Офлайн у залі (м. Київ, HUB Cyberspace)'),
        ('vip', 'VIP (Воркшопи, сертифікат та нетворкінг)'),
    ]

    # 1. Текстове поле з обмеженням довжини
    full_name = forms.CharField(
        max_length=50,
        min_length=4,
        label="ПІБ учасника",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Шевченко Тарас Григорович'
        }),
        help_text="Вкажіть прізвище та ім'я кирилицею або латиницею"
    )

    # 2. Поле електронної пошти
    email = forms.EmailField(
        label="Електронна пошта",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'taras@cyber.ua'
        }),
        help_text="На цю пошту буде надіслано запрошення"
    )

    # 3. Поле вибору зі списку варіантів
    ticket_type = forms.ChoiceField(
        choices=PARTICIPATION_CHOICES,
        label="Формат участі",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    # 4. Багаторядкове текстове поле
    message = forms.CharField(
        label="Мотиваційний лист або коментар",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Чому ви бажаєте взяти участь у конференції та які теми вас найбільше цікавлять?'
        }),
        help_text="Щонайменше 3 слова"
    )

    def clean_full_name(self):
        """
        Кастомна валідація ПІБ:
        - перевірка на наявність щонайменше двох слів (прізвище та ім'я);
        - заборона цифр та спеціальних символів.
        """
        full_name = self.cleaned_data.get('full_name', '').strip()
        words = full_name.split()

        if len(words) < 2:
            raise forms.ValidationError(
                "ПІБ повинно містити щонайменше два слова (ім'я та прізвище)."
            )

        # Дозволені лише літери кирилиці, латиниці, апостроф, дефіс та пробіл
        if not re.match(r"^[A-Za-zА-Яа-яІіЇїЄєҐґ'\-\s]+$", full_name):
            raise forms.ValidationError(
                "ПІБ може містити лише літери, пробіли, дефіси та апострофи (без цифр та спецсимволів)."
            )

        return full_name

    def clean_message(self):
        """
        Кастомна валідація тексту повідомлення:
        - перевірка на мінімальну кількість слів (бізнес-правило: не менше 3 слів).
        """
        message = self.cleaned_data.get('message', '').strip()
        words = message.split()

        if len(words) < 3:
            raise forms.ValidationError(
                f"Повідомлення занадто коротке ({len(words)} сл.). Мінімальна кількість слів — 3."
            )

        return message
