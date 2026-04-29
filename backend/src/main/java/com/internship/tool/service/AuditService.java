package com.internship.tool.service;

import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class AuditService {

    private final AuditLogRepository repo;

    public AuditService(AuditLogRepository repo) {
        this.repo = repo;
    }

    public void log(String action, String username) {
        AuditLog log = new AuditLog();
        log.setAction(action);
        log.setUsername(username);
        log.setTimestamp(LocalDateTime.now());
        repo.save(log);
    }
}
