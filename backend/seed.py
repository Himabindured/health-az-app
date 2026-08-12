from database import SessionLocal
from models.models import Condition

CONDITIONS = [
    {"name":"Asthma","category":"Respiratory","overview":"A chronic condition where airways become inflamed and narrow, causing breathing difficulty. Triggered by allergens, exercise, or cold air.","symptoms":["Wheezing","Shortness of breath","Chest tightness","Coughing at night"],"severity":2,"treatment":"Bronchodilators (inhalers), corticosteroids, avoiding triggers, and regular monitoring."},
    {"name":"Diabetes (Type 2)","category":"Metabolic","overview":"A metabolic disorder where the body cannot properly use insulin, leading to elevated blood sugar levels over time.","symptoms":["Frequent urination","Excessive thirst","Fatigue","Blurred vision","Slow wound healing"],"severity":3,"treatment":"Lifestyle changes, metformin, blood sugar monitoring, and in some cases insulin therapy."},
    {"name":"Hypertension","category":"Cardiovascular","overview":"Consistently elevated blood pressure (≥140/90 mmHg) that strains the heart and blood vessels, increasing risk of stroke and heart disease.","symptoms":["Often no symptoms","Headache","Dizziness","Shortness of breath","Nosebleeds"],"severity":3,"treatment":"Low-sodium diet, exercise, weight management, and antihypertensive medications."},
    {"name":"Migraine","category":"Neurological","overview":"A neurological condition causing intense, throbbing headaches often with nausea and light sensitivity, lasting hours to days.","symptoms":["Severe one-sided headache","Nausea","Vomiting","Light sensitivity","Aura"],"severity":2,"treatment":"Pain relievers, triptans, preventive medications, and identifying personal triggers."},
    {"name":"Osteoporosis","category":"Musculoskeletal","overview":"A bone disease where density decreases, making fractures more likely. Common in postmenopausal women and older adults.","symptoms":["Back pain","Loss of height","Stooped posture","Fractures from minor falls"],"severity":2,"treatment":"Calcium and Vitamin D supplements, weight-bearing exercise, bisphosphonates."},
    {"name":"Eczema","category":"Dermatological","overview":"A chronic inflammatory skin condition causing dry, itchy, inflamed patches. Often associated with allergies and asthma.","symptoms":["Itchy skin","Red patches","Dry/scaly skin","Blisters","Skin thickening"],"severity":1,"treatment":"Moisturisers, topical corticosteroids, antihistamines, and avoiding irritants."},
    {"name":"Anxiety Disorder","category":"Mental Health","overview":"A group of conditions characterised by persistent, excessive worry or fear that interferes with daily activities.","symptoms":["Excessive worry","Restlessness","Fatigue","Difficulty concentrating","Sleep disturbance"],"severity":2,"treatment":"Cognitive behavioural therapy (CBT), SSRIs, lifestyle changes, and mindfulness."},
    {"name":"Gastritis","category":"Digestive","overview":"Inflammation of the stomach lining, caused by H. pylori infection, NSAIDs, or excessive alcohol.","symptoms":["Stomach pain","Nausea","Vomiting","Bloating","Loss of appetite"],"severity":2,"treatment":"Proton pump inhibitors, antibiotics (for H. pylori), dietary changes, and antacids."},
    {"name":"Anaemia","category":"Haematological","overview":"A condition where there are insufficient healthy red blood cells to carry adequate oxygen to the body's tissues.","symptoms":["Fatigue","Pale skin","Shortness of breath","Dizziness","Cold hands/feet"],"severity":2,"treatment":"Iron supplements, dietary changes, Vitamin B12 injections, or treating underlying causes."},
    {"name":"Hypothyroidism","category":"Endocrine","overview":"An underactive thyroid gland that produces insufficient hormones, slowing down metabolism and body functions.","symptoms":["Fatigue","Weight gain","Cold sensitivity","Dry skin","Constipation","Depression"],"severity":2,"treatment":"Daily levothyroxine (synthetic thyroid hormone), lifelong treatment required."},
    {"name":"COPD","category":"Respiratory","overview":"Chronic obstructive pulmonary disease — a progressive lung disease including emphysema and chronic bronchitis, mostly from smoking.","symptoms":["Chronic cough","Shortness of breath","Wheezing","Chest tightness","Frequent infections"],"severity":3,"treatment":"Bronchodilators, inhaled steroids, pulmonary rehab, and smoking cessation."},
    {"name":"Rheumatoid Arthritis","category":"Musculoskeletal","overview":"An autoimmune disease causing chronic inflammation of joints, leading to pain, swelling, and eventual joint damage.","symptoms":["Joint pain","Morning stiffness","Swollen joints","Fatigue","Fever"],"severity":3,"treatment":"DMARDs (methotrexate), biologics, NSAIDs, physiotherapy, and lifestyle adjustments."},
    {"name":"Depression","category":"Mental Health","overview":"A mood disorder causing persistent sadness, loss of interest, and a range of physical and emotional problems.","symptoms":["Persistent sadness","Loss of interest","Sleep changes","Appetite changes","Fatigue","Hopelessness"],"severity":3,"treatment":"Psychotherapy, antidepressants (SSRIs/SNRIs), lifestyle changes, and social support."},
    {"name":"Urinary Tract Infection","category":"Urological","overview":"A bacterial infection in any part of the urinary system — kidneys, bladder, ureters, or urethra. More common in women.","symptoms":["Burning urination","Frequent urge to urinate","Cloudy urine","Pelvic pain","Fever"],"severity":1,"treatment":"Antibiotics (trimethoprim, nitrofurantoin), hydration, and urinary analgesics."},
]

def seed_conditions():
    db = SessionLocal()
    try:
        if db.query(Condition).count() == 0:
            for c in CONDITIONS:
                db.add(Condition(**c))
            db.commit()
            print(f"✅ Seeded {len(CONDITIONS)} conditions.")
        else:
            print("ℹ️  Conditions already seeded.")
    finally:
        db.close()
