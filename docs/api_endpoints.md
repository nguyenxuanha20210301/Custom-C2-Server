# API Endpoints – SCSF

PREFIX = /api/v1

## Agents
POST /agents/register  
GET  /agents/{id}/tasks  
POST /agents/{id}/heartbeat  
PUT  /agents/{id}/upload  

## Tasks
POST /tasks  
GET  /tasks  
POST /tasks/{id}/cancel  

## Auth
POST /auth/login

## System
GET /health  
GET /metrics  
