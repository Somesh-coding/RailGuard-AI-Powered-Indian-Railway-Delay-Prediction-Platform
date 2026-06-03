package com.railguard.controller;

import com.railguard.dto.TrainSearchRequest;
import com.railguard.service.TrainService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/trains")
public class TrainController {

    private final TrainService trainService;

    public TrainController(TrainService trainService) {
        this.trainService = trainService;
    }

    @GetMapping("/health")
    public Object health() {
        return java.util.Map.of("status", "RailGuard backend is running");
    }

    @PostMapping("/search")
    public Object search(@RequestBody TrainSearchRequest request) {
        return trainService.searchTrains(request);
    }
}
