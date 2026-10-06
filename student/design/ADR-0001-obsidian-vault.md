schema_version: "1.0"
proposal_id: "adr-0001"
status: "proposed"
personal_domain: "Knowledge Management"
intended_learning_outcome: "Learn to manage external study materials alongside course code"
non_goals:
  - "Do not sync raw vault content directly into git history"
  - "Do not track personal unverified notes in main repo"
governance:
  ai_role: "Assist with code structure and validation troubleshooting"
  deterministic_role: "Automated schema validation via CLI tools"
  human_role: "Student reviews decisions and executes system commands"
usefulness_condition: "Useful when referencing external notes during labs"
material_risk: "Low risk of local path mismatch across different PCs"
non_ai_baseline: "Manual note tracking in standard text files"
uncertainty: "Low"
required_evidence:
  - "Saved screenshot of doctor report"
  - "Environment report file in json format"
