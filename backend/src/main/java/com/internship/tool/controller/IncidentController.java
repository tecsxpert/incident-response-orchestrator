package com.internship.tool.controller;

import com.internship.tool.entity.Incident;
import com.internship.tool.repository.IncidentRepository;
import org.springframework.data.domain.*;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpServletResponse;
import java.io.PrintWriter;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/incidents")
public class IncidentController {

    private final IncidentRepository repository;

    public IncidentController(IncidentRepository repository) {
        this.repository = repository;
    }

    // PAGINATION + SORTING
    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER','VIEWER')")
    public Page<Incident> getAll(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "5") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String sortDir
    ) {

        Sort sort = sortDir.equalsIgnoreCase("desc") ?
                Sort.by(sortBy).descending() :
                Sort.by(sortBy).ascending();

        Pageable pageable = PageRequest.of(page, size, sort);

        return repository.findAll(pageable);
    }

    //  CREATE
    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public Incident create(@RequestBody Incident incident) {
        return repository.save(incident);
    }

    // UPDATE
    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public Incident update(@PathVariable UUID id, @RequestBody Incident updated) {

        Incident incident = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Not found"));

        incident.setTitle(updated.getTitle());
        incident.setDescription(updated.getDescription());
        incident.setStatus(updated.getStatus());
        incident.setPriority(updated.getPriority());
        incident.setAssignedTo(updated.getAssignedTo());

        return repository.save(incident);
    }

    // DELETE
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public String delete(@PathVariable UUID id) {
        repository.deleteById(id);
        return "Deleted";
    }

    // CSV EXPORT
    @GetMapping("/export")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public void exportCSV(HttpServletResponse response) throws Exception {

        response.setContentType("text/csv");
        response.setHeader("Content-Disposition", "attachment; filename=incidents.csv");

        List<Incident> incidents = repository.findAll();

        PrintWriter writer = response.getWriter();

        // Header
        writer.println("ID,Title,Description,Status,Priority,AssignedTo");

        // Data
        for (Incident i : incidents) {
            writer.println(
                    i.getId() + "," +
                    i.getTitle() + "," +
                    i.getDescription() + "," +
                    i.getStatus() + "," +
                    i.getPriority() + "," +
                    i.getAssignedTo()
            );
        }

        writer.flush();
        writer.close();
    }
}