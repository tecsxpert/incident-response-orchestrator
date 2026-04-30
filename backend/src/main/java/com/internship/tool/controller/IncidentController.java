package com.internship.tool.controller;

import com.internship.tool.entity.Incident;
import com.internship.tool.service.IncidentService;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.access.prepost.PreAuthorize;

import java.util.UUID;

@RestController
@RequestMapping("/incidents")
public class IncidentController {

    private final IncidentService service;

    public IncidentController(IncidentService service) {
        this.service = service;
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public Incident create(@RequestBody Incident incident) {
        return service.create(incident);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public Incident update(@PathVariable UUID id, @RequestBody Incident updated) {
        return service.update(id, updated);
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public String delete(@PathVariable UUID id) {
        service.delete(id);
        return "Deleted";
    }
}