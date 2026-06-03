package com.railguard.service;

import com.railguard.dto.TrainSearchRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;

@Service
public class TrainService {

    private final WebClient webClient;

    @Value("${ml.service.url}")
    private String mlServiceUrl;

    public TrainService() {
        this.webClient = WebClient.builder().build();
    }

    public Object searchTrains(TrainSearchRequest request) {
        return webClient.post()
                .uri(mlServiceUrl + "/search-trains")
                .bodyValue(Map.of(
                        "source", request.source,
                        "destination", request.destination,
                        "weather", request.weather,
                        "dayOfWeek", request.dayOfWeek,
                        "timeOfDay", request.timeOfDay,
                        "routeCongestion", request.routeCongestion
                ))
                .retrieve()
                .bodyToMono(Object.class)
                .block();
    }
}
