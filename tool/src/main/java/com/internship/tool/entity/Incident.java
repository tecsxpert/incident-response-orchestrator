package com.internship.tool.entity;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.io.Serializable;
import java.time.LocalDateTime;

@Entity
@Table(name = "incidents")
@EntityListeners(AuditingEntityListener.class)
@Schema(description = "Represents a security or technical incident within the system")
public class Incident implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Schema(description = "Unique identifier of the incident", example = "1")
    private Long id;

    @Schema(description = "Path to the uploaded attachment related to the incident", example = "/uploads/error_log.txt")
    private String attachmentPath;

    @Column(name = "title", nullable = false)
    @Schema(description = "Short descriptive title", example = "Database Connection Failure", requiredMode = Schema.RequiredMode.REQUIRED)
    private String title;

    @Column(name = "description", columnDefinition = "TEXT")
    @Schema(description = "Detailed explanation of the incident", example = "The primary database stopped responding to queries at 02:00 AM.")
    private String description;

    @Column(name = "status")
    @Schema(description = "Current state of the incident", example = "OPEN", allowableValues = {"OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"})
    private String status;

    @Column(name = "priority")
    @Schema(description = "Urgency level of the incident", example = "HIGH", allowableValues = {"LOW", "MEDIUM", "HIGH", "CRITICAL"})
    private String priority;

    // --- DAY 14 ADDITION: SCORE FIELD ---
    @Column(name = "score")
    @Schema(description = "Calculated risk score of the incident", example = "85")
    private Integer score;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    @Schema(description = "Timestamp when the incident was reported", example = "2026-05-07T12:00:00")
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    @Schema(description = "Timestamp of the last update to the incident", example = "2026-05-07T14:30:00")
    private LocalDateTime updatedAt;

    // --- GETTERS AND SETTERS ---

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getAttachmentPath() { return attachmentPath; }
    public void setAttachmentPath(String attachmentPath) { this.attachmentPath = attachmentPath; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getPriority() { return priority; }
    public void setPriority(String priority) { this.priority = priority; }

    // DAY 14: Score Getter and Setter
    public Integer getScore() { return score; }
    public void setScore(Integer score) { this.score = score; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}