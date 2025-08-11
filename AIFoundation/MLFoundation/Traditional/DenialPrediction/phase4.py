# Phase 4: Complete Deployment Configuration
# Kubernetes, Docker, and Infrastructure as Code

# 1. Docker Configuration
---
# Dockerfile for ML API Service
FROM python:3.9-slim

LABEL maintainer="healthcare-ml-team"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "120", "src.api.main:app"]

---
# 2. Kubernetes Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: healthcare-ml
  labels:
    name: healthcare-ml
    compliance: hipaa
    environment: production

---
# 3. ConfigMap for Application Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: ml-api-config
  namespace: healthcare-ml
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  MLFLOW_TRACKING_URI: "http://mlflow-server:5000"
  FEAST_REPO_PATH: "/app/feast"
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"
  MODEL_NAME: "denial_predictor"
  PREDICTION_TIMEOUT: "30"
  BATCH_SIZE: "1000"
  ENABLE_MODEL_MONITORING: "true"
  DRIFT_CHECK_INTERVAL: "3600"
  PERFORMANCE_THRESHOLD: "0.8"

---
# 4. Secret for Sensitive Configuration
apiVersion: v1
kind: Secret
metadata:
  name: ml-api-secrets
  namespace: healthcare-ml
type: Opaque
data:
  DATABASE_URL: <base64-encoded-db-url>
  REDIS_PASSWORD: <base64-encoded-redis-password>
  MLFLOW_TRACKING_USERNAME: <base64-encoded-username>
  MLFLOW_TRACKING_PASSWORD: <base64-encoded-password>
  ENCRYPTION_KEY: <base64-encoded-encryption-key>
  JWT_SECRET: <base64-encoded-jwt-secret>

---
# 5. Deployment for ML API Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api-deployment
  namespace: healthcare-ml
  labels:
    app: ml-api
    version: v1.0.0
    tier: api
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: ml-api
  template:
    metadata:
      labels:
        app: ml-api
        version: v1.0.0
        tier: api
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: ml-api
        image: your-registry/healthcare-ml-api:v1.0.0
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        envFrom:
        - configMapRef:
            name: ml-api-config
        - secretRef:
            name: ml-api-secrets
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
            ephemeral-storage: "2Gi"
          limits:
            memory: "2Gi"
            cpu: "1000m"
            ephemeral-storage: "4Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        volumeMounts:
        - name: model-cache
          mountPath: /app/models
        - name: logs
          mountPath: /app/logs
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
      - name: model-sync
        image: your-registry/model-sync:v1.0.0
        imagePullPolicy: Always
        env:
        - name: MLFLOW_TRACKING_URI
          valueFrom:
            configMapKeyRef:
              name: ml-api-config
              key: MLFLOW_TRACKING_URI
        - name: MODEL_NAME
          valueFrom:
            configMapKeyRef:
              name: ml-api-config
              key: MODEL_NAME
        volumeMounts:
        - name: model-cache
          mountPath: /app/models
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
      volumes:
      - name: model-cache
        emptyDir:
          sizeLimit: 5Gi
      - name: logs
        emptyDir:
          sizeLimit: 1Gi
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - ml-api
              topologyKey: kubernetes.io/hostname

---
# 6. Service for ML API
apiVersion: v1
kind: Service
metadata:
  name: ml-api-service
  namespace: healthcare-ml
  labels:
    app: ml-api
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
  selector:
    app: ml-api

---
# 7. Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-api-hpa
  namespace: healthcare-ml
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-api-deployment
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: custom_api_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 120
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 25
        periodSeconds: 60

---
# 8. Ingress for External Access
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ml-api-ingress
  namespace: healthcare-ml
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "120"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "120"
spec:
  tls:
  - hosts:
    - api.healthcare-ml.company.com
    secretName: ml-api-tls
  rules:
  - host: api.healthcare-ml.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ml-api-service
            port:
              number: 80

---
# 9. Network Policy for Security
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ml-api-network-policy
  namespace: healthcare-ml
spec:
  podSelector:
    matchLabels:
      app: ml-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - podSelector:
        matchLabels:
          app: monitoring
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
  - to:
    - podSelector:
        matchLabels:
          app: mlflow
    ports:
    - protocol: TCP
      port: 5000
  - to: []
    ports:
    - protocol: TCP
      port: 443
    - protocol: UDP
      port: 53

---
# 10. Redis Deployment for Caching
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
  namespace: healthcare-ml
  labels:
    app: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        volumeMounts:
        - name: redis-storage
          mountPath: /data
        args:
        - redis-server
        - --appendonly
        - "yes"
        - --requirepass
        - $(REDIS_PASSWORD)
        env:
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: ml-api-secrets
              key: REDIS_PASSWORD
      volumes:
      - name: redis-storage
        persistentVolumeClaim:
          claimName: redis-pvc

---
# 11. Redis Service
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: healthcare-ml
spec:
  selector:
    app: redis
  ports:
  - protocol: TCP
    port: 6379
    targetPort: 6379

---
# 12. Redis Persistent Volume Claim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: healthcare-ml
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd

---
# 13. MLflow Server Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-deployment
  namespace: healthcare-ml
  labels:
    app: mlflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mlflow
  template:
    metadata:
      labels:
        app: mlflow
    spec:
      containers:
      - name: mlflow
        image: your-registry/mlflow-server:latest
        ports:
        - containerPort: 5000
        env:
        - name: MLFLOW_BACKEND_STORE_URI
          value: "postgresql://user:password@postgres-service:5432/mlflow"
        - name: MLFLOW_DEFAULT_ARTIFACT_ROOT
          value: "s3://mlflow-artifacts-bucket"
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: ml-api-secrets
              key: AWS_ACCESS_KEY_ID
        - name: AWS_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: ml-api-secrets
              key: AWS_SECRET_ACCESS_KEY
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: mlflow-storage
          mountPath: /mlflow
      volumes:
      - name: mlflow-storage
        persistentVolumeClaim:
          claimName: mlflow-pvc

---
# 14. MLflow Service
apiVersion: v1
kind: Service
metadata:
  name: mlflow-service
  namespace: healthcare-ml
spec:
  selector:
    app: mlflow
  ports:
  - protocol: TCP
    port: 5000
    targetPort: 5000

---
# 15. MLflow PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mlflow-pvc
  namespace: healthcare-ml
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
  storageClassName: standard

---
# 16. Pod Disruption Budget
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ml-api-pdb
  namespace: healthcare-ml
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: ml-api

---
# 17. Monitoring: ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ml-api-monitor
  namespace: healthcare-ml
  labels:
    app: ml-api
spec:
  selector:
    matchLabels:
      app: ml-api
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
    scrapeTimeout: 10s

---
# 18. Security: Pod Security Policy
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: healthcare-ml-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'

---
# 19. RBAC: Service Account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ml-api-service-account
  namespace: healthcare-ml

---
# 20. RBAC: Role
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: healthcare-ml
  name: ml-api-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch"]

---
# 21. RBAC: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ml-api-rolebinding
  namespace: healthcare-ml
subjects:
- kind: ServiceAccount
  name: ml-api-service-account
  namespace: healthcare-ml
roleRef:
  kind: Role
  name: ml-api-role
  apiGroup: rbac.authorization.k8s.io

---
# 22. Backup CronJob for Model Artifacts
apiVersion: batch/v1
kind: CronJob
metadata:
  name: model-backup
  namespace: healthcare-ml
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: your-registry/backup-tool:latest
            env:
            - name: BACKUP_DESTINATION
              value: "s3://ml-model-backups"
            - name: SOURCE_PATH
              value: "/mlflow"
            command:
            - /bin/sh
            - -c
            - |
              echo "Starting model backup..."
              aws s3 sync /mlflow s3://ml-model-backups/$(date +%Y%m%d) --delete
              echo "Backup completed"
            volumeMounts:
            - name: mlflow-storage
              mountPath: /mlflow
              readOnly: true
          volumes:
          - name: mlflow-storage
            persistentVolumeClaim:
              claimName: mlflow-pvc
          restartPolicy: OnFailure

---
# 23. Init Container for Database Migration
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  namespace: healthcare-ml
spec:
  template:
    spec:
      initContainers:
      - name: db-migration
        image: your-registry/db-migration:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ml-api-secrets
              key: DATABASE_URL
        command:
        - /bin/sh
        - -c
        - |
          echo "Running database migrations..."
          alembic upgrade head
          echo "Migrations completed"
      containers:
      - name: placeholder
        image: busybox
        command: ["echo", "Migration job completed"]
      restartPolicy: Never

---
# 24. Kustomization for Environment Management
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

metadata:
  name: healthcare-ml-production

resources:
- namespace.yaml
- configmap.yaml
- secret.yaml
- deployment.yaml
- service.yaml
- ingress.yaml
- hpa.yaml
- pdb.yaml
- rbac.yaml
- monitoring.yaml

patchesStrategicMerge:
- production-patches.yaml

images:
- name: your-registry/healthcare-ml-api
  newTag: v1.0.0

configMapGenerator:
- name: ml-api-config
  behavior: merge
  literals:
  - ENVIRONMENT=production
  - REPLICAS=3
  - PERFORMANCE_THRESHOLD=0.85

secretGenerator:
- name: ml-api-secrets
  behavior: merge
  files:
  - DATABASE_URL=secrets/database-url
  - REDIS_PASSWORD=secrets/redis-password
