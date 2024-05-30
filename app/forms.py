from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, EmailField, PasswordField, DateTimeField, IntegerField, SelectField, TextAreaField, \
    FileField, BooleanField, SelectMultipleField, SubmitField
from wtforms.validators import Length, Email, DataRequired, NumberRange


class CreateUpdateDoctorForm(FlaskForm):
    first_name = StringField("Ім'я: ",
                             validators=[Length(2, 100, "Ім'я має бути від 2 до 100 символів"),
                                         DataRequired(message='Заповніть поле')])

    last_name = StringField("Прізвище: ",
                            validators=[Length(2, 100, "Прізвище має бути від 2 до 100 символів"),
                                        DataRequired(message='Заповніть поле')])

    middle_name = StringField("По-батькові: ",
                              validators=[Length(2, 100, "По-батькові має бути від 2 до 100 символів"),
                                          DataRequired(message='Заповніть поле')])

    phone = StringField("Номер телефону: ",
                        validators=[Length(2, 100, "Номер телефону має бути від 10 до 13 символів"),
                                    DataRequired(message='Заповніть поле')])

    email = EmailField("Електрона адреса: ",
                       validators=[Email(), DataRequired(message='Заповніть поле')])

    LOAN_SPECIALIZATION = (
        ('Терапевтична стоматологія', 'Терапевтична стоматологія'),
        ('Ортодонтія', 'Ортодонтія'),
        ('Хірургічна стоматологія', 'Хірургічна стоматологія'),
        ('Ендодонтія', 'Ендодонтія'),
        ('Періодонтологія', 'Періодонтологія'),
        ('Педіатрична стоматологія', 'Педіатрична стоматологія'),
        ('Протезування', 'Протезування')
    )

    specialization = SelectField('Спеціалізація: ', choices=LOAN_SPECIALIZATION,
                                 validators=[DataRequired(message='Заповніть поле')])

    photo = FileField('Фото лікаря',
                      validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Тільки зображення')])

    submit = SubmitField('Підтвердити')


class ConfirmDeleteForm(FlaskForm):
    confirm = BooleanField('Підтвердіть видалення ',
                           validators=[DataRequired()])

    submit = SubmitField('Підтвердити')


class CreateUpdateProcedureTypeForm(FlaskForm):
    name = StringField('Назва процедури: ',
                       validators=[DataRequired(message='Заповніть поле'),
                                   Length(2, 100, "Назва має бути від 2 до 100 символів")])

    price = IntegerField('Ціна процедури: ',
                         validators=[DataRequired(message='Заповніть поле'),
                                     NumberRange(1, message='Ціна має бути від 0')])

    details = TextAreaField('Деталі: ', validators=[DataRequired(message='Заповніть поле')])

    submit = SubmitField('Підтвердити')


class LoginForm(FlaskForm):
    username = StringField("Нікнейм: ",
                           validators=[DataRequired(message='Заповніть поле'),
                                       Length(4, message='Нікнейм має бути від 4 символів')])

    password = PasswordField("Пароль: ",
                             validators=[DataRequired(message='Заповніть поле'),
                                         Length(8, message='Пароль має бути від 8 символів')])

    remember = BooleanField("Запам'ятати мене")

    submit = SubmitField('Підтвердити')


class RegistrationForm(FlaskForm):
    first_name = StringField("Ім'я: ",
                             validators=[DataRequired(message='Заповніть поле'),
                                         Length(4, 100, message="Ім'я має бути від 4 символів")])

    last_name = StringField("Прізвище: ",
                            validators=[DataRequired(message='Заповніть поле'),
                                        Length(4, 100, message='Прізвище має бути від 4 символів')])

    middle_name = StringField("По-батькові: ",
                              validators=[DataRequired(message='Заповніть поле'),
                                          Length(4, 100, message='По-батькові має бути від 4 символів')])

    username = StringField("Нікнейм: ",
                           validators=[DataRequired(message='Заповніть поле'),
                                       Length(4, 100, message='Нікнейм має бути від 4 символів')])

    email = EmailField('Електрона адреса: ',
                       validators=[DataRequired(message='Заповніть поле'),
                                   Length(5, 100, message='Електрона адреса має бути до 100 символів')])

    password = PasswordField("Пароль: ",
                             validators=[DataRequired(message='Заповніть поле'),
                                         Length(8, message='Пароль має бути від 8 символів')])

    submit = SubmitField('Підтвердити')


class CreateProcedureFormForUsers(FlaskForm):
    date_time = (DateTimeField('Дата та час проведення процедури (наприклад 2022-03-31 19:30:00)',
                               validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S'))

    doctor = SelectField('Лікар: ',
                         validators=[DataRequired(message='Заповніть поле')])

    procedure_type = SelectMultipleField('Назва процедури: ',
                                         validators=[DataRequired(message='Заповніть поле')])

    details = TextAreaField('Деталі: ')

    submit = SubmitField('Підтвердити')


class CreateUpdateProcedureFormForAdmins(FlaskForm):
    date_time = DateTimeField('Дата та час проведення процедури (наприклад 2022-03-31 19:30:00)',
                              validators=[DataRequired(message='Заповніть поле')])

    doctor = SelectField('Лікар: ',
                         validators=[DataRequired(message='Заповніть поле')])

    patient = SelectField('Пацієнт: ',
                          validators=[DataRequired(message='Заповніть поле')])

    procedure_type = SelectMultipleField('Назва процедури: ',
                                         validators=[DataRequired(message='Заповніть поле')])

    LOAN_STATUS = (
        ('Заплановано', 'Заплановано'),
        ('Підтверджено', 'Підтверджено'),
        ('Виконано', 'Виконано'),
        ('Прострочено', 'Прострочено')
    )

    status = SelectField('Статус: ', choices=LOAN_STATUS,
                         validators=[DataRequired(message='Заповніть поле')])

    details = TextAreaField('Деталі: ')

    submit = SubmitField('Підтвердити')


class UpdateUserForm(FlaskForm):
    first_name = StringField("Ім'я: ",
                             validators=[DataRequired(message='Заповніть поле'),
                                         Length(4, 100, message="Ім'я має бути від 4 символів")])

    last_name = StringField("Прізвище: ",
                            validators=[DataRequired(message='Заповніть поле'),
                                        Length(4, 100, message='Прізвище має бути від 4 символів')])

    middle_name = StringField("По-батькові: ",
                              validators=[DataRequired(message='Заповніть поле'),
                                          Length(4, 100, message='По-батькові має бути від 4 символів')])

    username = StringField("Нікнейм: ",
                           validators=[DataRequired(message='Заповніть поле'),
                                       Length(4, 100, message='Нікнейм має бути від 4 символів')])

    email = EmailField('Електрона адреса: ',
                       validators=[DataRequired(message='Заповніть поле'),
                                   Length(5, 100, message='Електрона адреса має бути до 100 символів')])

    submit = SubmitField('Підтвердити')


class UpdateUserFormForAdmin(FlaskForm):
    first_name = StringField("Ім'я: ",
                             validators=[DataRequired(message='Заповніть поле'),
                                         Length(4, 100, message="Ім'я має бути від 4 символів")])

    last_name = StringField("Прізвище: ",
                            validators=[DataRequired(message='Заповніть поле'),
                                        Length(4, 100, message='Прізвище має бути від 4 символів')])

    middle_name = StringField("По-батькові: ",
                              validators=[DataRequired(message='Заповніть поле'),
                                          Length(4, 100, message='По-батькові має бути від 4 символів')])

    username = StringField("Нікнейм: ",
                           validators=[DataRequired(message='Заповніть поле'),
                                       Length(4, 100, message='Нікнейм має бути від 4 символів')])

    email = EmailField('Електрона адреса: ',
                       validators=[DataRequired(message='Заповніть поле'),
                                   Length(5, 100, message='Електрона адреса має бути до 100 символів')])

    role = SelectField('Роль: ',
                       validators=[DataRequired(message='Заповніть поле')])

    submit = SubmitField('Підтвердити')
