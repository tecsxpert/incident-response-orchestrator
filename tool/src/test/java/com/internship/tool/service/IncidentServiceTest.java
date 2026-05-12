package com.internship.tool.service;

import com.internship.tool.entity.Incident;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.repository.IncidentRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.*;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class IncidentServiceTest {

    @Mock
    private IncidentRepository incidentRepository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private IncidentService incidentService;

    private Incident testIncident;

    @BeforeEach
    void setUp() {
        testIncident = new Incident();
        testIncident.setId(1L);
        testIncident.setTitle("Server Downtime");
        testIncident.setStatus("OPEN");
    }

    // --- createIncident() Tests ---

    @Test
    @DisplayName("1. Create Incident: Happy Path - Should set default status and send email")
    void createIncident_Success() {
        testIncident.setStatus(null); // Test default status logic
        when(incidentRepository.save(any(Incident.class))).thenReturn(testIncident);

        Incident saved = incidentService.createIncident(testIncident);

        assertNotNull(saved);
        assertEquals("OPEN", saved.getStatus());
        verify(emailService, times(1)).sendIncidentCreatedEmail(any(), any(), any());
        verify(incidentRepository).save(testIncident);
    }

    @Test
    @DisplayName("2. Create Incident: Fail - Empty title should throw exception")
    void createIncident_EmptyTitle_ThrowsException() {
        testIncident.setTitle("");

        assertThrows(IllegalArgumentException.class, () -> incidentService.createIncident(testIncident));
        verify(incidentRepository, never()).save(any());
    }

    // --- updateIncident() Tests ---

    @Test
    @DisplayName("3. Update Incident: Happy Path - Should save without sending email")
    void updateIncident_Success() {
        when(incidentRepository.save(any(Incident.class))).thenReturn(testIncident);

        Incident updated = incidentService.updateIncident(testIncident);

        assertNotNull(updated);
        verify(emailService, never()).sendIncidentCreatedEmail(any(), any(), any());
        verify(incidentRepository).save(testIncident);
    }

    // --- getIncidentById() Tests ---

    @Test
    @DisplayName("4. Get Incident By ID: Happy Path")
    void getIncidentById_Success() {
        when(incidentRepository.findById(1L)).thenReturn(Optional.of(testIncident));

        Incident found = incidentService.getIncidentById(1L);

        assertEquals(1L, found.getId());
        assertEquals("Server Downtime", found.getTitle());
    }

    @Test
    @DisplayName("5. Get Incident By ID: Fail - Invalid ID should throw ResourceNotFound")
    void getIncidentById_NotFound_ThrowsException() {
        when(incidentRepository.findById(99L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> incidentService.getIncidentById(99L));
    }

    // --- getAllIncidents() Tests ---

    @Test
    @DisplayName("6. Get All Incidents: Happy Path - Verify pagination")
    void getAllIncidents_Success() {
        Pageable pageable = PageRequest.of(0, 5);
        Page<Incident> page = new PageImpl<>(List.of(testIncident));
        when(incidentRepository.findAll(pageable)).thenReturn(page);

        Page<Incident> result = incidentService.getAllIncidents(pageable);

        assertEquals(1, result.getTotalElements());
        assertEquals("Server Downtime", result.getContent().get(0).getTitle());
    }

    @Test
    @DisplayName("7. Get All Incidents: Empty list should return empty page")
    void getAllIncidents_Empty() {
        Pageable pageable = PageRequest.of(0, 5);
        when(incidentRepository.findAll(pageable)).thenReturn(Page.empty());

        Page<Incident> result = incidentService.getAllIncidents(pageable);

        assertTrue(result.isEmpty());
    }

    // --- Cache and Interaction Verification ---

    @Test
    @DisplayName("8. Create Incident: Verify Repository Interaction Count")
    void createIncident_VerifyInteraction() {
        when(incidentRepository.save(any())).thenReturn(testIncident);
        incidentService.createIncident(testIncident);
        verify(incidentRepository, atLeastOnce()).save(any());
    }

    @Test
    @DisplayName("9. Update Incident: Verify attachment path preservation")
    void updateIncident_AttachmentCheck() {
        testIncident.setAttachmentPath("uuid_file.jpg");
        when(incidentRepository.save(any())).thenReturn(testIncident);

        Incident result = incidentService.updateIncident(testIncident);

        assertEquals("uuid_file.jpg", result.getAttachmentPath());
    }

    @Test
    @DisplayName("10. Service Initialization: Ensure mocks are injected")
    void service_MockInjectionCheck() {
        assertNotNull(incidentService);
        // This confirms @InjectMocks worked
    }
}