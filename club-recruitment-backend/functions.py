from sqlalchemy import Integer, String, Column, ForeignKey, create_engine
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "recruitment.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Clubs(Base):
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    seats = Column(Integer)
    deadline = Column(String)
    recruiting = Column(Integer, default=1)

class Applications(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.id'))
    roll_no = Column(String)
    why_join = Column(String)
    status = Column(String, default='applied')
    applied_on = Column(String)

Base.metadata.create_all(engine)

def get_all_clubs(category=None):
    session = Session(engine)
    clubs = session.query(Clubs).all()
    applications = session.query(Applications).all()
    response = []

    for club in clubs:
        if category and club.category != category:
            continue
        
        count = 0
        for application in applications:
            if application.club_id == club.id and application.status != 'withdrawn':
                count = count + 1
        
        response.append({
            'id': club.id,
            'name': club.name,
            'category': club.category,
            'seats': club.seats,
            'deadline': club.deadline,
            'recruiting': club.recruiting,
            'application_count': count
        })

    session.close()
    return response

def get_club_by_id(club_id):
    session = Session(engine)
    club = session.get(Clubs, club_id)
    if not club:
        session.close()
        return None

    applications = session.query(Applications).all()
    club_apps = []
    for application in applications:
        if application.club_id == club_id:
            club_apps.append({
                'id': application.id,
                'club_id': application.club_id,
                'roll_no': application.roll_no,
                'why_join': application.why_join,
                'status': application.status,
                'applied_on': application.applied_on
            })

    session.close()
    return {
        'id': club.id,
        'name': club.name,
        'category': club.category,
        'seats': club.seats,
        'deadline': club.deadline,
        'recruiting': club.recruiting,
        'applications': club_apps
    }

def add_new_club(name, category, seats, deadline):
    session = Session(engine)
    new_club = Clubs(name=name, category=category, seats=seats, deadline=deadline, recruiting=1)
    session.add(new_club)
    session.commit()

    response = {
        'id': new_club.id,
        'name': new_club.name,
        'category': new_club.category,
        'seats': new_club.seats,
        'deadline': new_club.deadline,
        'recruiting': new_club.recruiting
    }
    session.close()
    return response

def update_club_recruitment(club_id, recruiting):
    session = Session(engine)
    club = session.get(Clubs, club_id)
    if not club:
        session.close()
        return None

    club.recruiting = recruiting
    session.commit()
    session.close()
    return {'id': club_id, 'recruiting': recruiting}

def apply_club(club_id, roll_no, why_join):
    session = Session(engine)
    
    d = datetime.now()
    today = f"{d.day:02d}-{d.month:02d}-{d.year}"

    application = Applications(
        club_id=club_id,
        roll_no=roll_no,
        why_join=why_join,
        status='applied',
        applied_on=today
    )
    session.add(application)
    session.commit()

    response = {
        'id': application.id,
        'club_id': application.club_id,
        'roll_no': application.roll_no,
        'why_join': application.why_join,
        'status': application.status,
        'applied_on': application.applied_on
    }
    session.close()
    return response

def update_status(application_id, status):
    session = Session(engine)
    application = session.get(Applications, application_id)
    if not application:
        session.close()
        return None

    application.status = status
    session.commit()
    session.close()
    return {'id': application_id, 'status': status}

def withdraw_app(application_id):
    session = Session(engine)
    app = session.get(Applications, application_id)
    if not app:
        session.close()
        return None

    app.status = 'withdrawn'
    session.commit()
    session.close()
    return {'id': application_id, 'status': 'withdrawn'}

def get_student_apps(roll_no):
    session = Session(engine)
    applications = session.query(Applications).all()
    clubs = session.query(Clubs).all()
    response = []

    for application in applications:
        if application.roll_no == roll_no:
            club_name = ''
            for club in clubs:
                if club.id == application.club_id:
                    club_name = club.name
                    break
            
            response.append({
                'id': application.id,
                'club_id': application.club_id,
                'club_name': club_name,
                'roll_no': application.roll_no,
                'why_join': application.why_join,
                'status': application.status,
                'applied_on': application.applied_on
            })

    session.close()
    if len(response) == 0:
        return None
    return response

def get_summary():
    session = Session(engine)
    clubs = session.query(Clubs).all()
    applications = session.query(Applications).all()
    response = []

    for club in clubs:
        application_count = 0
        shortlist_count = 0
        selection_count = 0
        rejection_count = 0

        for application in applications:
            if application.club_id == club.id:
                if application.status == 'applied':
                    application_count = application_count + 1
                elif application.status == 'shortlisted':
                    shortlist_count = shortlist_count + 1
                elif application.status == 'selected':
                    selection_count = selection_count + 1
                elif application.status == 'rejected':
                    rejection_count = rejection_count + 1

        response.append({
            'club_id': club.id,
            'club_name': club.name,
            'applied': application_count,
            'shortlisted': shortlist_count,
            'selected': selection_count,
            'rejected': rejection_count
        })

    session.close()
    return response