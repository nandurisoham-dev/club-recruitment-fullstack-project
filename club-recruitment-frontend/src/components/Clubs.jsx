import {useState, useEffect} from "react";

const API_URL = "http://127.0.0.1:8001";

function Clubs({ refresh }) {
    const [clubs, setClubs] = useState([]);
    const [category, setCategory] = useState("");
    const [selectedClubId, setSelectedClubId] = useState(null);
    const [rollNo, setRollNo] = useState("");
    const [whyJoin, setWhyJoin] = useState("");
    const [error, setError] = useState("");

function getClubs() {
    let url = API_URL + "/clubs";
    if (category !== "") {
        url = API_URL + "/clubs?category=" + category;
    }
    fetch(url).then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        }
        else {
            setClubs(data);
            setError("");
        }
    });
}

useEffect(() => {
    getClubs();
}, [category]);

function submitApplication() {
    let url = API_URL + "/clubs/" + selectedClubId + "/applications";
    url = url + "?roll_no=" + rollNo + "&why_join=" + whyJoin;

    fetch(url, { method: "POST" }).then((res) => res.json())
      .then((data) => {
        if (data.detail) {
            setError(data.detail);
        }
        else {
            setRollNo("");
            setWhyJoin("");
            setSelectedClubId(null);
            setError("");
            getClubs();
            refresh();
        }
    });
}

return (
    <>
      <h2>Clubs</h2>
      <p>{error}</p>

      <label>Filter: </label>
      <select value={category} onChange={(event) => setCategory(event.target.value)}>
        <option value="">All</option>
        <option value="technical">technical</option>
        <option value="cultural">cultural</option>
        <option value="sports">sports</option>
        <option value="social">social</option>
        <option value="literary">literary</option>
      </select>

      {clubs.map((club) => (
        <section key={club.id}>
          <h3>{club.name} {club.recruiting === 0 && "(Closed)"}</h3>
          <p>Category: {club.category}</p>
          <p>Seats: {club.seats}</p>
          <p>Deadline: {club.deadline}</p>
          <p>Applications: {club.application_count}</p>
          {club.recruiting === 1 && (
            <button onClick={() => setSelectedClubId(club.id)}>Apply</button>
          )}
        </section>
      ))}

      {selectedClubId && (
        <section>
          <h3>Apply</h3>
          <p>
            <input
              type="text"
              placeholder="Roll Number"
              value={rollNo}
              onChange={(event) => setRollNo(event.target.value)}
            />
          </p>
          <p>
            <input
              type="text"
              placeholder="Why join?"
              value={whyJoin}
              onChange={(event) => setWhyJoin(event.target.value)}
            />
          </p>
          <p>
            <button onClick={submitApplication}>Submit</button>
            <button onClick={() => setSelectedClubId(null)}>Cancel</button>
          </p>
        </section>
      )}
    </>
  );
}

export default Clubs;