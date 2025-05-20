from .models import db, Board, Page, Section, page_sections, User


def seed_demo_data():
    board = Board(name="Demo Board")
    db.session.add(board)
    db.session.commit()

    s1 = Section(title="Welcome Message", content="<p>Welcome to the Demo Board!</p>")
    s2 = Section(title="Today's Announcements", content="<ul><li>Lunch at noon</li><li>Assembly at 2pm</li></ul>")
    s3 = Section(title="Fun Fact", content="<p>Did you know flamingos bend their legs at the ankle, not the knee?</p>")
    db.session.add_all([s1, s2, s3])
    db.session.commit()

    page = Page(name="Demo Page", order=0, board_id=board.id)
    db.session.add(page)
    db.session.commit()

    db.session.execute(page_sections.insert().values([
        {'page_id': page.id, 'section_id': s1.id, 'position': 0},
        {'page_id': page.id, 'section_id': s2.id, 'position': 1},
        {'page_id': page.id, 'section_id': s3.id, 'position': 2}
    ]))

    # Create demo admin user
    admin = User(username="admin", is_admin=True)
    db.session.add(admin)

    user = User(username="viewer", is_admin=False)
    db.session.add(user)

    db.session.commit()
