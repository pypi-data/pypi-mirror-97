deployment = """
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: easier-serving
  name: pod-easier-serving
spec:
  replicas: 1
  selector:
    matchLabels:
      app: easier-serving
  template:
    metadata:
      labels:
        app: easier-serving
  containers:
  - name: easier-serving
    image: easierai/easier_model:1.0
    imagePullPolicy: Always
    ports:
    - containerPort: 5000
    envFrom:
      - configMapRef:
          name: easier-serving
  restartPolicy: Always
  # imagePullSecrets:
  # - name: regcred
"""