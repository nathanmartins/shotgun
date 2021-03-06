import os
from datetime import datetime

from flask import render_template, request, redirect, flash
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import FileForm
from runner import Runner
from .models import Result


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FileForm()

    if form.validate_on_submit():
        file = request.files['file']

        filename = secure_filename(file.filename)

        full_filename = '/tmp/shotgun/' + filename

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        r = Runner(full_filename)
        r.run()

        res = Result(
            filename=filename,
            real=r.run_results['real'],
            user=r.run_results['user'],
            sys=r.run_results['sys'],
            output=r.output,
            datetime=datetime.now(),
        )

        db.session.add(res)
        db.session.commit()

        flash('Successfully created result!')

        return redirect('/results')

    context = {
        'title': 'Home',
        'form': form,
    }

    return render_template('index.html', **context)


@app.route('/results', )
def results():
    res = Result.query.all()

    return render_template('list.html', results=res)


@app.route('/delete/<int:result_id>', )
def delete(result_id):
    res = Result.query.get_or_404(result_id)
    db.session.delete(res)
    db.session.commit()
    flash('Successfully deleted result ID #{}'.format(result_id))

    return redirect('/results')
