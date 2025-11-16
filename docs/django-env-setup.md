# Django Container Environment Setup

Use these instructions when you package the chatbot container together with your Django application. The goal is to make sure the container receives a `PROJECT_ID` value so the backend only retrieves content for that project.

## 1. Decide how you will supply the project id

- **Static value:** hard-code the project id in your infrastructure pipeline or Docker build command.
- **Dynamic value:** read the project id from an environment variable that your pipeline sets (for example `DJANGO_PROJECT_ID`).

## 2. Pass the project id into the container build

Add a build argument to your `Dockerfile` (or the docker build command) so the project id is available while the image is assembled.

```dockerfile
# Dockerfile
ARG PROJECT_ID
ARG PROJECT_FIELD=project_id
ENV PROJECT_ID=${PROJECT_ID}
ENV PROJECT_FIELD=${PROJECT_FIELD}
```

When building the image, provide the value:

```bash
docker build \
  --build-arg PROJECT_ID=my-django-project \
  --build-arg PROJECT_FIELD=project_id \
  -t django-chatbot:latest .
```

If the value should come from another environment variable, you can pass it straight through:

```bash
docker build \
  --build-arg PROJECT_ID=${DJANGO_PROJECT_ID} \
  --build-arg PROJECT_FIELD=${DJANGO_PROJECT_FIELD:-project_id} \
  -t django-chatbot:latest .
```

## 3. Persist the project id in the chatbot `.env`

The chatbot reads configuration from `/usr/src/app/.env`. Ensure the build injects the project id into that file. You can template the `.env` before copying it into the image, or append the value as part of the build:

```dockerfile
# After copying your base .env into the image
RUN echo "PROJECT_ID=${PROJECT_ID}" >> /usr/src/app/.env

# Optional: override PROJECT_FIELD if Django uses a different metadata name
RUN if [ -n "${PROJECT_FIELD}" ]; then \
      echo "PROJECT_FIELD=${PROJECT_FIELD}" >> /usr/src/app/.env ; \
    fi
```

If your pipeline stores secrets (like API keys) separately, keep those in your deployment platform so you do not commit secrets into source control. Only add `PROJECT_ID`/`PROJECT_FIELD` during the build.

## 4. Surface the project id at runtime (optional)

If the same image is used for multiple environments, override the value at runtime with the platform’s environment settings:

```bash
docker run --env PROJECT_ID=contoso-prod django-chatbot:latest
```

App Service, AKS, and container orchestrators expose similar configuration screens—set `PROJECT_ID`/`PROJECT_FIELD` there so the container picks them up on startup.

## 5. Test inside the Django deployment

After building the image:

1. Run the container locally and confirm `/usr/src/app/.env` contains the `PROJECT_ID` line.
2. Trigger a chat query and ensure the backend response only returns documents with the matching project metadata.

With the project id in place, the chatbot will only surface data associated with that project, keeping each Django tenant isolated.
