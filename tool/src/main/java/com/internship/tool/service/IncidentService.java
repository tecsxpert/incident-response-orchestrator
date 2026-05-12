package com.internship.tool.service;

import com.internship.tool.entity.Incident;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.repository.IncidentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class IncidentService {

    @Autowired
    private IncidentRepository incidentRepository;

    @Autowired
    private EmailService emailService;

    public Incident createIncident(Incident incident) {
        if (incident.getTitle() == null || incident.getTitle().isEmpty()) {
            throw new IllegalArgumentException("Title is required");
        }
        if (incident.getStatus() == null) {
            incident.setStatus("OPEN");
        }

        Incident saved = incidentRepository.save(incident);
        emailService.sendIncidentCreatedEmail(saved.getId(), saved.getTitle(), saved.getStatus());
        return saved;
    }

    public Incident updateIncident(Incident incident) {
        return incidentRepository.save(incident);
    }

    public Incident getIncidentById(Long id) {
        return incidentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Incident not found with id: " + id));
    }

    public Page<Incident> getAllIncidents(Pageable pageable) {
        return incidentRepository.findAll(pageable);
    }
}