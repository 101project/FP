import mailing
...

@module.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register function.
    """
    if form.validate_on_submit():
        *### Registering the new user here* ###
        mailing.send_awaiting_confirm_mail(new_user)
        flash(messages.EMAIL_VALIDATION_SENT, 'info')
        return redirect(url_for('index'))
    else:
        if not g.user:
            return render_template('register.html', form=form)
        else:
            return redirect(url_for('index'))

#Para activar el usuario.
@module.route('/activate_user/<user_id>')
def activate_user(user_id):
    """
    Activate user function.
    """
    found_user = *### Getting user in db from id here ###*
    if not found_user:
        return abort(404)
    else:
        if found_user['status'] == 'awaiting_confirm':
            *### Setting the user status active here ###*
            mailing.send_subscription_confirmed_mail(found_user)
            flash('user has been activated', 'info')
        elif found_user['status'] == 'active':
            flash('user already activated', 'info')
        return redirect(url_for('login'))
