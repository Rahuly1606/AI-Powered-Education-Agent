import os
import pandas as pd
from aixplain.factories import AgentFactory, TeamAgentFactory
from aixplain.modules.agent.tool.model_tool import ModelTool

# Agent IDs from previous deployment
AGENT_IDS = {
    "teacher_recruitment": "67e0fc32338999cb9696a93e",
    "training_mentorship": "67e0fc33338999cb9696a93f",
    "incentive_management": "67e0fc34181c58b7238ebd26",
    "community_engagement": "67e0fc35338999cb9696a940",
    "progress_monitoring": "67e0fc36338999cb9696a941"
}

def load_data(data_dir="SampleData"):
    """Load all data files from the specified directory."""
    data_frames = {}
    required_files = [
        'teacher_data.csv',
        'training_data.csv',
        'incentives_data.csv',
        'community_data.csv',
        'student_data.csv'
    ]
    
    for file_name in required_files:
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            data_frames[file_name.replace('.csv', '')] = pd.read_csv(file_path)
        else:
            print(f"Warning: {file_name} not found in {data_dir}")
    
    return data_frames

def update_data(data_frames, new_data):
    """Update existing data frames with new data."""
    for key, new_df in new_data.items():
        if key in data_frames:
            # Append new data to existing data
            data_frames[key] = pd.concat([data_frames[key], new_df], ignore_index=True)
            print(f"Updated {key} with {len(new_df)} new records")
        else:
            print(f"Warning: Unknown data type {key}")
    
    return data_frames

def update_agents(data_frames):
    """Update existing agents with new data."""
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

    # Update each agent with new data
    agents = {}
    
    # Teacher Recruitment Agent
    agents["teacher_recruitment"] = AgentFactory.get(AGENT_IDS["teacher_recruitment"])
    agents["teacher_recruitment"].description = f"""You are an agent that helps identify and recruit educated rural youth
    to become part-time teachers in their villages. You prioritize women candidates when
    appropriate and match candidates with teaching opportunities based on their skills,
    education level, and village proximity.

    Here's the updated teacher data you have access to:
    {data_frames.get('teacher_data', pd.DataFrame()).to_string()}

    Here's the updated community data you have access to:
    {data_frames.get('community_data', pd.DataFrame()).to_string()}"""

    # Training and Mentorship Agent
    agents["training_mentorship"] = AgentFactory.get(AGENT_IDS["training_mentorship"])
    agents["training_mentorship"].description = f"""You are an agent that provides educational resources, training materials,
    and ongoing mentorship to rural part-time teachers.

    Here's the updated training data you have access to:
    {data_frames.get('training_data', pd.DataFrame()).to_string()}"""
    agents["training_mentorship"].tools = [speech_synthesis_tool]

    # Incentive Management Agent
    agents["incentive_management"] = AgentFactory.get(AGENT_IDS["incentive_management"])
    agents["incentive_management"].description = f"""You are an agent that tracks teacher participation and manages the
    non-monetary incentives program.

    Here's the updated incentives data you have access to:
    {data_frames.get('incentives_data', pd.DataFrame()).to_string()}

    Here's the updated teacher data you have access to:
    {data_frames.get('teacher_data', pd.DataFrame()).to_string()}"""

    # Community Engagement Agent
    agents["community_engagement"] = AgentFactory.get(AGENT_IDS["community_engagement"])
    agents["community_engagement"].description = f"""You are an agent that facilitates communication between teachers, parents,
    and village elders.

    Here's the updated community data you have access to:
    {data_frames.get('community_data', pd.DataFrame()).to_string()}"""
    agents["community_engagement"].tools = [translation_tool, speech_synthesis_tool]

    # Progress Monitoring Agent
    agents["progress_monitoring"] = AgentFactory.get(AGENT_IDS["progress_monitoring"])
    agents["progress_monitoring"].description = f"""You are an agent that tracks student attendance, learning outcomes,
    and program growth.

    Here's the updated student data you have access to:
    {data_frames.get('student_data', pd.DataFrame()).to_string()}

    Here's the updated teacher data you have access to:
    {data_frames.get('teacher_data', pd.DataFrame()).to_string()}

    Here's the updated community data you have access to:
    {data_frames.get('community_data', pd.DataFrame()).to_string()}"""

    return agents

def main():
    # Load existing data
    print("Loading existing data...")
    data_frames = load_data()
    
    # Here you would typically load new data from files or input
    # For example:
    # new_data = {
    #     'teacher_data': pd.read_csv('new_teacher_data.csv'),
    #     'training_data': pd.read_csv('new_training_data.csv'),
    #     ...
    # }
    
    # Update data with new records
    # data_frames = update_data(data_frames, new_data)
    
    # Update agents with new data
    print("Updating agents with new data...")
    agents = update_agents(data_frames)
    
    # Deploy updated agents
    print("Deploying updated agents...")
    for agent_name, agent in agents.items():
        try:
            agent.update()
            print(f"Successfully updated {agent_name}")
        except Exception as e:
            print(f"Error updating {agent_name}: {str(e)}")
    
    print("\nUpdate complete! All agents have been updated with new data.")

if __name__ == "__main__":
    main() 