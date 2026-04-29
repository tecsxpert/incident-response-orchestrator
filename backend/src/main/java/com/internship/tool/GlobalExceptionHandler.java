package com.internship.tool;

import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public String handleException(Exception ex) {
        ex.printStackTrace(); // shows error in terminal
        return ex.getMessage(); // shows error in Postman/Thunder
    }
}