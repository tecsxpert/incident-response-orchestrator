package com.internship.tool.client;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@Component
public class AiServiceClient {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    @Value("${ai.service.base-url:http://localhost:5000}")
    private String aiServiceBaseUrl;

    public AiServiceClient() {
        this.restTemplate = new RestTemplate();
        this.objectMapper = new ObjectMapper();
    }

    /**
     * Analyzes an incident using the AI service
     * @param title incident title
     * @param description incident description
     * @param severity incident severity
     * @param incidentType type of incident
     * @return AI analysis result or null if service unavailable
     */
    public String analyzeIncident(String title, String description, String severity, String incidentType) {
        try {
            String url = aiServiceBaseUrl + "/api/describe";

            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("title", title);
            requestBody.put("description", description);
            requestBody.put("severity", severity);
            requestBody.put("incident_type", incidentType);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

            ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                log.info("AI service analysis completed successfully for incident: {}", title);
                return response.getBody();
            } else {
                log.warn("AI service returned non-success status: {} for incident: {}", response.getStatusCode(), title);
                return null;
            }
        } catch (RestClientException e) {
            log.error("Failed to connect to AI service at {}: {}", aiServiceBaseUrl, e.getMessage());
            return null;
        } catch (Exception e) {
            log.error("Unexpected error calling AI service: {}", e.getMessage(), e);
            return null;
        }
    }

    /**
     * Generates a structured report using the AI service
     * @param title incident title
     * @param description incident description
     * @param severity incident severity
     * @param incidentType type of incident
     * @return Report JSON or null if service unavailable
     */
    public String generateReport(String title, String description, String severity, String incidentType) {
        try {
            String url = aiServiceBaseUrl + "/api/describe/generate-report";

            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("title", title);
            requestBody.put("description", description);
            requestBody.put("severity", severity);
            requestBody.put("incident_type", incidentType);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

            ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                log.info("AI service report generation completed successfully for incident: {}", title);
                return response.getBody();
            } else {
                log.warn("AI service returned non-success status: {} for report generation of: {}", response.getStatusCode(), title);
                return null;
            }
        } catch (RestClientException e) {
            log.error("Failed to connect to AI service at {}: {}", aiServiceBaseUrl, e.getMessage());
            return null;
        } catch (Exception e) {
            log.error("Unexpected error calling AI service for report: {}", e.getMessage(), e);
            return null;
        }
    }

    /**
     * Checks if AI service is available
     * @return true if service is reachable, false otherwise
     */
    public boolean isServiceAvailable() {
        try {
            String url = aiServiceBaseUrl + "/health";
            ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
            boolean available = response.getStatusCode().is2xxSuccessful();
            if (available) {
                log.debug("AI service is available");
            } else {
                log.warn("AI service health check returned status: {}", response.getStatusCode());
            }
            return available;
        } catch (RestClientException e) {
            log.warn("AI service health check failed: {}", e.getMessage());
            return false;
        } catch (Exception e) {
            log.error("Unexpected error during AI service health check: {}", e.getMessage());
            return false;
        }
    }

    /**
     * Extracts the analysis text from AI service response
     * @param aiResponse JSON response from AI service
     * @return extracted analysis or null if parsing fails
     */
    public String extractAnalysisFromResponse(String aiResponse) {
        try {
            JsonNode rootNode = objectMapper.readTree(aiResponse);
            if (rootNode.has("analysis")) {
                return rootNode.get("analysis").asText();
            } else if (rootNode.has("report")) {
                return objectMapper.writeValueAsString(rootNode.get("report"));
            }
            return aiResponse;
        } catch (Exception e) {
            log.warn("Failed to extract analysis from AI response: {}", e.getMessage());
            return aiResponse;
        }
    }
}
