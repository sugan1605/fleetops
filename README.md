# FleetOps

**A hands-on cloud engineering project focused on building, containerising and deploying a Python-based fleet management API.**

FleetOps is a fleet management system inspired by operational workflows in the vehicle rental industry. The project provides a practical environment for developing backend engineering, cloud infrastructure and automation skills.

The goal is to build a working application and progressively take responsibility for the infrastructure, deployment, security and operations behind it.

## Project Goals

- Build and maintain a Python REST API.
- Work with PostgreSQL and database integration.
- Develop reliable testing and code-quality practices.
- Containerise the application with Docker.
- Build CI/CD workflows using GitHub Actions.
- Provision and manage cloud infrastructure using AWS and Terraform.
- Develop practical Linux, networking and troubleshooting skills.
- Understand monitoring, security and operational practices.

## Technology Stack

| Area | Technologies |
|---|---|
| Backend | Python, REST API |
| Database | PostgreSQL |
| Testing | pytest |
| Code quality | Ruff |
| Containers | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | AWS |
| Infrastructure as Code | Terraform (planned) |
| Operating systems | Linux, Ubuntu |
| Version control | Git, GitHub |

## Engineering & DevOps

### Application Development

- Python-based REST API.
- PostgreSQL integration.
- Structured application architecture.
- Automated tests with pytest.
- Code quality checks using Ruff.

### Containers

- Dockerised application.
- Docker Compose for local multi-container development.
- Container networking and environment configuration.
- Troubleshooting container and database connectivity.

### Continuous Integration

GitHub Actions is used to automate the CI workflow.

Current CI responsibilities:
- Run automated tests.
- Run Ruff checks.
- Build the Docker image.

### Linux & Homelab

A Linux environment is used for practical exercises involving:

- Linux operations and command-line tools.
- SSH access and remote administration.
- Application execution and troubleshooting.
- Networking and service connectivity.

## AWS Cloud Engineering

AWS is the primary cloud platform for the next stage of FleetOps.

The objective is to understand the infrastructure behind a cloud-hosted application rather than simply deploy it and move on.

### AWS work completed

Initial networking and security exploration in the Stockholm region (`eu-north-1`).

- Inspected VPC architecture and IPv4 CIDR ranges.
- Explored subnets across multiple Availability Zones.
- Examined route tables and Internet Gateway routing.
- Learned how local routes enable communication within a VPC.
- Created dedicated security groups for the planned application architecture:

| Security Group | Inbound access |
|---|---|
| `fleetops-alb-sg` | HTTPS — TCP 443 from `0.0.0.0/0` |
| `fleetops-api-sg` | TCP 8000 from the ALB security group |
| `fleetops-db-sg` | PostgreSQL — TCP 5432 from the API security group |

These security groups currently exist in the default VPC. They are not yet attached to deployed application or database resources.

### Planned AWS architecture

The next phase is to build a dedicated VPC for FleetOps and progressively deploy the application.

Planned components:

- Dedicated VPC with public and private subnets.
- Internet Gateway and route tables.
- Purpose-specific security groups.
- AWS Identity and Access Management (IAM).
- Amazon Elastic Container Registry (ECR).
- Amazon ECS with Fargate.
- PostgreSQL database deployment.
- CloudWatch monitoring and logging.
- Terraform for infrastructure provisioning.
- GitHub Actions deployment workflow using AWS OIDC authentication.

Kubernetes and Amazon EKS are later learning goals, once the fundamentals of cloud infrastructure and container orchestration are established.

## Current Project Focus

The current focus is **AWS Cloud Engineering**.

The development path is:

1. AWS networking and security fundamentals.
2. Dedicated VPC architecture.
3. Terraform and Infrastructure as Code.
4. Container deployment using Amazon ECS and Fargate.
5. PostgreSQL connectivity and application configuration.
6. GitHub Actions CI/CD deployment.
7. Monitoring, logging and security.
8. Further exploration of Kubernetes and EKS.

## How I Work

FleetOps is developed incrementally, with an emphasis on understanding the reasoning behind technical decisions.

- Build and test before expanding functionality.
- Keep changes small and focused.
- Document important implementation decisions.
- Investigate and troubleshoot problems rather than simply applying workarounds.
- Use GitHub issues and a Kanban board to track progress.
- Keep documentation aligned with the actual state of the project.

## Objective

FleetOps is intended to become a practical portfolio project demonstrating the ability to build an application, understand its infrastructure, automate its deployment and troubleshoot it in a cloud environment.

The long-term goal is to develop the skills required for Cloud Engineering, DevOps and Platform Engineering roles.