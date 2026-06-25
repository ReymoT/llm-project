# OpenServe: Kubernetes-Native LLM Inference Platform

![CI](https://github.com/ReymoT/openserve/actions/workflows/ci.yml/badge.svg)

Production-grade LLM inference platform that serves open-source language models through multiple inference backends behind a unified OpenAI-compatible API.

OpenServe focuses on **LLM inference systems engineering** rather than model training, emphasizing backend routing, operational reliability, observability, deployment automation, and production infrastructure.

The platform provides a FastAPI gateway that routes requests to multiple inference backends beginning with vLLM and later Triton Inference Server. It is designed to be deployed on Kubernetes using GitOps workflows with Terraform and Argo CD while exposing production grade metrics for benchmarking and monitoring.



# Features

## Inference Gateway

- OpenAI-compatible Chat Completions API
- FastAPI gateway
- Request validation with Pydantic
- API key authentication
- Rate limiting
- Streaming responses
- Request timeout handling

## Backend Layer

- Backend abstraction interface
- Health-aware routing layer
- vLLM backend integration
- Backend health checking

## Observability

- Prometheus metrics endpoint
- Request latency metrics
- Request counters

## Deployment

- Docker Compose local deployment



# Planned Features

## Multi-Backend Serving

- Triton Inference Server integration
- Health-based failover
- Weighted backend routing
- Backend benchmarking
- Multi-model routing

## Kubernetes

- Separate Gateway, vLLM, and Triton deployments
- GPU scheduling
- Horizontal Pod Autoscaler
- Readiness and liveness probes
- Persistent model cache

## Infrastructure

- Terraform infrastructure provisioning
- Argo CD GitOps deployment
- Development, staging, and production environments
- Canary deployments
- Rollback demonstrations

## Observability

- Grafana dashboards
- GPU utilization
- VRAM usage
- Tokens per second
- Time to First Token (TTFT)
- Backend comparison dashboards

## Benchmarking

Compare inference backends using:

- Throughput
- Tokens/sec
- Time to First Token
- p50 latency
- p95 latency
- p99 latency
- Concurrent request scalability
- Failure behavior under overload


# Architecture

```text
                    Client Applications
                           │
                           ▼
            OpenAI-Compatible REST API
                           │
                           ▼
                  FastAPI Gateway
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Authentication   Rate Limiting   Validation
                           │
                           ▼
                   Backend Router
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
       vLLM Backend                 Triton Backend
            │                             │
            └──────────────┬──────────────┘
                           ▼
                 Open Source LLM Models
```


# Tech Stack

### Backend

- FastAPI
- Pydantic
- HTTPX
- Python

### LLM Serving

- vLLM
- Triton Inference Server *(planned)*

### Infrastructure

- Docker
- Kubernetes *(planned)*
- Terraform *(planned)*
- Argo CD *(planned)*

### Observability

- Prometheus
- Grafana *(planned)*

### Benchmarking

- Custom benchmarking suite
- Prometheus metrics
- Load testing


# Roadmap

## Gateway

- [x] OpenAI-compatible API
- [x] API key authentication
- [x] Request validation
- [x] Rate limiting
- [x] Streaming responses
- [x] Request timeout handling

## Backend

- [x] Backend abstraction
- [x] Backend routing
- [x] Health checking
- [x] vLLM integration
- [ ] Triton integration
- [ ] Health-based failover
- [ ] Weighted routing
- [ ] Multi-model routing

## Observability

- [x] Prometheus metrics
- [ ] Backend metrics
- [ ] GPU metrics
- [ ] Grafana dashboards

## Infrastructure

- [ ] Kubernetes deployment
- [ ] Terraform infrastructure
- [ ] Argo CD GitOps
- [ ] Canary deployments
- [ ] Rollback demonstrations

## Benchmarking

- [ ] Throughput benchmarking
- [ ] Latency benchmarking
- [ ] TTFT benchmarking
- [ ] Tokens/sec benchmarking
- [ ] Backend comparison reports



# Motivation

Modern LLM applications require significantly more than exposing a model through an API. Production inference platforms must support multiple serving backends, provide operational visibility, maintain predictable latency under load, and enable reliable deployments.

OpenServe explores the engineering challenges involved in building a production-ready LLM inference platform with modern infrastructure, observability, and deployment practices.



# License

MIT License