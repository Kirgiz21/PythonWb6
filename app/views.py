import os

from flask_login import login_user, login_required, logout_user, current_user

from app import db, app
from .models import Doctor, Procedure, ProcedureType, User, Role
from flask import render_template, request, url_for, redirect, flash
from werkzeug.utils import secure_filename

from app.forms import CreateUpdateDoctorForm, ConfirmDeleteForm, CreateUpdateProcedureTypeForm, LoginForm, \
    RegistrationForm, CreateUpdateProcedureFormForAdmins, CreateProcedureFormForUsers, UpdateUserForm, \
    UpdateUserFormForAdmin


@app.route('/')
def index():
    doc_count = db.session.query(Doctor).count()
    pt_count = db.session.query(ProcedureType).count()
    patient_count = db.session.query(Role).filter(Role.name == 'Пацієнт').count()
    return render_template('index.html', doc_count=doc_count, pt_count=pt_count, patient_count=patient_count)


@app.route('/doctors/')
def doctors():
    doc = db.session.query(Doctor).order_by(Doctor.specialization).all()
    return render_template('doctors.html', doctors=doc)


@app.route('/doctors/<int:pk>/')
def doctor(pk):
    doc = db.session.query(Doctor).get_or_404(pk)
    return render_template('doctor.html', doctor=doc)


@app.route('/doctors/create/', methods=['POST', 'GET'])
def doctor_create():
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))
    form = CreateUpdateDoctorForm()
    if form.validate_on_submit():
        image = form.photo.data
        image_filename = secure_filename(image.filename)
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image.save(image_url)
        doc = Doctor(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            middle_name=form.middle_name.data,
            phone=form.phone.data,
            email=form.email.data,
            specialization=form.specialization.data,
            photo=image_filename
        )
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('doctors'))
    return render_template('create_update_doctor.html', title='Створити доктора', form=form)


@app.route('/doctors/<int:pk>/renew/', methods=['POST', 'GET'])
def doctor_update(pk):
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))
    form = CreateUpdateDoctorForm()
    doc = db.session.query(Doctor).get_or_404(pk)

    if form.validate_on_submit():
        image = form.photo.data
        image_filename = secure_filename(image.filename)
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image.save(image_url)

        doc.first_name = form.first_name.data
        doc.last_name = form.last_name.data
        doc.middle_name = form.middle_name.data
        doc.phone = form.phone.data
        doc.email = form.email.data
        doc.specialization = form.specialization.data
        doc.photo = image_filename
        db.session.commit()

        return redirect(url_for('doctors'))

    form.first_name.data = doc.first_name
    form.last_name.data = doc.last_name
    form.middle_name.data = doc.middle_name
    form.phone.data = doc.phone
    form.email.data = doc.email
    form.specialization.data = doc.specialization

    return render_template('create_update_doctor.html', title='Оновити доктора', form=form)


@app.route('/doctors/<int:pk>/delete/', methods=['POST', 'GET'])
def doctor_delete(pk):
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))
    doc = db.session.query(Doctor).get_or_404(pk)
    form = ConfirmDeleteForm()

    if form.validate_on_submit() and form.confirm.data:
        db.session.delete(doc)
        db.session.commit()
        return redirect(url_for('doctors'))

    return render_template('delete.html', form=form, model=doc, title='Видалити Лікаря', back='doctors')


@app.route('/procedure_types/')
def procedure_types():
    pts = db.session.query(ProcedureType).order_by(ProcedureType.name).all()
    return render_template('procedure_types.html', procedure_types=pts)


@app.route('/procedure_types/create', methods=['POST', 'GET'])
def procedure_type_create():
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))
    form = CreateUpdateProcedureTypeForm()
    if form.validate_on_submit():
        pt = ProcedureType(
            name=form.name.data,
            price=form.price.data,
            details=form.details.data
        )
        db.session.add(pt)
        db.session.commit()
        return redirect(url_for('procedure_types'))
    return render_template('create_update_procedure_type.html', title='Створити послугу', form=form)


@app.route('/procedure_types/<int:pk>/renew/', methods=['POST', 'GET'])
def procedure_type_update(pk):
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))
    form = CreateUpdateProcedureTypeForm()
    pt = db.session.query(ProcedureType).get_or_404(pk)
    if form.validate_on_submit():
        pt.name = form.name.data
        pt.price = form.price.data
        pt.details = form.details.data
        db.session.commit()
        return redirect(url_for('procedure_types'))
    form.name.data = pt.name
    form.price.data = pt.price
    form.details.data = pt.details
    return render_template('create_update_procedure_type.html', title='Створити послугу', form=form)


@app.route('/procedure_types/<int:pk>/delete/', methods=['POST', 'GET'])
def procedure_type_delete(pk):
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))
    pt = db.session.query(ProcedureType).get_or_404(pk)
    form = ConfirmDeleteForm()

    if form.validate_on_submit() and form.confirm.data:
        db.session.delete(pt)
        db.session.commit()
        return redirect(url_for('procedure_types'))

    return render_template('delete.html', form=form, model=pt, title='Видалити послугу', back='procedure_types')


@app.route('/my_procedures/')
def my_procedures():
    if not current_user.is_authenticated or current_user.role.name != 'Пацієнт':
        return redirect(url_for('index'))
    procedures = current_user.procedures
    return render_template('my_procedures.html', procedures=procedures)


@app.route('/all_procedures/')
def all_procedures():
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))
    procedures = db.session.query(Procedure).order_by(Procedure.created_on).all()
    return render_template('all_procedures.html', procedures=procedures)


@app.route('/all_procedures/create_procedure/', methods=['POST', 'GET'])
def procedure_create_admin():
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))

    form = CreateUpdateProcedureFormForAdmins()

    form.doctor.choices = [(doc.pk, f'{doc.last_name} {doc.first_name}')
                           for doc in Doctor.query.all()]
    form.patient.choices = [(pat.pk, f'{pat.last_name} {pat.first_name}')
                            for pat in User.query.filter(User.role.has(name='Пацієнт')).all()]
    form.procedure_type.choices = [(prt.pk, prt.name)
                                   for prt in ProcedureType.query.all()]

    if form.validate_on_submit():
        doc_pk = int(form.doctor.data)
        pat_pk = int(form.patient.data)
        prt_pk = list(map(int, form.procedure_type.data))

        doc = Doctor.query.get(doc_pk)
        pat = User.query.get(pat_pk)
        prt = ProcedureType.query.filter(ProcedureType.pk.in_(prt_pk)).all()

        procedure = Procedure(
            date_time=form.date_time.data,
            doctor=doc,
            user=pat,
            procedure_types=prt,
            status=form.status.data,
            details=form.details.data
        )

        db.session.add(procedure)
        db.session.commit()

        return redirect(url_for('all_procedures'))
    return render_template('create_update_procedure_admin.html', title='Створити процедуру', form=form)


@app.route('/create_procedure/', methods=['POST', 'GET'])
def procedure_create_user():
    if not current_user.is_authenticated or current_user.role.name != 'Пацієнт':
        return redirect(url_for('index'))

    form = CreateProcedureFormForUsers()

    form.doctor.choices = [(doc.pk, f'{doc.last_name} {doc.first_name}')
                           for doc in Doctor.query.all()]
    form.procedure_type.choices = [(prt.pk, prt.name)
                                   for prt in ProcedureType.query.all()]

    if form.validate_on_submit():
        doc_pk = int(form.doctor.data)
        prt_pk = list(map(int, form.procedure_type.data))

        doc = Doctor.query.get(doc_pk)
        prt = ProcedureType.query.filter(ProcedureType.pk.in_(prt_pk)).all()

        procedure = Procedure(
            date_time=form.date_time.data,
            doctor=doc,
            user=current_user,
            procedure_types=prt,
            status='Заплановано',
            details=form.details.data
        )

        db.session.add(procedure)
        db.session.commit()

        return redirect(url_for('my_procedures'))
    return render_template('create_update_procedure_user.html', title='Створити процедуру', form=form)


@app.route('/all_procedures/<int:pk>/renew/', methods=['POST', 'GET'])
def procedure_update(pk):
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))

    form = CreateUpdateProcedureFormForAdmins()

    form.doctor.choices = [(doc.pk, f'{doc.last_name} {doc.first_name}')
                           for doc in Doctor.query.all()]
    form.patient.choices = [(pat.pk, f'{pat.last_name} {pat.first_name}')
                            for pat in User.query.filter(User.role.has(name='Пацієнт')).all()]
    form.procedure_type.choices = [(prt.pk, prt.name)
                                   for prt in ProcedureType.query.all()]

    procedure = db.session.query(Procedure).get_or_404(pk)

    if form.validate_on_submit():
        doc_pk = int(form.doctor.data)
        pat_pk = int(form.patient.data)
        prt_pk = list(map(int, form.procedure_type.data))

        doc = Doctor.query.get(doc_pk)
        pat = User.query.get(pat_pk)
        prt = ProcedureType.query.filter(ProcedureType.pk.in_(prt_pk)).all()

        procedure.date_time = form.date_time.data
        procedure.doctor = doc
        procedure.user = pat
        procedure.procedure_types = prt
        procedure.status = form.status.data
        procedure.details = form.details.data
        db.session.commit()

        return redirect(url_for('all_procedures'))

    form.date_time.data = procedure.date_time
    form.doctor.data = str(procedure.doctor_id)
    form.patient.data = str(procedure.user_id)
    form.procedure_type.data = [str(prt.pk) for prt in procedure.procedure_types]
    form.status.data = procedure.status
    form.details.data = procedure.details

    return render_template('create_update_procedure_admin.html', title='Оновити процедуру', form=form)


@app.route('/all_procedures/<int:pk>/delete/', methods=['POST', 'GET'])
def procedure_delete(pk):
    if not current_user.is_authenticated or (current_user.role.name != 'Адміністратор' and current_user.role.name != 'Супер адмін'):
        return redirect(url_for('index'))
    procedure = db.session.query(Procedure).get_or_404(pk)
    form = ConfirmDeleteForm()

    if form.validate_on_submit() and form.confirm.data:
        db.session.delete(procedure)
        db.session.commit()
        return redirect(url_for('procedure_types'))

    return render_template('delete.html', form=form, model=procedure, title='Видалити процедуру', back='all_procedures')


@app.route('/profile/')
def profile():
    if not current_user.is_authenticated or current_user.role.name != 'Пацієнт':
        return redirect(url_for('index'))

    return render_template('profile.html')


@app.route('/profile/update/', methods=['POST', 'GET'])
def profile_update():
    if not current_user.is_authenticated or current_user.role.name != 'Пацієнт':
        return redirect(url_for('index'))

    form = UpdateUserForm()

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.middle_name = form.middle_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        return redirect(url_for('profile'))

    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.middle_name.data = current_user.middle_name
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('profile_update.html', form=form)


@app.route('/admin/')
def admin():
    if not current_user.is_authenticated or current_user.role.name != 'Супер адмін':
        return redirect(url_for('index'))

    users = User.query.filter(~User.role.has(name='Супер адмін')).all()
    return render_template('admin.html', users=users)


@app.route('/admin/user/<int:pk>/update/', methods=['POST', 'GET'])
def user_update(pk):
    if not current_user.is_authenticated or current_user.role.name != 'Супер адмін':
        return redirect(url_for('index'))

    user = db.session.query(User).get_or_404(pk)
    form = UpdateUserFormForAdmin()

    form.role.choices = [(role.pk, f'{role.name}')
                         for role in Role.query.all()]

    if form.validate_on_submit():
        role_pk = int(form.role.data)
        role = Role.query.get(role_pk)

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.middle_name = form.middle_name.data
        user.username = form.username.data
        user.email = form.email.data
        user.role = role
        db.session.commit()

        return redirect(url_for('profile'))

    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.middle_name.data = user.middle_name
    form.username.data = user.username
    form.email.data = user.email
    form.role.data = str(user.role_id)
    return render_template('user_update.html', form=form)


@app.route('/admin/user/<int:pk>/delete/', methods=['POST', 'GET'])
def user_delete(pk):
    if not current_user.is_authenticated or current_user.role.name != 'Супер адмін':
        return redirect(url_for('index'))

    user = db.session.query(User).get_or_404(pk)
    form = ConfirmDeleteForm()

    if form.validate_on_submit() and form.confirm.data:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('delete.html', form=form, model=current_user, title='Видалити користувача', back='admin')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username ==
                                             form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash("Invalid username/password", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        role_patient_pk = db.session.query(Role).filter(Role.name == 'Пацієнт').first().pk
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            middle_name=form.middle_name.data,
            username=form.username.data,
            email=form.email.data,
            role_id=role_patient_pk
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('registration.html', form=form)


@app.route('/logout/')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))
