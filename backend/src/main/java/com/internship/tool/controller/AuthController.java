package com.internship.tool.controller;

import com.internship.tool.entity.User;
import com.internship.tool.repository.UserRepository;
import com.internship.tool.security.JwtUtil;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder encoder;
    private final JwtUtil jwtUtil;

    public AuthController(UserRepository userRepository,
                          BCryptPasswordEncoder encoder,
                          JwtUtil jwtUtil) {
        this.userRepository = userRepository;
        this.encoder = encoder;
        this.jwtUtil = jwtUtil;
    }

    // ✅ REGISTER
    @PostMapping("/register")
    public String register(@RequestBody User user) {

        if (userRepository.findByUsername(user.getUsername()).isPresent()) {
            return "User already exists";
        }

        user.setPassword(encoder.encode(user.getPassword()));
        user.setRole("VIEWER");

        userRepository.save(user);

        return "User registered successfully";
    }

    // ✅ LOGIN → RETURN TOKEN
    @PostMapping("/login")
    public Map<String, String> login(@RequestBody User user) {

        User existingUser = userRepository.findByUsername(user.getUsername())
                .orElseThrow(() -> new RuntimeException("User not found"));

        if (encoder.matches(user.getPassword(), existingUser.getPassword())) {

            String token = jwtUtil.generateToken(user.getUsername());

            return Map.of("token", token);

        } else {
            throw new RuntimeException("Invalid password");
        }
    }

    // ✅ REFRESH TOKEN
    @PostMapping("/refresh")
    public Map<String, String> refresh(@RequestHeader("Authorization") String authHeader) {

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            throw new RuntimeException("Invalid token");
        }

        String oldToken = authHeader.substring(7);

        String username = jwtUtil.extractUsername(oldToken);

        String newToken = jwtUtil.generateToken(username);

        return Map.of("token", newToken);
    }
}