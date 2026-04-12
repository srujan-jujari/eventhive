# DevOps Pipeline Implementation for EventHive

This plan outlines the final steps to fully implement an end-to-end DevOps pipeline for the EventHive project, fulfilling all constraints for AWS infrastructure, containerization, orchestration, config management, CI/CD, and testing.

## Proposed Changes

### Docker & Python Testing
- **`tests/test_app.py`**: [NEW] Create basic integration/unit tests using `pytest` to test the Flask application (Home page and Login routes).
- **`requirements.txt`**: [MODIFY] Add `pytest` and `pytest-flask` to allow Jenkins to run the basic tests.
- **`Dockerfile`**: No major changes needed; already uses best practices and runs on `0.0.0.0:5000`.

---
### Infrastructure as Code (Terraform)
- **`terraform/main.tf` & `terraform/variables.tf`**: No major changes needed. Standard AWS provider config, Security Group already allows ports 22, 80, 5000, and Kubernetes node ports (30000-32767), and provisions a `t2.medium` EC2 instance.

---
### Configuration Management (Ansible)
- **`ansible/playbook.yml`**: [MODIFY] Upgrade to ensure an idempotent installation of Docker, `kubeadm`, `kubelet`, and `kubectl`. Add steps to initialize the Kubernetes cluster on the single node using `kubeadm init`, deploy a Pod network (like Calico or Flannel), and remove the taint from the master node so that pods can be scheduled directly on it.

---
### Orchestration (Kubernetes)
- **`k8s/deployment.yaml`**: [MODIFY] Adjust if needed to ensure 2 replicas and proper container port 5000 exposing, ensuring high availability.
- **`k8s/service.yaml`**: [MODIFY] Change from `LoadBalancer` to `NodePort` mapping port 80 or 5000 to the container. `NodePort` is simpler and more effective for a standalone EC2 instance. 

---
### CI/CD Pipeline (Jenkins)
- **`Jenkinsfile`**: [MODIFY] Refine the existing declarative pipeline to clearly demonstrate the build -> test -> push -> deploy lifecycle. Validate it uses correct variables.

---
### Documentation (README.md)
- **`README.md`**: [MODIFY] Thoroughly update to document the entire DevOps workflow:
  - Architecture overview.
  - Setup instructions (Local, Docker, and Cloud/AWS Pipeline).
  - Folder structure explanation.
  - Instructions for Apache JMeter load performance testing.

## User Review Required
> [!IMPORTANT]
> - Do you have a preferred Pod Network (CNI) for the `kubeadm` single-node cluster (e.g. Flannel or Calico)? If none is specified, I will default to Flannel for its simplicity.
> - For JMeter Load Testing, since this is a mini project, I'll explain how to simulate user load on the Book Ticket endpoint. Please confirm if this is sufficient.

## Verification Plan
### Automated Tests
- The Jenkins pipeline will automatically run `pytest test/` in the build image to ensure application health before pushing.
### Manual Verification
- Review resulting files and verify they conform to standard DevOps best practices and syntax.
