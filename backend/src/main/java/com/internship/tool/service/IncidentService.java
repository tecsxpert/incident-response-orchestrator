package com.internship.tool.service;

import com.internship.tool.client.AiServiceClient;
import com.internship.tool.dto.IncidentDTO;
import com.internship.tool.entity.Incident;
import com.internship.tool.repository.IncidentRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@Transactional
public class IncidentService {

    @Autowired
    private IncidentRepository incidentRepository;

    @Autowired
    private AiServiceClient aiServiceClient;

    /**
     * Creates a new incident and asynchronously calls AI service for analysis
     * @param incidentDTO incident data
     * @return saved incident (without AI analysis, which is populated asynchronously)
     */
    public Incident createIncident(IncidentDTO incidentDTO) {
        log.info("Creating new incident: {}", incidentDTO.getTitle());

        Incident incident = Incident.builder()
                .title(incidentDTO.getTitle())
                .description(incidentDTO.getDescription())
                .status(incidentDTO.getStatus() != null ? incidentDTO.getStatus() : "OPEN")
                .severity(incidentDTO.getSeverity())
                .incidentType(incidentDTO.getIncidentType())
                .build();

        Incident savedIncident = incidentRepository.save(incident);
        log.info("Incident created with ID: {}", savedIncident.getId());

        // Asynchronously call AI service for analysis
        callAiServiceAsync(savedIncident);

        return savedIncident;
    }

    /**
     * Asynchronously calls AI service to analyze the incident
     * Handles null responses gracefully and logs any failures
     * @param incident the incident to analyze
     */
    @Async
    public void callAiServiceAsync(Incident incident) {
        try {
            log.info("Starting async AI analysis for incident ID: {}", incident.getId());

            // Check if AI service is available
            if (!aiServiceClient.isServiceAvailable()) {
                log.warn("AI service is unavailable for incident ID: {}", incident.getId());
                return;
            }

            // Call AI service for analysis
            String analysisResponse = aiServiceClient.analyzeIncident(
                    incident.getTitle(),
                    incident.getDescription(),
                    incident.getSeverity(),
                    incident.getIncidentType()
            );

            if (analysisResponse != null && !analysisResponse.isEmpty()) {
                // Extract analysis text from response
                String analysis = aiServiceClient.extractAnalysisFromResponse(analysisResponse);

                // Update incident with AI analysis
                incident.setAiAnalysis(analysis);
                incidentRepository.save(incident);

                log.info("AI analysis completed and stored for incident ID: {}", incident.getId());
            } else {
                log.warn("AI service returned null or empty response for incident ID: {}", incident.getId());
            }

        } catch (Exception e) {
            log.error("Error during async AI analysis for incident ID: {}", incident.getId(), e);
            // Gracefully handle failure - incident is already created
        }
    }

    /**
     * Retrieves all incidents
     * @return list of all incidents
     */
    public List<Incident> getAllIncidents() {
        log.debug("Fetching all incidents");
        return incidentRepository.findAll();
    }

    /**
     * Retrieves an incident by ID
     * @param id incident ID
     * @return incident if found, empty optional otherwise
     */
    public Optional<Incident> getIncidentById(Long id) {
        log.debug("Fetching incident by ID: {}", id);
        return incidentRepository.findById(id);
    }

    /**
     * Updates an existing incident
     * @param id incident ID
     * @param incidentDTO updated incident data
     * @return updated incident or null if not found
     */
    public Incident updateIncident(Long id, IncidentDTO incidentDTO) {
        log.info("Updating incident ID: {}", id);

        Optional<Incident> existingIncident = incidentRepository.findById(id);
        if (existingIncident.isPresent()) {
            Incident incident = existingIncident.get();
            if (incidentDTO.getTitle() != null) {
                incident.setTitle(incidentDTO.getTitle());
            }
            if (incidentDTO.getDescription() != null) {
                incident.setDescription(incidentDTO.getDescription());
            }
            if (incidentDTO.getStatus() != null) {
                incident.setStatus(incidentDTO.getStatus());
            }
            if (incidentDTO.getSeverity() != null) {
                incident.setSeverity(incidentDTO.getSeverity());
            }
            if (incidentDTO.getIncidentType() != null) {
                incident.setIncidentType(incidentDTO.getIncidentType());
            }

            Incident updatedIncident = incidentRepository.save(incident);
            log.info("Incident ID: {} updated successfully", id);
            return updatedIncident;
        } else {
            log.warn("Incident ID: {} not found for update", id);
            return null;
        }
    }

    /**
     * Deletes an incident
     * @param id incident ID
     * @return true if deletion successful, false if not found
     */
    public boolean deleteIncident(Long id) {
        log.info("Deleting incident ID: {}", id);

        if (incidentRepository.existsById(id)) {
            incidentRepository.deleteById(id);
            log.info("Incident ID: {} deleted successfully", id);
            return true;
        } else {
            log.warn("Incident ID: {} not found for deletion", id);
            return false;
        }
    }

}

