import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import api from "../services/api";

export default function EditIncident() {
  const {id} = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    title: "",
    description: "",
    priority: "",
    status: "",
    assignedTo: "",
    createdBy: "",
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    api.get(`/incidents/${id}`)
      .then((res) => setForm(res.data))
      .catch((err) => console.log("Error fetching incident:", err));
  }, [id]);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: "" });
  }

  function validate() {
    const newErrors = {};
    if (!form.title.trim()) newErrors.title = "Title is required";
    if (!form.description.trim()) newErrors.description = "Description is required";
    if (!form.priority) newErrors.priority = "Priority is required";
    if (!form.status) newErrors.status = "Status is required";
    if (!form.assignedTo.trim()) newErrors.assignedTo = "Assigned To is required";
    return newErrors;
  }

  function handleSubmit(e) {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    console.log("Updating:", form);
    api.put(`/incidents/${id}`, form)
      .then(() => navigate("/incidents"))
      .catch((err) => console.log("Error updating incident:", err));
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <button
        onClick={() => navigate("/incidents")}
        className="text-sm text-brand hover:underline mb-4 block">
        ← Back to Incidents
      </button>

      <div className="bg-white border border-gray-200 rounded-lg p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Edit Incident</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Title</label>
            <input
              type="text"
              name="title"
              value={form.title}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-brand"/>
            {errors.title && <p className="text-red-500 text-xs mt-1">{errors.title}</p>}
          </div>

          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Description</label>
            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-brand"
              rows={3}/>
            {errors.description && <p className="text-red-500 text-xs mt-1">{errors.description}</p>}
          </div>

          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Priority</label>
            <select
              name="priority"
              value={form.priority}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-brand">
              <option value="">Select priority</option>
              <option value="LOW">LOW</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HIGH">HIGH</option>
              <option value="CRITICAL">CRITICAL</option>
            </select>
            {errors.priority && <p className="text-red-500 text-xs mt-1">{errors.priority}</p>}
          </div>

          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Status</label>
            <select
              name="status"
              value={form.status}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-brand">
              <option value="">Select status</option>
              <option value="OPEN">OPEN</option>
              <option value="IN_PROGRESS">IN_PROGRESS</option>
              <option value="RESOLVED">RESOLVED</option>
            </select>
            {errors.status && <p className="text-red-500 text-xs mt-1">{errors.status}</p>}
          </div>

          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Assigned To</label>
            <input
              type="text"
              name="assignedTo"
              value={form.assignedTo}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-brand"/>
            {errors.assignedTo && <p className="text-red-500 text-xs mt-1">{errors.assignedTo}</p>}
          </div>

          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Created By</label>
            <input
              type="text"
              name="createdBy"
              value={form.createdBy}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-brand"/>
            {errors.createdBy && <p className="text-red-500 text-xs mt-1">{errors.createdBy}</p>}
          </div>

          <button
            type="submit"
            className="w-full bg-brand hover:bg-blue-900 text-white px-4 py-3 rounded-lg text-sm font-medium min-h-[44px] transition-colors mt-2">
            Update
          </button>
        </form>
      </div>
    </div>
  );
}