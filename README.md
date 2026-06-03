# RailGuard - No Login Version

Simplified deployment architecture:

Frontend React -> Spring Boot Backend -> Python FastAPI ML Service

No MongoDB. No login. No JWT.

## Run backend

```bash
cd backend
mvn spring-boot:run
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

## Frontend image

Put your homepage train image here:

```txt
frontend/public/images/train.jpg
```

## Deployment

Frontend: Vercel
Backend: Render
ML Service: Render
