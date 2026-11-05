import { useState } from "react";
import Clubs from "./components/Clubs";
import MyApplications from "./components/MyApplications";
import Coordinator from "./components/Coordinator";

function App() {
  const [count, setCount] = useState(0);

  function refreshData() {
    setCount(count + 1);
  }

  return (
    <>
      <h1>Club Recruitment Portal</h1>
      <Clubs refresh={refreshData} />
      <MyApplications refresh={refreshData} />
      <Coordinator count={count} refresh={refreshData} />
    </>
  );
}

export default App;