package com.internship.tool.controller;

import com.internship.tool.dto.IncidentDTO;
import com.internship.tool.entity.Incident;
import com.internship.tool.service.IncidentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@Slf4j
@RestController
@RequestMapping("/incidents")
public class IncidentController {

    @Autowired
    private IncidentService incidentService;

    /**
     * GET /incidents - List all incidents
     * @return list of all incidents
     */
    @GetMapping
    public ResponseEntity<List<Incident>> getAllIncidents() {
        log.info("GET /incidents - Retrieving all incidents");
        List<Incident> incidents = incidentService.getAllIncidents();
        return ResponseEntity.ok(incidents);
    }

    /**
     * GET /incidents/{id} - Get incident by ID
     * @param id incident ID
     * @return incident if found, 404 otherwise
     */
    @GetMapping("/{id}")
    public ResponseEntity<Incident> getIncidentById(@PathVariable Long id) {
        log.info("GET /incidents/{} - Retrieving incident by ID", id);
        Optional<Incident> incident = incidentService.getIncidentById(id);
        if (incident.isPresent()) {
            return ResponseEntity.ok(incident.get());
        } else {
            log.warn("Incident with ID: {} not found", id);
            return ResponseEntity.notFound().build();
        }
    }

    /**
     * POST /incidents - Create new incident
     * Automatically calls AI service asynchronously for analysis
     * @param incidentDTO incident data
     * @return created incident with 201 status
     */
    @PostMapping
    public ResponseEntity<Incident> createIncident(@RequestBody IncidentDTO incidentDTO) {
        log.info("POST /incidents - Creating new incident: {}", incidentDTO.getTitle());

        if (incidentDTO.getTitle() == null || incidentDTO.getTitle().isEmpty()) {
            log.warn("Invalid incident data: title is required");
            return ResponseEntity.badRequest().build();
        }

        Incident createdIncident = incidentService.createIncident(incidentDTO);
        log.info("Incident created with ID: {}. AI analysis will be processed asynchronously.", createdIncident.getId());

        return ResponseEntity.status(HttpStatus.CREATED).body(createdIncident);
    }

    /**
     * PUT /incidents/{id} - Update incident
     * @param id incident ID
     * @param incidentDTO updated incident data
     * @return updated incident if found, 404 otherwise
     */
    @PutMapping("/{id}")
    public ResponseEntity<Incident> updateIncident(@PathVariable Long id, @RequestBody IncidentDTO incidentDTO) {
        log.info("PUT /incidents/{} - Updating incident", id);

        Incident updatedIncident = incidentService.updateIncident(id, incidentDTO);
        if (updatedIncident != null) {
            return ResponseEntity.ok(updatedIncident);
        } else {
            log.warn("Incident with ID: {} not found for update", id);
            return ResponseEntity.notFound().build();
        }
    }

    /**
     * DELETE /incidents/{id} - Delete incident
     * @param id incident ID
     * @return 204 No Content if successful, 404 if not found
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteIncident(@PathVariable Long id) {
        log.info("DELETE /incidents/{} - Deleting incident", id);

        if (incidentService.deleteIncident(id)) {
            return ResponseEntity.noContent().build();
        } else {
            log.warn("Incident with ID: {} not found for deletion", id);
            return ResponseEntity.notFound().build();
        }
    }

}

