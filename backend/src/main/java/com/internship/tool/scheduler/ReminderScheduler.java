package com.internship.tool.scheduler;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ReminderScheduler {

    // TODO: Implement scheduled reminder jobs
    @Scheduled(fixedDelay = 60000)
    public void sendReminders() {
        // Scheduled logic here
    }

}
