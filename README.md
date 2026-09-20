# 🚀 Spring Cloud Gateway with Redis Rate Limiter

[![Java](https://img.shields.io/badge/Java-17-orange.svg)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.5-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Spring Cloud](https://img.shields.io/badge/Spring%20Cloud-2023.0.0-blue.svg)](https://spring.io/projects/spring-cloud)
[![Redis](https://img.shields.io/badge/Redis-Alpine-red.svg)](https://redis.io/)

A high-performance, reactive API Gateway built using **Spring Boot 3.2.5** and **Spring Cloud Gateway**. This project implements the **Token Bucket Algorithm** backed by **Redis** to control traffic flow, handle bursts, and prevent abuse or overloading of downstream services.

---

## 🏗️ Architecture & Flow

```text
[ Client / Python Script ] 
       │
       ▼ (HTTP: 8080)
┌────────────────────────────────────────────────────────┐
│              Spring Cloud Gateway                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │ IP KeyResolver (Identifies client unique address)│  │
│  └──────────────────────┬───────────────────────────┘  │
│                         ▼                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Redis Token-Bucket Rate Limiter (Port 6379)    │  │
│  └──────┬───────────────────────────────────┬──────┘  │
│         │ (Allowed)                         │ (Exceeded)
│         ▼                                   ▼         │
│   [ Forward to ]                    [ Return 429 ]    │
│   [https://httpbin.org](https://httpbin.org)             Too Many Requests   │
└────────────────────────────────────────────────────────┘





####
application.yml

server:
  port: 8080

spring:
  cloud:
    gateway:
      routes:
        - id: protected_api_route
          uri: [https://httpbin.org](https://httpbin.org)
          predicates:
            - Path=/api/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 2   # 2 tokens added per second
                redis-rate-limiter.burstCapacity: 5   # Max 5 requests per burst window
                redis-rate-limiter.requestedTokens: 1 # Cost of 1 token per request
                key-resolver: "#{@userKeyResolver}"   # Rate limit tracked per client IP





Java 17 installed locally.

Docker Desktop running for the Redis backend.

Python 3 with the requests library installed (pip install requests).




To create redis container === docker-compose up -d
To run spring application === mvn spring-boot:run
To run and test rate limiter  === python3 test_limiter.py
