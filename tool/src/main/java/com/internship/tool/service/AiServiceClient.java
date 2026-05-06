package com.internship.tool.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

/**
 * Talks to the Flask AI service.
 *
 * Base URL comes from ai.service.url in application.yml (default
 * http://localhost:5000). Every call is wrapped in try/catch so an AI
 * outage doesn't bubble up as a 5xx — the caller just gets null and
 * decides what to do.
 */
@Component
public class AiServiceClient {

    private static final Logger log = LoggerFactory.getLogger(AiServiceClient.class);

    private final RestTemplate restTemplate;
    private final String aiServiceUrl;

    public AiServiceClient(RestTemplateBuilder builder,
                           @Value("${ai.service.url:http://localhost:5000}") String aiServiceUrl) {
        // 10s connect + read timeout
        this.restTemplate = builder
                .connectTimeout(Duration.ofSeconds(10))
                .readTimeout(Duration.ofSeconds(10))
                .build();
        this.aiServiceUrl = aiServiceUrl;
    }

    public Map<String, Object> describe(String text) {
        return post("/describe", Map.of("input", text));
    }

    public Map<String, Object> recommend(String text) {
        return post("/recommend", Map.of("input", text));
    }

    public Map<String, Object> categorise(String text) {
        return post("/categorise", Map.of("input", text));
    }

    public Map<String, Object> generateReport(String text) {
        return post("/generate-report", Map.of("input", text));
    }

    public Map<String, Object> query(String question) {
        return post("/query", Map.of("question", question));
    }

    public Map<String, Object> health() {
        try {
            ResponseEntity<Map> resp = restTemplate.getForEntity(aiServiceUrl + "/health", Map.class);
            return safeBody(resp);
        } catch (Exception ex) {
            log.warn("AI /health call failed: {}", ex.getMessage());
            return null;
        }
    }

    private Map<String, Object> post(String path, Map<String, Object> body) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);

            ResponseEntity<Map> resp = restTemplate.postForEntity(aiServiceUrl + path, entity, Map.class);
            return safeBody(resp);
        } catch (Exception ex) {
            log.warn("AI {} call failed: {}", path, ex.getMessage());
            return null;
        }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> safeBody(ResponseEntity<Map> resp) {
        if (resp == null || resp.getBody() == null) {
            return new HashMap<>();
        }
        return (Map<String, Object>) resp.getBody();
    }
}
