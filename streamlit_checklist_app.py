import streamlit as st

def generate_checklist(role):
    common_tools = [
        "Google Workspace account setup",
        "Slack workspace invite",
        "Zoom license activation",
        "Okta/SSO provisioning",
        "Introductory security guidelines PDF"
    ]

    role_specific = {
        "Engineer": ["GitHub repo access", "Jira board invite", "PostgreSQL credentials"],
        "Sales": ["HubSpot access", "CRM training invite", "Sales presentation decks"],
        "Support": ["Zendesk credentials", "Knowledge base access", "Escalation protocol document"]
    }

    return common_tools + role_specific.get(role, [])

# Streamlit UI
st.title("New Hire Onboarding Checklist Generator")

name = st.text_input("Enter new hire's name")
role = st.selectbox("Select role", ["Engineer", "Sales", "Support"])

if st.button("Generate Checklist"):
    if name and role:
        checklist = generate_checklist(role)
        st.subheader(f"Onboarding Checklist for {name} ({role})")
        for i, item in enumerate(checklist, 1):
            st.markdown(f"{i}. {item}")
    else:
        st.warning("Please fill out all fields.")
