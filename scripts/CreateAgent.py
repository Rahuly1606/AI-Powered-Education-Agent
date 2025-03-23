#@title  setup environment

import os
import pandas as pd
from aixplain.factories import AgentFactory, TeamAgentFactory
from aixplain.modules.agent.tool.model_tool import ModelTool
from google.colab import files


# Step 2: Upload and prepare data files
print("Please upload your CSV files (teacher_data.csv, training_data.csv, incentives_data.csv, community_data.csv, student_data.csv)")
uploaded = files.upload()  # This will prompt you to upload files

# Reading the uploaded CSV files
file_names = list(uploaded.keys())
data_frames = {}

for file_name in file_names:
    # Skip non-CSV files if any
    if not file_name.endswith('.csv'):
        continue
    data_frames[file_name.replace('.csv', '')] = pd.read_csv(file_name)

# Step 3: Create agents without vector tools (simplified version)

# Speech synthesis tool
speech_synthesis_tool = ModelTool(
    model="6171efa6159531495cadefc2",  # aiXplain - Text to Speech
    description="Converts text to speech for creating audio learning materials"
)

# Translation tool
translation_tool = ModelTool(
    model="61b097551efecf30109d32da",  # aiXplain - Translation (OPUS-MT)
    description="Translates content between languages to support multilingual education"
)

# Create Individual Agents
teacher_recruitment_agent = AgentFactory.create(
    name="Teacher Recruitment Agent",
    description="""You are an agent that helps identify and recruit educated rural youth
    to become part-time teachers in their villages. You prioritize women candidates when
    appropriate and match candidates with teaching opportunities based on their skills,
    education level, and village proximity. You explain the non-monetary incentive system
    (farming tools, food supplies, scholarships) to candidates. 
    
    Here's the teacher data you have access to:
    """ + pd.DataFrame(data_frames.get('teacher_data', pd.DataFrame())).to_string() + """
    
    Here's the community data you have access to:
    """ + pd.DataFrame(data_frames.get('community_data', pd.DataFrame())).to_string(),
    llm_id="6646261c6eb563165658bbb1"  # aiXplain - OpenAI GPT-4
)

training_mentorship_agent = AgentFactory.create(
    name="Training and Mentorship Agent",
    description="""You are an agent that provides educational resources, training materials,
    and ongoing mentorship to rural part-time teachers. You help simplify complex educational
    concepts, suggest interactive teaching methods for rural settings with limited resources,
    and provide guidance on engaging students effectively. You particularly focus on strategies
    to promote girls' education and create inclusive learning environments.
    
    Here's the training data you have access to:
    """ + pd.DataFrame(data_frames.get('training_data', pd.DataFrame())).to_string() + """
    
    Basic mathematics teaching methods for rural settings: Focus on using everyday objects for counting, 
    measuring, and basic arithmetic. Use local contexts like farming calculations, market transactions, 
    and household budgeting to make concepts relevant.
    
    Language teaching in multilingual rural contexts: Start with familiar local language, 
    use storytelling from local traditions, gradually introduce national language, 
    use practical applications like letter writing and form filling.
    
    Science teaching with minimal resources: Use nature as laboratory, observe local plants and animals, 
    study agricultural practices, discuss weather patterns and seasonal changes, 
    use simple household items for experiments.
    
    Effective teaching methods for mixed-age classrooms: Group activities by ability rather than age, 
    use peer teaching where older students help younger ones, rotate attention between groups, 
    use self-directed activities, incorporate games and interactive learning.""",
    tools=[speech_synthesis_tool],
    llm_id="6646261c6eb563165658bbb1"  # aiXplain - OpenAI GPT-4
)

incentive_management_agent = AgentFactory.create(
    name="Incentive Management Agent",
    description="""You are an agent that tracks teacher participation and manages the 
    non-monetary incentives program. You help match teachers with appropriate incentives 
    such as farming tools, ration kits, school supplies, or scholarships based on their 
    needs and teaching contributions. You ensure fair distribution of resources and maintain
    records of allocated incentives.
    
    Here's the incentives data you have access to:
    """ + pd.DataFrame(data_frames.get('incentives_data', pd.DataFrame())).to_string() + """
    
    Here's the teacher data you have access to:
    """ + pd.DataFrame(data_frames.get('teacher_data', pd.DataFrame())).to_string(),
    llm_id="6646261c6eb563165658bbb1"  # aiXplain - OpenAI GPT-4
)

community_engagement_agent = AgentFactory.create(
    name="Community Engagement Agent",
    description="""You are an agent that facilitates communication between teachers, parents, 
    and village elders. You help organize community meetings, gather feedback from parents, 
    and ensure education is valued as a shared responsibility. You promote parental involvement
    in children's education and help address community concerns about education, especially
    for girls.
    
    Here's the community data you have access to:
    """ + pd.DataFrame(data_frames.get('community_data', pd.DataFrame())).to_string(),
    tools=[translation_tool, speech_synthesis_tool],
    llm_id="6646261c6eb563165658bbb1"  # aiXplain - OpenAI GPT-4
)

progress_monitoring_agent = AgentFactory.create(
    name="Progress Monitoring Agent",
    description="""You are an agent that tracks student attendance, learning outcomes, 
    and program growth. You analyze data to identify trends, success stories, and areas 
    needing improvement. You create progress reports for stakeholders and suggest 
    interventions for students or villages showing concerning patterns.
    
    Here's the student data you have access to:
    """ + pd.DataFrame(data_frames.get('student_data', pd.DataFrame())).to_string() + """
    
    Here's the teacher data you have access to:
    """ + pd.DataFrame(data_frames.get('teacher_data', pd.DataFrame())).to_string() + """
    
    Here's the community data you have access to:
    """ + pd.DataFrame(data_frames.get('community_data', pd.DataFrame())).to_string(),
    llm_id="6646261c6eb563165658bbb1"  # aiXplain - OpenAI GPT-4
)

# Create Team Agent
rural_education_team = TeamAgentFactory.create(
    name="Rural Education Team",
    description="""You are a team that empowers educated rural youth—especially women—to 
    become part-time teachers in their villages. You coordinate the recruitment, training, 
    incentive management, community engagement, and progress monitoring aspects of the 
    rural education program. You focus on creating sustainable education cycles within 
    communities through non-monetary incentive systems.""",
    agents=[
        teacher_recruitment_agent,
        training_mentorship_agent,
        incentive_management_agent,
        community_engagement_agent,
        progress_monitoring_agent
    ],
    llm_id="6646261c6eb563165658bbb1"  # aiXplain - OpenAI GPT-4
)

# Test Individual Agents
print("Testing Teacher Recruitment Agent:")
recruitment_response = teacher_recruitment_agent.run(
    "Find qualified female candidates with at least high school education who can teach Mathematics in their villages."
)
print(recruitment_response)

print("\nTesting Training & Mentorship Agent:")
training_response = training_mentorship_agent.run(
    "Suggest interactive mathematics teaching methods for a classroom with no electricity and limited supplies."
)
print(training_response)

print("\nTesting Incentive Management Agent:")
incentive_response = incentive_management_agent.run(
    "Which incentives are currently available for teachers who have completed at least 3 months of teaching?"
)
print(incentive_response)

print("\nTesting Community Engagement Agent:")
community_response = community_engagement_agent.run(
    "How can we increase parental support for girls' education in traditional communities?"
)
print(community_response)

print("\nTesting Progress Monitoring Agent:")
progress_response = progress_monitoring_agent.run(
    "Which village shows the most improvement in student attendance over the last three months?"
)
print(progress_response)

# Test Team Agent
print("\nTesting Rural Education Team Agent:")
team_response = rural_education_team.run("""
We need to expand our program to a new district with 5 villages. 
How should we approach recruitment, training, incentives, community engagement, 
and progress tracking?
""")
print(team_response)

# Deploy Agents
print("\nDeploying all agents...")
agent_ids = {
    "Teacher Recruitment Agent": teacher_recruitment_agent.deploy(),
    "Training & Mentorship Agent": training_mentorship_agent.deploy(),
    "Incentive Management Agent": incentive_management_agent.deploy(),
    "Community Engagement Agent": community_engagement_agent.deploy(),
    "Progress Monitoring Agent": progress_monitoring_agent.deploy(),
    "Rural Education Team": rural_education_team.deploy()
}

print("\nDeployment complete! Here are your agent IDs:")
for agent_name, agent_id in agent_ids.items():
    print(f"{agent_name} ID: {agent_id}")

print("\nYou can now access these agents via the aixplain platform or API.")