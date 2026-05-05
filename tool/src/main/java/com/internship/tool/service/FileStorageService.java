package com.internship.tool.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

@Service
public class FileStorageService {

    private final String UPLOAD_DIR = "incident_attachments/";
    // Define allowed types in a list for cleaner validation
    private final List<String> ALLOWED_TYPES = Arrays.asList("image/png", "image/jpeg", "application/pdf");

    public FileStorageService() {
        try {
            Path path = Paths.get(UPLOAD_DIR);
            if (!Files.exists(path)) {
                Files.createDirectories(path);
            }
        } catch (IOException e) {
            System.err.println("Could not create directory: " + e.getMessage());
        }
    }

    public String storeFile(MultipartFile file) throws IOException {
        // 1. Polished Validation using equalsIgnoreCase logic
        String contentType = file.getContentType();

        boolean isSupported = false;
        if (contentType != null) {
            for (String type : ALLOWED_TYPES) {
                if (type.equalsIgnoreCase(contentType)) {
                    isSupported = true;
                    break;
                }
            }
        }

        if (!isSupported) {
            throw new IllegalArgumentException("Only PNG, JPEG, and PDF files are allowed!");
        }

        // 2. Existing UUID logic for unique storage
        String fileName = UUID.randomUUID().toString() + "_" +
                file.getOriginalFilename().replaceAll("[^a-zA-Z0-9.\\-]", "_");

        Path targetLocation = Paths.get(UPLOAD_DIR).resolve(fileName);
        Files.copy(file.getInputStream(), targetLocation, StandardCopyOption.REPLACE_EXISTING);

        return fileName;
    }
}