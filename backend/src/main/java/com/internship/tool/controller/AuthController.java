package com.internship.tool.controller;

import com.internship.tool.entity.User;
import com.internship.tool.repository.UserRepository;
import com.internship.tool.security.JwtUtil;
import com.internship.tool.service.AuditService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final AuditService auditService;

    public AuthController(UserRepository userRepository,
                          BCryptPasswordEncoder passwordEncoder,
                          JwtUtil jwtUtil,
                          AuditService auditService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
        this.auditService = auditService;
    }

    // ✅ REGISTER
    @PostMapping("/register")
    public String register(@RequestBody User user) {

        if (userRepository.findByUsername(user.getUsername()).isPresent()) {
            return "Username already exists";
        }

        // 🔥 FIX: ensure role is set
        if (user.getRole() == null || user.getRole().isBlank()) {
            user.setRole("VIEWER"); // default role
        }

        user.setPassword(passwordEncoder.encode(user.getPassword()));
        userRepository.save(user);

        auditService.log("REGISTER", user.getUsername());

        return "User registered successfully";
    }

    // ✅ LOGIN
    @PostMapping("/login")
    public Map<String, String> login(@RequestBody User user) {

        User dbUser = userRepository.findByUsername(user.getUsername())
                .orElseThrow(() -> new RuntimeException("User not found"));

        if (!passwordEncoder.matches(user.getPassword(), dbUser.getPassword())) {
            throw new RuntimeException("Invalid password");
        }

        // 🔥 FIX: validate role
        if (dbUser.getRole() == null || dbUser.getRole().isBlank()) {
            throw new RuntimeException("User role is missing in DB");
        }

        String token = jwtUtil.generateToken(
                dbUser.getUsername(),
                dbUser.getRole()
        );

        auditService.log("LOGIN", dbUser.getUsername());

        return Map.of("token", token);
    }
}