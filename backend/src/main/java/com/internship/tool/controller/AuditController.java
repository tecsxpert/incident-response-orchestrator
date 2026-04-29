package com.internship.tool.controller;

import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.access.prepost.PreAuthorize;

import java.util.List;

@RestController
@RequestMapping("/audit")
public class AuditController {

    private final AuditLogRepository repo;

    public AuditController(AuditLogRepository repo) {
        this.repo = repo;
    }

    @GetMapping
    @PreAuthorize("hasRole('ADMIN')")
    public List<AuditLog> getLogs() {
        return repo.findAll();
    }
}