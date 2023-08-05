ingress = """
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: ingress-easier-serving
  kubernetes.io/ingress.allow-http: "true"
  nginx.ingress.kubernetes.io/backend-protocol: HTTP
  nginx.ingress.kubernetes.io/secure-backends: "false"
  labels:
    app: easier-serving
spec:
  tls:
  - secretName: wildcard-easier-ai.eu
  rules:
  - host: easier-ai.eu
    http:
      paths:
      - backend:
          serviceName: service-easier-serving
          servicePort: 5000
"""