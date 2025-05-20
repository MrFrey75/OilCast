from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Board, Page, Section, page_sections

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return redirect(url_for('main.admin'))


@main.route('/board/<int:board_id>')
def show_board(board_id):
    board = Board.query.get_or_404(board_id)
    if board.page_view_time:
        board.page_view_time = int(board.page_view_time)
    else:
        board.page_view_time = 10  # default to 10 seconds
    # Check if the board is empty
    if not board.pages:
        flash("This board has no pages.", "warning")
        return redirect(url_for('main.admin'))
    # Sort pages by order
    pages = sorted(board.pages, key=lambda p: p.order)
    return render_template('board.html', board=board, pages=pages)


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    boards = Board.query.all()
    if request.method == 'POST':
        name = request.form.get('board_name', '').strip()
        if not name:
            flash("Board name cannot be empty.", "danger")
        else:
            db.session.add(Board(name=name))
            db.session.commit()
            flash("Board created successfully!", "success")
        return redirect(url_for('main.admin'))
    return render_template('admin.html', boards=boards)


@main.route('/admin/board/<int:board_id>', methods=['GET', 'POST'])
def edit_board(board_id):
    board = Board.query.get_or_404(board_id)

    if request.method == 'POST':
        name = request.form.get('page_name', 'Untitled Page').strip()
        order = request.form.get('order', 0)
        db.session.add(Page(name=name, board_id=board.id, order=int(order)))
        db.session.commit()
        flash("Page added!", "success")
        return redirect(url_for('main.edit_board', board_id=board.id))
    return render_template('edit_board.html', board=board)


@main.route('/admin/page/<int:page_id>/edit', methods=['GET', 'POST'])
def edit_page(page_id):
    page = Page.query.get_or_404(page_id)

    if request.method == 'POST':
        page.order = int(request.form.get('order', page.order))
        page.name = request.form.get('name', page.name).strip()

        db.session.execute(page_sections.delete().where(page_sections.c.page_id == page.id))

        section_ids = request.form.getlist('section_ids')
        for idx, section_id in enumerate(section_ids):
            db.session.execute(page_sections.insert().values(
                page_id=page.id,
                section_id=int(section_id),
                position=idx
            ))

        db.session.commit()
        flash("Page updated!", "success")
        return redirect(url_for('main.edit_board', board_id=page.board_id))

    all_sections = Section.query.all()
    current_section_ids = [s.id for s in page.sections]

    return render_template(
        'edit_page.html',
        page=page,
        available_sections=all_sections,
        current_section_ids=current_section_ids
    )


@main.route('/admin/page/<int:page_id>/delete', methods=['POST'])
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)
    board_id = page.board_id

    db.session.execute(page_sections.delete().where(page_sections.c.page_id == page.id))
    db.session.delete(page)
    db.session.commit()

    flash("Page deleted!", "warning")
    return redirect(url_for('main.edit_board', board_id=board_id))


@main.route('/admin/sections')
def list_sections():
    sections = Section.query.all()
    return render_template('sections.html', sections=sections)


@main.route('/admin/section/new', methods=['GET', 'POST'])
def create_section():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title:
            flash("Section title is required.", "danger")
        else:
            db.session.add(Section(title=title, content=content))
            db.session.commit()
            flash("Section created.", "success")
            return redirect(url_for('main.list_sections'))

    return render_template('section_form.html', section=None)


@main.route('/admin/section/<int:section_id>', methods=['GET', 'POST'])
def edit_section(section_id):
    section = Section.query.get_or_404(section_id)
    if request.method == 'POST':
        section.title = request.form.get('title', section.title).strip()
        section.content = request.form.get('content', section.content)
        db.session.commit()
        flash("Section updated.", "success")
        return redirect(url_for('main.list_sections'))
    return render_template('section_form.html', section=section)


@main.route('/admin/reset-db', methods=['POST'])
def reset_db():
    db.drop_all()
    db.create_all()

    from .seed_demo import seed_demo_data
    seed_demo_data()

    flash("✅ Database has been reset and seeded with demo data.", "success")
    return redirect(url_for('main.admin'))


@main.route('/admin/board/<int:board_id>/update', methods=['POST'])
def update_board(board_id):
    board = Board.query.get_or_404(board_id)
    name = request.form.get('name', '').strip()
    page_view_time = request.form.get('page_view_time', 10)

    if not name:
        flash("Board name cannot be empty.", "danger")
    else:
        board.name = name
        board.page_view_time = int(request.form.get('page_view_time', 10))
        db.session.commit()
        flash("Board updated successfully!", "success")

    return redirect(url_for('main.edit_board', board_id=board.id))
