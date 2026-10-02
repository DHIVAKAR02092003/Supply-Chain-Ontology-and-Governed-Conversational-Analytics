-- =====================================================
-- SPCS Setup for Supply Chain Analytics Dashboard
-- =====================================================

-- 1. Create image repository
CREATE IMAGE REPOSITORY IF NOT EXISTS SCM_ANALYTICS.PERSONA.SCM_IMAGES;

-- 2. Create compute pool
CREATE COMPUTE POOL IF NOT EXISTS SCM_ANALYTICS_POOL
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_RESUME = TRUE
  AUTO_SUSPEND_SECS = 300;

-- 3. Create network rule for external access (if needed)
CREATE OR REPLACE NETWORK RULE scm_egress_rule
  TYPE = HOST_PORT
  MODE = EGRESS
  VALUE_LIST = ('0.0.0.0:443', '0.0.0.0:80');

-- 4. Create external access integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION scm_external_access
  ALLOWED_NETWORK_RULES = (scm_egress_rule)
  ENABLED = TRUE;

-- 5. Create the service
CREATE SERVICE IF NOT EXISTS SCM_ANALYTICS.PERSONA.SCM_DASHBOARD_SERVICE
  IN COMPUTE POOL SCM_ANALYTICS_POOL
  FROM SPECIFICATION $$
spec:
  containers:
    - name: backend
      image: /SCM_ANALYTICS/PERSONA/SCM_IMAGES/scm-backend:latest
      env:
        SNOWFLAKE_ACCOUNT: <your_account>
        SNOWFLAKE_USER: <your_user>
        SNOWFLAKE_PASSWORD: <your_password>
        SNOWFLAKE_ROLE: ACCOUNTADMIN
        SNOWFLAKE_WAREHOUSE: COMPUTE_WH
        SNOWFLAKE_DATABASE: SCM_ANALYTICS
        SNOWFLAKE_SCHEMA: PERSONA
        CORS_ORIGINS: "*"
      resources:
        requests:
          cpu: 0.5
          memory: 1Gi
        limits:
          cpu: 1
          memory: 2Gi
      ports:
        - port: 8000
          protocol: TCP
    - name: frontend
      image: /SCM_ANALYTICS/PERSONA/SCM_IMAGES/scm-frontend:latest
      resources:
        requests:
          cpu: 0.25
          memory: 256Mi
        limits:
          cpu: 0.5
          memory: 512Mi
      ports:
        - port: 80
          protocol: TCP
  endpoints:
    - name: app
      port: 80
      public: true
    - name: api
      port: 8000
      public: true
$$
  MIN_INSTANCES = 1
  MAX_INSTANCES = 1
  EXTERNAL_ACCESS_INTEGRATIONS = (scm_external_access);

-- 6. Check service status
CALL SYSTEM$GET_SERVICE_STATUS('SCM_ANALYTICS.PERSONA.SCM_DASHBOARD_SERVICE');

-- 7. Get service endpoint URLs
SHOW ENDPOINTS IN SERVICE SCM_ANALYTICS.PERSONA.SCM_DASHBOARD_SERVICE;
