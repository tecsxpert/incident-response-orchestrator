package com.internship.tool.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class IncidentDTO {

    private Long id;
    private String title;
    private String description;
    private String status;
    private String severity;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

}
