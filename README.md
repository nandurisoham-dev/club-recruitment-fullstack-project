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

Soham: E1, E2, E3, E4, E5, E6, E7, E8, E9

Database file name: recruitment.db
Tables: clubs and applications

clubs: id, name, category, seats, deadline, recruiting (1 or 0)
applications: id, club_id, roll_no, why_join, status, applied_on

Category must be one of: technical, cultural, sports, social, literary.
Status is one of: applied, shortlisted, selected, rejected, withdrawn.

Day 2: Frontend

Files required: Clubs.jsx, MyApplications.jsx, and Coordinator.jsx in src/components, and app.jsx in src/
npm module installation required

Soham: Coordinator.jsx + App.jsx implementation, Clubs.jsx, MyApplications.jsx


API contracts

E1: Get all clubs
Method: GET
Path: /clubs
Request: category (Query parameter, optional string)
Success Code: 200
Error Code: 422 (Invalid category)

E2: Get one club by ID
Method: GET
Path: /clubs/{club_id}
Request: club_id (Path parameter, integer)
Success Code: 200
Error Code: 404 (Club that doesn't exist)

E3: Add a club
Method: POST
Path: /clubs
Request: JSON body with name, category, seats, deadline
Success Code: 201
Error Code: 422 (Missing fields or invalid values)

E4: Open or close recruitment
Method: PATCH
Path: /clubs/{club_id}/recruitment
Request: club_id (Path parameter, integer) and recruiting (Query parameter, integer: 1 or 0)
Success Code: 200
Error Code: 404 (Club doesn't exist), 422 (Value entry apart from 1 or 0)

E5: Apply to a club
Method: POST
Path: /clubs/{club_id}/applications
Request: club_id (Path parameter, integer) and JSON body with roll_no, why_join
Success Code: 201
Error Code: 400 (Club closed, user attempt to join same club again, or attempting to join more than 3 clubs),
            404 (Club doesn't exist), 422 (missing fields)

E6: Update application status
Method: PATCH
Path: /applications/{application_id}/status
Request: application_id (Path parameter, integer) and status (Query parameter, string)
Success Code: 200
Error Code: 400 (Invalid status transition, club is filled, or student selection limitation),
            404 (Application not found), 422 (Invalid status choice)

E7: Withdraw application
Method: PATCH
Path: /applications/{application_id}/withdraw
Request: application_id (Path parameter, integer) and roll_no (Query parameter, string)
Success Code: 200
Error Code: 400 (Cannot withdraw after shortlisting),
            403 (Roll number does not match applicant), 404 (Application not found), 422 (Missing roll number)

E8: Get student applications
Method: GET
Path: /students/{roll_no}/applications
Request: roll_no (Path parameter, string)
Success Code: 200
Error Code: 404 (No applications found for this student), 422 (Invalid roll number format)

E9: Get recruitment summary
Method: GET
Path: /summary
Request: None
Success Code: 200
Error Code: 500 (Server failure)
