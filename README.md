# EventHive – Automated Event Registration & Ticketing System

EventHive is a complete full-stack cloud-native web application designed for learning and demonstrating DevOps workflows including containerization, continuous integration, infrastructure as code, and configuration management.

## 📁 Project Structure

```text
eventhive/
├── app/                  # Flask Backend Application
│   ├── __init__.py      # App factory & DB initialization
│   ├── routes.py        # Application endpoints (/add, /book)
│   ├── models.py        # SQLite Database schema for 'Event'
│   └── database.py      # SQLAlchemy DB instance layer
├── templates/            # Frontend HTML Views
│   └── index.html       # Main UI constructed with Bootstrap
├── static/               # Frontend Assets
│   └── styles.css       # Custom styling overrides
├── tests/                # Unit Tests
│   └── test_app.py      # Basic pytest suite for Flask app
├── k8s/                  # Kubernetes Configuration
│   ├── deployment.yaml  # Defines our replica set of pods
│   └── service.yaml     # Exposes our pods to external traffic
├── terraform/            # Infrastructure as Code (AWS setup)
│   ├── main.tf          # Core infrastructure, EC2 and Security Groups
│   └── variables.tf     # Configurable variables for Terraform
├── ansible/              # Configuration Management
│   ├── inventory.ini    # List of target servers
│   └── playbook.yml     # Actions to install Docker & K8s
├── Dockerfile            # Blueprint for Python application image
├── requirements.txt      # Python dependencies
├── app.py                # Main entrypoint to start Flask locally
├── Jenkinsfile           # CI/CD Pipeline configuration
└── README.md             # Project documentation
```

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9+
- Git

### Steps
1. **Clone & Navigate**
   ```bash
   git clone <repo-url>
   cd eventhive
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Application**
   ```bash
   python app.py
   ```
4. **Access UI**
   Open your browser and navigate to `http://localhost:5000`

## 🐳 How to Run via Docker

1. **Build the image**
   ```bash
   docker build -t eventhive:latest .
   ```
2. **Run the container**
   ```bash
   docker run -p 5000:5000 eventhive:latest
   ```

## ☁️ How to Deploy (DevOps Pipeline)

### Infrastructure Setup (Terraform)
Navigate to `terraform/`, initialize, and plan/apply to spin up your AWS EC2 instance:
```bash
cd terraform
terraform init
terraform apply
```

### Server Configuration (Ansible)
1. Add the outputted EC2 IP address from Terraform to `ansible/inventory.ini`.
2. Run the Ansible playbook to install Docker and Kubernetes dependencies on the running EC2 instance:
```bash
cd ansible
ansible-playbook -i inventory.ini playbook.yml
```

### CI/CD Deployment (Jenkins)
Our `Jenkinsfile` outlines a 5-step pipeline:
1. Checkouts codebase.
2. Builds `eventhive:latest` Docker image.
3. Runs pytest `tests/test_app.py` in container.
4. Pushes successfully tested image to DockerHub.
5. Deploys updated image using `k8s/deployment.yaml` and `k8s/service.yaml`.

### Testing (JMeter Load Test)
- Download and open Apache JMeter.
- Create a 'Thread Group' simulating 100+ virtual users.
- Add an HTTP Request Default hitting your NodePort or EC2 public IP.
- Add HTTP Requests for `GET /` and `POST /book/1`.
- View results in a 'View Results Tree' and 'Summary Report' listener.
