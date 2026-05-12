package com.internship.tool.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "Data Transfer Object for user authentication requests")
public class AuthRequest {

    @Schema(description = "The unique username of the user", example = "admin", requiredMode = Schema.RequiredMode.REQUIRED)
    private String username;

    @Schema(description = "The secret password associated with the account", example = "password123", requiredMode = Schema.RequiredMode.REQUIRED)
    private String password;
}