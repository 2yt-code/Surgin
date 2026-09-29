# <center>Surgin<center>
## A powerful web-based music streaming platform

# Guidline
- [Surgin](#surgin)
  - [A powerful web-based music streaming platform](#a-powerful-web-based-music-streaming-platform)
- [Guidline](#guidline)
- [Goal](#goal)
- [Demo](#demo)
- [Introduction](#introduction)
  - [Core Areas](#core-areas)
- [Structure](#structure)
- [Database shema](#database-shema)
- [Flow diagram](#flow-diagram)
- [Setup](#setup)
  - [dev](#dev)
    - [mock data](#mock-data)
    - [test](#test)
- [Stage](#stage)
- [Production](#production)
  - [setup](#setup-1)
  - [monitoring](#monitoring)
  - [asset](#asset)
- [Tasks](#tasks)

# Goal
The goal of Surgin is to build a secure, scalable, and maintainable backend for a modern music platform, providing efficient music discovery, search, and personalized experiences

# Demo
soon

# Introduction
Surgin is a backend-focused music platform designed to provide a scalable and structured foundation for music discovery, content management, authentication, and personalized user experiences

The project is built with Django and Django REST Framework (DRF) and follows a modular architecture to keep the system maintainable, extensible, and suitable for future growth

Surgin provides a RESTful API for managing and discovering music content, including songs, artists, albums, search, filtering, and exploration features. The platform also includes a modern authentication system based on JWT, with additional device and fingerprint signals to strengthen session security and account protection

The Explore system is designed around multiple content sources such as popular, latest, most-liked, and most-played songs, providing a foundation that can later evolve into a more advanced recommendation and personalization system

The project also emphasizes software engineering practices such as API documentation, testing, database design, Git-based development workflows, and performance-aware query design

## Core Areas
- Authentication & Security — JWT-based authentication with device and fingerprint verification
- Music Management — Songs, artists, albums, media files, and related metadata
- Explore & Search — Advanced search, filtering, sorting, and discovery mechanisms
- API Architecture — Structured REST APIs built with Django REST Framework
- Documentation — OpenAPI documentation powered by drf-spectacular
- Scalability — Query optimization, pagination, caching, and an architecture prepared for future recommendation features

Surgin is designed not only as a music API, but as a practical backend architecture that can evolve from a conventional content platform into a personalized music discovery system


# Structure
```
├───apps
│   ├───api
│   │   ├───v1
│   │   │   ├───account
│   │   │   │   ├───migrations
│   │   │   │   ├───serializers
│   │   │   │   ├───tests
│   │   │   │   ├───urls
│   │   │   │   └───views
│   │   │   ├───core
│   │   │   │   ├───album
│   │   │   │   │   ├───migrations
│   │   │   │   │   ├───serializers
│   │   │   │   │   ├───urls
│   │   │   │   │   └───views
│   │   │   │   ├───artist
│   │   │   │   │   ├───migrations 
│   │   │   │   │   ├───serializers
│   │   │   │   │   ├───urls
│   │   │   │   │   └───views
│   │   │   │   ├───playlist
│   │   │   │   │   ├───migrations
│   │   │   │   │   ├───serializers
│   │   │   │   │   ├───urls
│   │   │   │   │   └───views
│   │   │   │   ├───song
│   │   │   │   │   ├───migrations
│   │   │   │   │   ├───serializers
│   │   │   │   │   ├───urls
│   │   │   │   │   └───views
│   │   │   │   ├───track
│   │   │   │   │   ├───migrations
│   │   │   │   │   ├───serializers
│   │   │   │   │   ├───urls
│   │   │   │   │   └───views
├───config
│   └───envs
├───docs
├───requirements
└───utils
```
**config/envs:** default for various development environments 

# Database shema
![database-shema](docs/database-shema.png)

# Flow diagram
![flow-diagram](docs/flow-diagram.png)

# Setup
soon

## dev

### mock data

### test

# Stage

environments sample

# Production
soon

## setup
## monitoring
## asset

# Tasks
soon
