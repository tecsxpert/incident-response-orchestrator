package com.internship.tool.service;

import com.internship.tool.entity.Incident;
import com.internship.tool.repository.IncidentRepository;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class IncidentService {

    private final IncidentRepository repository;

    public IncidentService(IncidentRepository repository) {
        this.repository = repository;
    }

    public Incident create(Incident incident) {
        return repository.save(incident);
    }

    public Incident update(UUID id, Incident updated) {
        Incident incident = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Not found"));

        incident.setTitle(updated.getTitle());
        incident.setDescription(updated.getDescription());
        incident.setStatus(updated.getStatus());
        incident.setPriority(updated.getPriority());
        incident.setAssignedTo(updated.getAssignedTo());

        return repository.save(incident);
    }

    public void delete(UUID id) {
        repository.deleteById(id);
    }
}