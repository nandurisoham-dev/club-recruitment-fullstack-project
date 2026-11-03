# club-recruitment-fullstack-project
Problem statement:

A school has a club management council and the club secretary is very unorganised where he/she messes up the records of students recruiting for
different clubs during club recruitment drive. A team comes up with a great idea of creating a web application that stores student records during start
of the club recruitment drive and the web application must display the open clubs looking for new members and submit applications by which the club
secretary's life becomes easy.

Roles assigned:

Day 1: Backend API

Files required: main.py, functions.py, recruitment.db
Libraries needed: FastAPI + SQLite

Soham: E7, E8, E9
Tanush: E4, E5, E6
Abrar: E1, E2, E3

Database file name: recruitment.db
Tables: clubs and applications

clubs: id, name, category, seats, deadline, recruiting (1 or 0)
applications: id, club_id, roll_no, why_join, status, applied_on

Category must be one of: technical, cultural, sports, social, literary.
Status is one of: applied, shortlisted, selected, rejected, withdrawn.

Day 2: Frontend

Files required: Clubs.jsx, MyApplications.jsx, and Coordinator.jsx in src/components, and app.jsx in src/
npm module installation required

Soham: Coordinator.jsx + App.jsx implementation
Tanush: Clubs.jsx + App.jsx implementation
Abrar: MyApplications.jsx + App.jsx implementation


API contracts

E1: Get all the clubs. Can be filtered by category. Each one includes its number of applications that aren't withdrawn.
Method: GET
Path: /clubs
Request: None
Success response: 200 (Okay)
Error code: 422 (Invalid Category)

E2: Get one club by its id, with its list of applications.
Method: GET
Path: /clubs/{club_id}
Request: None
Success response: 200 (Okay)
Error code: 404 (club doesn't exist)

E3: Add a club: name, category, seats and deadline. It starts recruiting.
Method: POST
Path: /clubs
Request: name, category, seats, deadline
Success response: 201 (Creation success)
Error code: 422 (Missing fields or invalid data)

E4: Open or close a club's recruitment.
Method: PATCH
Path: /clubs/{club_id}/recruitment
Request: recruiting
Success response: 200 (Okay)
Error code: 404 (If the club id doesn't exist), 422 (Invalid data apart from yes or no)

E5: Apply to a club: roll number and why you want to join. It starts as applied.
Method: POST
Path: /clubs/{club_id}/applications
Request: roll_no, why_join
Success response: 201 (Application got added)
Error code: 400 (Bad request. The student attempts to join another club after they have joined another 3 clubs or tries to applies for same club again),
            404 (The club doesn't exist), 422 (Invalid status apart from applied, shortlisted, selected, rejected, withdrawn.)

E6: Move an application to shortlisted, selected or rejected.
Method: PATCH
Path: /applications/{application_id}/status
Request: status
Success response: 200 (Status updated successfully)
Error code: 400 (Wrong change as per rules or the club is full), 404(The application ID doesn't exist), 422(Missing status)

E7: Withdraw an application, with the applicant's roll number.
Method: PATCH
Path: /applications/{application_id}/withdraw
Request: roll_no
Success response: 200 (Okay, application withdrawn)
Error code: 400 (Unable to withdraw application), 403 (Restricted action, the roll number doesn't match the applicant), 404 (Application doesn't exist),
			422 (Missing roll number or invalid roll number)

E8: Get one student's applications, by roll number. Each one includes the club's name.
Method: GET
Path: /students/{roll_no}/applications
Request: None
Success response: 200 (Okay, students applications with club names)
Error code: 404 (Roll number doesn't exist) 422 (If the roll number is invalid or missing)

E9: Get the summary: for each club, how many applications are applied, shortlisted, selected and rejected.
Method: GET
Path: /summary
Request: None
Success response: 200 (Okay, application counts for each club)
Error code: 500 (Unexpected server error)

