package com.internship.tool.repository;
import org.springframework.data.repository.query.Param;
import java.util.UUID;
import com.internship.tool.entity.Incident;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface IncidentRepository extends JpaRepository<Incident, UUID> {
    
    @Query("SELECT i FROM Incident i WHERE i.status = :status")
    List<Incident> findByStatus(String status);

    
    @Query("SELECT i FROM Incident i WHERE LOWER(i.title) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<Incident> searchByTitle(String keyword);

    
    @Query("SELECT i FROM Incident i WHERE i.createdAt BETWEEN :start AND :end")
    List<Incident> findByDateRange(LocalDateTime start, LocalDateTime end);

    @Query("SELECT i FROM Incident i WHERE i.title LIKE %:q% OR i.description LIKE %:q%")
    List<Incident> search(@Param("q") String q);

}