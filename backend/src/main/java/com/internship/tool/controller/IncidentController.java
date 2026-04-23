package com.internship.tool.controller;

import com.internship.tool.entity.Incident;
import com.internship.tool.repository.IncidentRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/incidents")
public class IncidentController {

    private final IncidentRepository repository;

    public IncidentController(IncidentRepository repository) {
        this.repository = repository;
    }

    // 🔹 UPDATE INCIDENT
    @PutMapping("/{id}")
    public Incident updateIncident(@PathVariable UUID id, @RequestBody Incident updated) {
        Incident incident = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Incident not found"));

        incident.setTitle(updated.getTitle());
        incident.setDescription(updated.getDescription());
        incident.setStatus(updated.getStatus());
        incident.setPriority(updated.getPriority());
        incident.setAssignedTo(updated.getAssignedTo());

        return repository.save(incident);
    }

    // 🔹 SOFT DELETE
    @DeleteMapping("/{id}")
    public String deleteIncident(@PathVariable UUID id) {
        Incident incident = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Incident not found"));

        incident.setIsDeleted(true);
        repository.save(incident);

        return "Incident soft deleted";
    }

    // 🔹 SEARCH
    @GetMapping("/search")
    public List<Incident> search(@RequestParam String q) {
        return repository.search(q);
    }

    // 🔹 STATS (TOTAL COUNT)
    @GetMapping("/stats")
    public long stats() {
        return repository.count();
    }
}