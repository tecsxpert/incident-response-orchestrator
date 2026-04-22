import {BrowserRouter, Routes, Route} from "react-router-dom";
import IncidentList from "./pages/IncidentList";
import CreateIncident from "./pages/CreateIncident";
import EditIncident from "./pages/EditIncident";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<IncidentList />} />
        <Route path="/create" element={<CreateIncident />} />
        <Route path="/edit/:id" element={<EditIncident />} />
      </Routes>
    </BrowserRouter>
  );
}