import {useState} from "react";
import {useNavigate} from "react-router-dom";
import api from "../services/api";

export default function CreateIncident() {
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

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: "" });
  }

  function validate() {
    const newErrors = {};
    if (!form.title.trim()) newErrors.title = "Title is required*";
    if (!form.description.trim()) newErrors.description = "Description is required*";
    if (!form.priority) newErrors.priority = "Priority is required*";
    if (!form.status) newErrors.status = "Status is required*";
    if (!form.assignedTo.trim()) newErrors.assignedTo = "Assigned To is required*";
    return newErrors;
  }

  function handleSubmit(e) {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    console.log("Submitting:", form);
    api.post("/incidents", form)
      .then(() => navigate("/"))
      .catch((err) => console.log("Error creating incident:", err));
  }

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-4">Create Incident</h1>
      <form onSubmit={handleSubmit} className="space-y-4">

        <div>
          <label className="block mb-1 text-sm font-medium">Title</label>
          <input
            type="text"
            name="title"
            value={form.title}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded px-3 py-2 text-sm"/>
            {errors.title && <p className="text-red-500 text-xs mt-1">{errors.title}</p>}
        </div>

        <div>
          <label className="block mb-1 text-sm font-medium">Description</label>
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
            rows={3} />
            {errors.description && <p className="text-red-500 text-xs mt-1">{errors.description}</p>}
        </div>

        <div>
          <label className="block mb-1 text-sm font-medium">Priority</label>
          <select 
            name="priority" 
            value={form.priority} 
            onChange={handleChange}
            className="w-full border border-gray-300 rounded px-3 py-2 text-sm">
            <option value="">Select priority</option>
            <option value="LOW">LOW</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="HIGH">HIGH</option>
            <option value="CRITICAL">CRITICAL</option>
          </select>
          {errors.priority && <p className="text-red-500 text-xs mt-1">{errors.priority}</p>}
        </div>

        <div>
          <label className="block mb-1 text-sm font-medium">Status</label>
          <select
            name="status"
            value={form.status}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded px-3 py-2 text-sm">
            <option value="">Select status</option>
            <option value="OPEN">OPEN</option>
            <option value="IN_PROGRESS">IN_PROGRESS</option>
            <option value="RESOLVED">RESOLVED</option>
          </select>
          {errors.status && <p className="text-red-500 text-xs mt-1">{errors.status}</p>}
        </div>

        <div>
          <label className="block mb-1 text-sm font-medium">Assigned To</label>
          <input
            type="text"
            name="assignedTo"
            value={form.assignedTo}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded px-3 py-2 text-sm" />
          {errors.assignedTo && <p className="text-red-500 text-xs mt-1">{errors.assignedTo}</p>}
        </div>

        <div>
          <label className="block mb-1 text-sm font-medium">Created By</label>
          <input
          type="text"
          name="createdBy"
          value={form.createdBy}
          onChange={handleChange}
          className="w-full border border-gray-300 rounded px-3 py-2 text-sm" />
          {errors.createdBy && <p className="text-red-500 text-xs mt-1">{errors.createdBy}</p>}
        </div>

        <button
          type="submit"
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm">
          Create
        </button>

      </form>
    </div>
  );
}