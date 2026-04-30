package com.internship.tool.aop;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class AuditAspect {

    private final AuditLogRepository auditRepository;
    private final ObjectMapper mapper = new ObjectMapper();

    public AuditAspect(AuditLogRepository auditRepository) {
        this.auditRepository = auditRepository;
    }

    // ✅ TARGET ONLY IncidentService (clean & safe)
    @Around("execution(* com.internship.tool.service.IncidentService.*(..))")
    public Object logAudit(ProceedingJoinPoint joinPoint) throws Throwable {

        Object[] args = joinPoint.getArgs();

        // ✅ SAFE USERNAME
        String username = "SYSTEM";

        if (SecurityContextHolder.getContext().getAuthentication() != null &&
            SecurityContextHolder.getContext().getAuthentication().isAuthenticated() &&
            !"anonymousUser".equals(SecurityContextHolder.getContext().getAuthentication().getName())) {

            username = SecurityContextHolder.getContext().getAuthentication().getName();
        }

        String action = joinPoint.getSignature().getName();

        String oldData = null;
        String newData = null;

        // ✅ CAPTURE INPUT (new data)
        try {
            if (args.length > 0) {
                newData = mapper.writeValueAsString(args[0]);
            }
        } catch (Exception e) {
            newData = "error converting newData";
        }

        // 🔁 EXECUTE METHOD
        Object result = joinPoint.proceed();

        // ✅ CAPTURE RESULT (old/final state)
        try {
            if (result != null && !(result instanceof String)) {
                oldData = mapper.writeValueAsString(result);
            }
        } catch (Exception e) {
            oldData = "error converting oldData";
        }

        // ❗ ONLY SAVE FOR CREATE/UPDATE/DELETE
        if (action.equalsIgnoreCase("create") ||
            action.equalsIgnoreCase("update") ||
            action.equalsIgnoreCase("delete")) {

            AuditLog log = new AuditLog();
            log.setAction(action);
            log.setUsername(username);
            log.setOldData(oldData);
            log.setNewData(newData);

            auditRepository.save(log);
        }

        return result;
    }
}