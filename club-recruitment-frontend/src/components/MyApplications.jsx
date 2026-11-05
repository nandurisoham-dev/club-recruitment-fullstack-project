import {useState} from "react";

const API_URL = "http://127.0.0.1:8001";

function MyApplications({ refresh }) {
    const [rollNo, setRollNo] = useState("");
    const [applications, setApplications] = useState([]);
    const [error, setError] = useState("");

function getMyApps() {
    let url = API_URL + "/students/" + rollNo + "/applications";

    fetch(url).then((res) => res.json())
    .then((data) => {
        if (data.detail) {
            setError(data.detail);
            setApplications([]);
        }
        else {
            setApplications(data);
            setError("");
        }
    });
}

function withdrawApp(id) {
    let url = API_URL + "/applications/" + id + "/withdraw?roll_no=" + rollNo;

    fetch(url, { method: "PATCH" }).then((res) => res.json())
    .then((data) => {
        if (data.detail) {
            setError(data.detail);
        }
        else {
            setError("");
            getMyApps();
            refresh();
        }
    });
}

return (
    <>
      <h2>My Applications</h2>
      <p>{error}</p>

      <p>
        <input
          type="text"
          placeholder="Roll Number"
          value={rollNo}
          onChange={(event) => setRollNo(event.target.value)}
        />
        <button onClick={getMyApps}>Show</button>
      </p>

      <ul>
        {applications.map((app) => (
          <li key={app.id}>
            {app.club_name} - {app.status}{" "}
            {app.status === "applied" && (
              <button onClick={() => withdrawApp(app.id)}>Withdraw</button>
            )}
          </li>
        ))}
      </ul>
    </>
  );
}

export default MyApplications;