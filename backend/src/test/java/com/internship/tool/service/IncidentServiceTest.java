package com.internship.tool.service;

import com.internship.tool.client.AiServiceClient;
import com.internship.tool.dto.IncidentDTO;
import com.internship.tool.entity.Incident;
import com.internship.tool.repository.IncidentRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@SpringBootTest
@ActiveProfiles("test")
public class IncidentServiceTest {

    private IncidentService incidentService;

    @Mock
    private IncidentRepository incidentRepository;

    @Mock
    private AiServiceClient aiServiceClient;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        incidentService = new IncidentService();
        incidentService.incidentRepository = incidentRepository;
        incidentService.aiServiceClient = aiServiceClient;
    }

    @Test
    void testCreateIncident_Success() {
        // Arrange
        IncidentDTO incidentDTO = IncidentDTO.builder()
                .title("Test Ransomware Attack")
                .description("A ransomware attack detected on server")
                .severity("critical")
                .incidentType("ransomware")
                .status("OPEN")
                .build();

        Incident savedIncident = Incident.builder()
                .id(1L)
                .title(incidentDTO.getTitle())
                .description(incidentDTO.getDescription())
                .severity(incidentDTO.getSeverity())
                .incidentType(incidentDTO.getIncidentType())
                .status("OPEN")
                .build();

        when(incidentRepository.save(any(Incident.class))).thenReturn(savedIncident);
        when(aiServiceClient.isServiceAvailable()).thenReturn(true);

        // Act
        Incident result = incidentService.createIncident(incidentDTO);

        // Assert
        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals("Test Ransomware Attack", result.getTitle());
        assertEquals("critical", result.getSeverity());
        verify(incidentRepository, times(1)).save(any(Incident.class));
    }

    @Test
    void testCreateIncident_WithoutTitle_ShouldHandleGracefully() {
        // Arrange
        IncidentDTO incidentDTO = IncidentDTO.builder()
                .description("A test incident")
                .severity("high")
                .incidentType("malware")
                .build();

        // Act & Assert
        assertThrows(NullPointerException.class, () -> {
            incidentService.createIncident(incidentDTO);
        });
    }

    @Test
    void testCallAiServiceAsync_WhenServiceAvailable() {
        // Arrange
        Incident incident = Incident.builder()
                .id(1L)
                .title("Test Incident")
                .description("Test Description")
                .severity("high")
                .incidentType("malware")
                .build();

        String aiResponse = "{\"status\": \"success\", \"analysis\": \"Test analysis result\"}";

        when(aiServiceClient.isServiceAvailable()).thenReturn(true);
        when(aiServiceClient.analyzeIncident(anyString(), anyString(), anyString(), anyString()))
                .thenReturn(aiResponse);
        when(aiServiceClient.extractAnalysisFromResponse(aiResponse))
                .thenReturn("Test analysis result");
        when(incidentRepository.save(any(Incident.class))).thenReturn(incident);

        // Act
        incidentService.callAiServiceAsync(incident);

        // Assert - Give time for async processing
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        verify(aiServiceClient, times(1)).isServiceAvailable();
        verify(aiServiceClient, times(1)).analyzeIncident(anyString(), anyString(), anyString(), anyString());
    }

    @Test
    void testCallAiServiceAsync_WhenServiceUnavailable() {
        // Arrange
        Incident incident = Incident.builder()
                .id(1L)
                .title("Test Incident")
                .description("Test Description")
                .severity("high")
                .incidentType("malware")
                .build();

        when(aiServiceClient.isServiceAvailable()).thenReturn(false);

        // Act
        incidentService.callAiServiceAsync(incident);

        // Assert - Give time for async processing
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        verify(aiServiceClient, times(1)).isServiceAvailable();
        verify(aiServiceClient, never()).analyzeIncident(anyString(), anyString(), anyString(), anyString());
    }

    @Test
    void testUpdateIncident_Success() {
        // Arrange
        Long id = 1L;
        IncidentDTO incidentDTO = IncidentDTO.builder()
                .title("Updated Title")
                .status("CLOSED")
                .build();

        Incident existingIncident = Incident.builder()
                .id(id)
                .title("Original Title")
                .status("OPEN")
                .build();

        Incident updatedIncident = Incident.builder()
                .id(id)
                .title("Updated Title")
                .status("CLOSED")
                .build();

        when(incidentRepository.findById(id)).thenReturn(java.util.Optional.of(existingIncident));
        when(incidentRepository.save(any(Incident.class))).thenReturn(updatedIncident);

        // Act
        Incident result = incidentService.updateIncident(id, incidentDTO);

        // Assert
        assertNotNull(result);
        assertEquals("Updated Title", result.getTitle());
        assertEquals("CLOSED", result.getStatus());
        verify(incidentRepository, times(1)).save(any(Incident.class));
    }

    @Test
    void testDeleteIncident_Success() {
        // Arrange
        Long id = 1L;
        when(incidentRepository.existsById(id)).thenReturn(true);

        // Act
        boolean result = incidentService.deleteIncident(id);

        // Assert
        assertTrue(result);
        verify(incidentRepository, times(1)).deleteById(id);
    }

    @Test
    void testDeleteIncident_NotFound() {
        // Arrange
        Long id = 999L;
        when(incidentRepository.existsById(id)).thenReturn(false);

        // Act
        boolean result = incidentService.deleteIncident(id);

        // Assert
        assertFalse(result);
        verify(incidentRepository, never()).deleteById(id);
    }
}
