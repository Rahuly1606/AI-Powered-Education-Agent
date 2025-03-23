#@title pipeline
# Import required modules
from aixplain.modules.agent import Agent
from aixplain.factories import AgentFactory

# Agent IDs from your deployment
AGENT_IDS = {
    "teacher_recruitment": "67dfca08338999cb9696a566",
    "training_mentorship": "67dfb3fc338999cb9696a525",
    "incentive_management": "67dfb3fd181c58b7238eb907",
    "community_engagement": "67dfb3fe338999cb9696a526",
    "progress_monitoring": "67dfc9f8338999cb9696a565",
    "team": "7a6d1fd8d107ec1c54e98c995ce4d35114644d43d890d11e2c6024bb11a46212"
}

# Print out the agent IDs for reference
print("Agent IDs for reference:")
for agent_name, agent_id in AGENT_IDS.items():
    print(f"{agent_name}: {agent_id}")

# Since Agent.load() is not available, let's check if we have direct access to our agents
# If you still have the agent objects in your session, use them directly
try:
    # Try to access one of your agents 
    # This assumes you still have the agent objects from when you created them
    test_query = teacher_recruitment_agent.run("Test query")
    print("We still have access to the agent objects!")
    
    # Define our function to use the agent objects
    def direct_agent_request(query, action_type, village_id=None, teacher_id=None):
        """Send requests directly to agents"""
        agent_map = {
            "recruitment": teacher_recruitment_agent,
            "training": training_mentorship_agent,
            "incentives": incentive_management_agent,
            "community": community_engagement_agent,
            "progress": progress_monitoring_agent,
            "full_cycle": rural_education_team
        }
        
        agent = agent_map.get(action_type)
        if not agent:
            return {"error": f"Unknown action type: {action_type}"}
        
        # Build the prompt
        prompt = query
        if village_id:
            prompt += f" (for village {village_id})"
        if teacher_id:
            prompt += f" (regarding teacher {teacher_id})"
            
        # Run the agent
        return agent.run(prompt)
    
except Exception as e:
    print(f"Error accessing agents: {e}")
    print("We'll need to recreate the agents")
    
    # If we don't have the agent objects, we'll need to create new ones
    # Since the API changed, let's check how to create agents properly
    # Try to inspect the AgentFactory
    import inspect
    print("\nInspecting AgentFactory.create:")
    try:
        print(inspect.signature(AgentFactory.create))
        print(inspect.getdoc(AgentFactory.create))
    except Exception as e:
        print(f"Error inspecting AgentFactory: {e}")
    
    # Let's try a simple approach to recreate an agent
    try:
        # Try to recreate one agent to see if it works
        new_agent = AgentFactory.create(
            name="Test Agent",
            llm_id="61e94f04d08575a63e6cbe14"  # Example LLM ID (GPT-4)
        )
        print("Successfully created a new agent!")
        
        # Define a function to recreate our agents
        def recreate_agents():
            """Recreate agents with the same configurations as before"""
            llm_id = "61e94f04d08575a63e6cbe14"  # Use a default LLM ID
            
            agents = {}
            
            agents["recruitment"] = AgentFactory.create(
                name="Teacher Recruitment Agent",
                description="Identifies and recruits educated rural youth as teachers",
                llm_id=llm_id
            )
            
            agents["training"] = AgentFactory.create(
                name="Training Mentorship Agent",
                description="Provides educational resources and mentorship",
                llm_id=llm_id
            )
            
            agents["incentives"] = AgentFactory.create(
                name="Incentive Management Agent",
                description="Manages non-monetary incentive distribution",
                llm_id=llm_id
            )
            
            agents["community"] = AgentFactory.create(
                name="Community Engagement Agent",
                description="Facilitates communication between stakeholders",
                llm_id=llm_id
            )
            
            agents["progress"] = AgentFactory.create(
                name="Progress Monitoring Agent",
                description="Tracks student outcomes and program growth",
                llm_id=llm_id
            )
            
            agents["full_cycle"] = AgentFactory.create(
                name="Rural Education Team",
                description="Coordinates education initiatives in rural communities",
                llm_id=llm_id
            )
            
            return agents
        
        # Function to send requests to our recreated agents
        def direct_agent_request(query, action_type, village_id=None, teacher_id=None):
            """Send requests directly to recreated agents"""
            all_agents = recreate_agents()
            
            agent = all_agents.get(action_type)
            if not agent:
                return {"error": f"Unknown action type: {action_type}"}
            
            # Build the prompt
            prompt = query
            if village_id:
                prompt += f" (for village {village_id})"
            if teacher_id:
                prompt += f" (regarding teacher {teacher_id})"
                
            # Run the agent
            return agent.run(prompt)
        
    except Exception as e:
        print(f"Error creating new agent: {e}")
        
        # If all else fails, let's create a simple function that uses the aixplain API directly
        def direct_agent_request(query, action_type, village_id=None, teacher_id=None):
            """Send requests directly using aixplain API"""
            import requests
            import os
            
            # Get the API key from environment
            api_key = os.environ.get("AIXPLAIN_API_KEY", "")
            if not api_key:
                return {"error": "AIXPLAIN_API_KEY not set in environment"}
            
            # Map action types to agent IDs
            agent_id = AGENT_IDS.get(action_type)
            if not agent_id:
                return {"error": f"Unknown action type: {action_type}"}
            
            # Build the prompt
            prompt = query
            if village_id:
                prompt += f" (for village {village_id})"
            if teacher_id:
                prompt += f" (regarding teacher {teacher_id})"
            
            # Make API request
            url = f"https://api.aixplain.com/agents/{agent_id}/run"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "prompt": prompt
            }
            
            try:
                response = requests.post(url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"error": f"API request failed: {str(e)}"}

# Create a simple interface to interact with our agents
def run_coordinator_interface():
    """Simple command-line interface for program coordinators"""
    print("\n==== Rural Education Program Coordinator Interface ====\n")
    print("Available actions:")
    print("1. recruitment - Find and recruit teachers")
    print("2. training - Get training resources and guidance")
    print("3. incentives - Manage teacher incentives")
    print("4. community - Community engagement strategies")
    print("5. progress - Monitor student and program progress")
    print("6. full_cycle - Complete implementation plan")
    print("7. exit - Exit the interface")
    
    while True:
        action = input("\nSelect an action (1-7): ")
        
        if action == "7":
            print("Exiting coordinator interface")
            break
        
        if action not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid selection. Please choose 1-7.")
            continue
        
        action_types = {
            "1": "recruitment",
            "2": "training",
            "3": "incentives",
            "4": "community",
            "5": "progress",
            "6": "full_cycle"
        }
        
        query = input("Enter your question or request: ")
        
        village_id = None
        if input("Do you want to specify a village? (y/n): ").lower() == "y":
            village_id = input("Enter village ID (e.g., V001): ")
        
        teacher_id = None
        if action in ["2", "3"] and input("Do you want to specify a teacher? (y/n): ").lower() == "y":
            teacher_id = input("Enter teacher ID (e.g., T001): ")
        
        try:
            result = direct_agent_request(
                query=query,
                action_type=action_types[action],
                village_id=village_id,
                teacher_id=teacher_id
            )
            print("\nResponse:")
            print(result)
        except Exception as e:
            print(f"Error: {str(e)}")

# Test with a sample query
print("\nTesting with a sample query:")
try:
    result = direct_agent_request(
        query="Find qualified female teachers for mathematics education",
        action_type="recruitment",
        village_id="V001"
    )
    print(result)
except Exception as e:
    print(f"Error in test query: {e}")

# Ask if user wants to run the interface
run_interface = input("\nDo you want to run the interactive interface? (y/n): ")
if run_interface.lower() == "y":
    run_coordinator_interface()
else:
    print("Skipping interactive interface.")

print("\nCompleted!")