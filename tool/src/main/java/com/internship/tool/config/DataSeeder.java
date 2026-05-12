package com.internship.tool.config;

import com.internship.tool.entity.Incident;
import com.internship.tool.repository.IncidentRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

@Configuration
public class DataSeeder {

    @Bean
    CommandLineRunner initDatabase(IncidentRepository repository) {
        return args -> {
            // Check if we need to seed (keeping your <= 1 logic to force the first run)
            if (repository.count() <= 100) {
                System.out.println("🌱 Seeding 30 records with realistic statuses and score ranges...");

                Random random = new Random();
                List<String> titles = Arrays.asList(
                        "Network Outage", "Database Connection Failure", "API Latency",
                        "UI Scaling Issue", "Memory Leak Detected", "Login Timeout",
                        "Unauthorized Access Attempt", "Cloud Storage Limit Reached"
                );
                List<String> statuses = Arrays.asList("OPEN", "IN_PROGRESS", "CLOSED");
                List<String> priorities = Arrays.asList("LOW", "MEDIUM", "HIGH", "CRITICAL");

                for (int i = 1; i <= 30; i++) {
                    Incident incident = new Incident();

                    // Pick a random priority first so we can determine a realistic score
                    String priority = priorities.get(random.nextInt(priorities.size()));

                    incident.setTitle(titles.get(random.nextInt(titles.size())) + " #" + i);
                    incident.setDescription("Automated Day 14 demo report for incident #" + i);
                    incident.setStatus(statuses.get(random.nextInt(statuses.size())));
                    incident.setPriority(priority);

                    // --- REALISTIC SCORE GENERATION ---
                    // Logic: Score depends on Priority + some random variance
                    int baseScore = switch (priority) {
                        case "CRITICAL" -> 85; // Scores 85-100
                        case "HIGH"     -> 60; // Scores 60-84
                        case "MEDIUM"   -> 30; // Scores 30-59
                        default         -> 5;  // LOW: Scores 5-29
                    };

                    int finalScore = baseScore + random.nextInt(15);
                    incident.setScore(finalScore);

                    repository.save(incident);
                }
                System.out.println("✅ Day 14 Seeding Complete! 30 records with distributed scores added.");
            } else {
                System.out.println("✨ Database already populated. Skipping seeder.");
            }
        };
    }
}