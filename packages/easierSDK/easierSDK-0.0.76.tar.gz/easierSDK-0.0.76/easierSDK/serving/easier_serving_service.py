service = """
apiVersion: v1
kind: Service
metadata:
  name: service-easier-serving
  labels:
    app: easier-serving
spec:
  type: NodePort
  # type: LoadBalancer
  ports:
  - name: "5000"
    port: 5000
    targetPort: 5000
  selector:
    app: easier-serving
"""