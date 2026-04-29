package com.internship.tool.controller;

import com.internship.tool.entity.Incident;
import com.internship.tool.repository.IncidentRepository;
import com.internship.tool.service.AuditService;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/incidents")
public class IncidentController {

    private final IncidentRepository repository;
    private final AuditService auditService;

    public IncidentController(IncidentRepository repository,
                              AuditService auditService) {
        this.repository = repository;
        this.auditService = auditService;
    }

    // ✅ GET ALL
    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER','VIEWER')")
    public List<Incident> getAll() {
        return repository.findAll();
    }

    // ✅ CREATE INCIDENT (ADDED)
    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public Incident createIncident(@RequestBody Incident incident,
                                  Authentication auth) {

        Incident saved = repository.save(incident);

        // 🔥 AUDIT
        auditService.log("INCIDENT_CREATED", auth.getName());

        return saved;
    }

    // ✅ UPDATE INCIDENT (FIXED)
    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public Incident updateIncident(@PathVariable UUID id,
                                  @RequestBody Incident updated,
                                  Authentication auth) {

        Incident incident = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Incident not found"));

        // update fields safely
        incident.setTitle(updated.getTitle());
        incident.setDescription(updated.getDescription());
        incident.setStatus(updated.getStatus());
        incident.setPriority(updated.getPriority());
        incident.setAssignedTo(updated.getAssignedTo());

        Incident saved = repository.save(incident);

        // 🔥 AUDIT
        auditService.log("INCIDENT_UPDATED", auth.getName());

        return saved;
    }

    // ✅ DELETE INCIDENT (FIXED)
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public String deleteIncident(@PathVariable UUID id,
                                Authentication auth) {

        Incident incident = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Incident not found"));

        repository.delete(incident);

        // 🔥 AUDIT
        auditService.log("INCIDENT_DELETED", auth.getName());

        return "Incident deleted";
    }
}