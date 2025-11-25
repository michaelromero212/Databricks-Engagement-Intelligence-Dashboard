import json
import random
import os
from datetime import datetime, timedelta

# Constants
OUTPUT_DIR = "data/raw"
OUTPUT_FILE = "engagements_sample.json"
NUM_RECORDS = 500

CUSTOMERS = [
    "FinTech Corp", "HealthPlus", "RetailGiant", "AutoMotive Inc", "EduTech Solutions",
    "Global Logistics", "MediaStream", "GreenEnergy", "CyberSecure", "DataDriven Co"
]

TECHNOLOGIES = [
    "Delta Lake", "Auto Loader", "PySpark", "Unity Catalog", "Databricks SQL",
    "MLflow", "Structured Streaming", "Photon", "Serverless", "Terraform"
]

STATUSES = ["completed", "in-progress", "at-risk", "planned"]

# Templates for notes and feedback to make them look realistic
NOTES_TEMPLATES = [
    "Customer faced issues with {tech}. Resolved by optimizing configuration.",
    "Team is struggling with {tech} adoption. Recommended training.",
    "Successfully migrated to {tech}. Performance improved by 30%.",
    "Initial setup of {tech} was challenging due to legacy data formats.",
    "POC for {tech} was successful. Moving to production next week.",
    "Debugging {tech} errors took significant time. Root cause was network configuration.",
    "Customer requested best practices for {tech} scaling.",
    "Implemented {tech} for real-time analytics dashboard.",
    "Governance review highlighted gaps in {tech} implementation.",
    "Optimized {tech} jobs to reduce costs by 20%."
]

FEEDBACK_TEMPLATES = [
    "Great experience, but {tech} documentation could be better.",
    "The team was very helpful in resolving our {tech} issues.",
    "Impressed with the performance of {tech}.",
    "Implementation took longer than expected due to {tech} complexity.",
    "Would recommend Databricks for {tech} workloads.",
    "Need more support on {tech} advanced features.",
    "Smooth transition to {tech}.",
    "Encountered some bugs with {tech} preview features.",
    "Excellent guidance on {tech} architecture.",
    "Looking forward to expanding {tech} usage."
]

def generate_record(index):
    customer = random.choice(CUSTOMERS)
    tech_stack = random.sample(TECHNOLOGIES, k=random.randint(1, 4))
    main_tech = tech_stack[0]
    
    status = random.choices(STATUSES, weights=[0.5, 0.3, 0.1, 0.1])[0]
    
    # Generate date within the last 3 months
    days_ago = random.randint(0, 90)
    date_obj = datetime.now() - timedelta(days=days_ago)
    date_str = date_obj.strftime("%Y-%m-%d")
    
    notes = random.choice(NOTES_TEMPLATES).format(tech=main_tech)
    feedback = random.choice(FEEDBACK_TEMPLATES).format(tech=main_tech)
    
    return {
        "id": f"ENG-{index:03d}",
        "customer": customer,
        "notes": notes,
        "feedback": feedback,
        "technologies": tech_stack,
        "status": status,
        "date": date_str
    }

def main():
    print(f"Generating {NUM_RECORDS} synthetic engagement records...")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    records = [generate_record(i + 1) for i in range(NUM_RECORDS)]
    
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "w") as f:
        json.dump(records, f, indent=4)
        
    print(f"Successfully saved records to {output_path}")

if __name__ == "__main__":
    main()
