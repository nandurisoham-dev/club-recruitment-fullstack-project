import { useState, useEffect } from "react";

const API_URL = "http://127.0.0.1:8001";

function Coordinator({ count, refresh }) {
    const [summary, setSummary] = useState([]);
    const [selectedClubId, setSelectedClubId] = useState("");
    const [clubDetail, setClubDetail] = useState(null);
    const [error, setError] = useState("");
    const [name, setName] = useState("");
    const [category, setCategory] = useState("technical");
    const [seats, setSeats] = useState(5);
    const [deadline, setDeadline] = useState("");

function getSummary() {
    fetch(API_URL + "/summary").then((res) => res.json())
    .then((data) => {
        if (data.detail) {
            setError(data.detail);
        }
        else {
            setSummary(data);
        }
    });
}

function getClubDetail(id) {
    if (id === "") {
        setClubDetail(null);
    }
    else {
        fetch(API_URL + "/clubs/" + id).then((res) => res.json())
        .then((data) => {
            if (data.detail) {
                setError(data.detail);
            }
            else {
                setClubDetail(data);
            }
        });
    }
}

useEffect(() => {
    getSummary();
    if (selectedClubId !== "") {
        getClubDetail(selectedClubId);
    }
}, [count]);

function changeClub(id) {
    setSelectedClubId(id);
    getClubDetail(id);
}

function toggleRecruiting() {
    let newStatus = 0;
    if (clubDetail.recruiting === 0) {
        newStatus = 1;
    }
    
    let url = API_URL + "/clubs/" + clubDetail.id + "/recruitment?recruiting=" + newStatus;
    
    fetch(url, { method: "PATCH" }).then((res) => res.json())
    .then((data) => {
        if (data.detail) {
            setError(data.detail);
        }
        else {
            setError("");
            getClubDetail(clubDetail.id);
            getSummary();
            refresh();
        }
    });
}

function changeAppStatus(id, newStatus) {
    let url = API_URL + "/applications/" + id + "/status?status=" + newStatus;
    
    fetch(url, { method: "PATCH" }).then((res) => res.json())
    .then((data) => {
        if (data.detail) {
            setError(data.detail);
        }
        else {
            setError("");
            getClubDetail(selectedClubId);
            getSummary();
            refresh();
        }
    });
}

function createClub() {
    let url = API_URL + "/clubs?name=" + name + "&category=" + category + "&seats=" + seats + "&deadline=" + deadline;
    
    fetch(url, { method: "POST" }).then((res) => res.json())
    .then((data) => {
        if (data.detail) {
            setError(data.detail);
        }
        else {
            setName("");
            setDeadline("");
            setError("");
            getSummary();
            refresh();
        }
    });
}

return (
    <>
      <h2>Coordinator</h2>
      <p>{error}</p>

      <h3>Summary</h3>
      {summary.map((item) => (
        <section key={item.club_id}>
          <p>
            <b>{item.club_name}</b> - Applied: {item.applied}, Shortlisted: {item.shortlisted}, Selected: {item.selected}, Rejected: {item.rejected}
          </p>
        </section>
      ))}

      <h3>Add Club</h3>
      <p>
        <input
          placeholder="Name"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
        <select value={category} onChange={(event) => setCategory(event.target.value)}>
          <option value="technical">technical</option>
          <option value="cultural">cultural</option>
          <option value="sports">sports</option>
          <option value="social">social</option>
          <option value="literary">literary</option>
        </select>
        <input
          type="number"
          min="1"
          max="30"
          placeholder="Seats"
          value={seats}
          onChange={(event) => setSeats(event.target.value)}
        />
        <input
          placeholder="YYYY-MM-DD"
          value={deadline}
          onChange={(event) => setDeadline(event.target.value)}
        />
        <button onClick={createClub}>Add</button>
      </p>

      <h3>Manage Club</h3>
      <select value={selectedClubId} onChange={(event) => changeClub(event.target.value)}>
        <option value="">Select Club</option>
        {summary.map((item) => (
          <option key={item.club_id} value={item.club_id}>
            {item.club_name}
          </option>
        ))}
      </select>

      {clubDetail && (
        <section>
          <h4>
            {clubDetail.name} - {clubDetail.recruiting === 1 ? "Open" : "Closed"}
            <button onClick={toggleRecruiting}>
              {clubDetail.recruiting === 1 ? "Close" : "Open"}
            </button>
          </h4>

          {clubDetail.applications.map((app) => (
            <p key={app.id}>
              Roll No: {app.roll_no} | Reason: {app.why_join} | Status: {app.status}
              <button onClick={() => changeAppStatus(app.id, "shortlisted")}>Shortlist</button>
              <button onClick={() => changeAppStatus(app.id, "selected")}>Select</button>
              <button onClick={() => changeAppStatus(app.id, "rejected")}>Reject</button>
            </p>
          ))}
        </section>
      )}
    </>
  );
}

export default Coordinator;