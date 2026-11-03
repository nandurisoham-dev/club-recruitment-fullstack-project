from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {"message": "Recruitment backend running"}

@app.get("/clubs")
def get_clubs(category=None):
    if category and category not in ["technical", "cultural", "sports", "social", "literary"]:
        raise HTTPException(status_code=422, detail="Invalid category")
    return functions.get_all_clubs(category)

@app.get("/clubs/{club_id}")
def get_club_by_id(club_id):
    club = functions.get_club_by_id(club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return club

@app.post("/clubs")
def add_club(name, category, seats: int, deadline):
    if not name or not category or not deadline:
        raise HTTPException(status_code=422, detail="Missing fields")
    if category not in ["technical", "cultural", "sports", "social", "literary"]:
        raise HTTPException(status_code=422, detail="Invalid category")
    if seats < 1 or seats > 30:
        raise HTTPException(status_code=422, detail="Seats must be 1 to 30")
    if len(deadline) != 10:
        raise HTTPException(status_code=422, detail="Invalid deadline format")
    
    return functions.add_new_club(name, category, seats, deadline)

@app.patch("/clubs/{club_id}/recruitment")
def update_recruitment(club_id, recruiting=None):
    if recruiting not in ["0", "1", 0, 1]:
        raise HTTPException(status_code=422, detail="Recruiting must be 1 or 0")

    response = functions.update_club_recruitment(club_id, int(recruiting))
    if not response:
        raise HTTPException(status_code=404, detail="Club not found")
    return response

@app.post("/clubs/{club_id}/applications")
def apply_to_club(club_id, roll_no, why_join):
    if not roll_no or not why_join:
        raise HTTPException(status_code=422, detail="Missing fields")
    if len(why_join) < 20:
        raise HTTPException(status_code=422, detail="Reason too short")

    club = functions.get_club_by_id(club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    if club["recruiting"] == 0:
        raise HTTPException(status_code=400, detail="Recruitment closed")

    for app_item in club["applications"]:
        if app_item["roll_no"] == roll_no and app_item["status"] != "withdrawn":
            raise HTTPException(status_code=400, detail="Already applied")

    student_applications = functions.get_student_apps(roll_no)
    if student_applications:
        active = 0
        for item in student_applications:
            if item["status"] in ["applied", "shortlisted"]:
                active = active + 1
        if active >= 3:
            raise HTTPException(
                status_code=400, detail="Only 3 active applications allowed"
            )

    return functions.apply_club(club_id, roll_no, why_join)

@app.patch("/applications/{application_id}/status")
def update_status(application_id, status):
    if status not in ["shortlisted", "selected", "rejected"]:
        raise HTTPException(status_code=422, detail="Invalid status")

    target_app = None
    target_club = None
    for club in functions.get_all_clubs():
        club_detail = functions.get_club_by_id(club["id"])
        for app_item in club_detail["applications"]:
            if app_item["id"] == int(application_id):
                target_app = app_item
                target_club = club_detail
                break

    if not target_app:
        raise HTTPException(status_code=404, detail="Application not found")

    current_status = target_app["status"]
    if current_status == "applied" and status not in ["shortlisted", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status transition")
    if current_status == "shortlisted" and status not in ["selected", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status transition")
    if current_status in ["selected", "rejected", "withdrawn"]:
        raise HTTPException(status_code=400, detail="Cannot change status")

    if status == "selected":
        selected_in_club = 0
        for item in target_club["applications"]:
            if item["status"] == "selected":
                selected_in_club = selected_in_club + 1

        if selected_in_club >= target_club["seats"]:
            raise HTTPException(status_code=400, detail="Club is full")

        student_applications = functions.get_student_apps(
            target_app["roll_no"]
        )
        student_selected = 0
        if student_applications:
            for item in student_applications:
                if item["status"] == "selected":
                    student_selected = student_selected + 1

        if student_selected >= 2:
            raise HTTPException(
                status_code=400, detail="Student selected in 2 clubs already"
            )

    return functions.update_status(application_id, status)

@app.patch("/applications/{application_id}/withdraw")
def withdraw(application_id: int, roll_no=None):
    if not roll_no:
        raise HTTPException(status_code=422, detail="Missing roll number")

    target_app = None
    for club in functions.get_all_clubs():
        club_detail = functions.get_club_by_id(club["id"])
        for a in club_detail["applications"]:
            if a["id"] == application_id:
                target_app = a
                break

    if not target_app:
        raise HTTPException(status_code=404, detail="Application not found")

    if target_app["roll_no"] != roll_no:
        raise HTTPException(status_code=403, detail="Action not allowed")

    if target_app["status"] != "applied":
        raise HTTPException(status_code=400, detail="Cannot withdraw after shortlisting")

    return functions.withdraw_app(application_id)

@app.get("/students/{roll_no}/applications")
def get_student_applications(roll_no):
    applications = functions.get_student_apps(roll_no)
    if not applications:
        raise HTTPException(status_code=404, detail="No applications found")
    return applications

@app.get("/summary")
def summary():
    return functions.get_summary()