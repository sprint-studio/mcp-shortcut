#!/usr/bin/env python3

import logging
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

from client import ShortcutClient

# Import MCP SDK
from mcp.server.fastmcp import FastMCP

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("shortcut-pm-mcp")

# Global client that will be initialized at startup
client = None

# Create an MCP server
mcp = FastMCP("Shortcut Product Manager", 
             description="A virtual Product Manager using Shortcut API to manage your product development process",
             dependencies=["httpx"])

# Resources - Using type-specific schemes for resource paths
@mcp.resource("members://shortcut/members")
@mcp.tool("shortcut/members")
async def list_members() -> List[Dict]:
    """List all members in the workspace"""
    global client
    return await client.get("/members")

@mcp.resource("members://shortcut/members/{member_id}")
@mcp.tool("shortcut/members/{member_id}")
async def get_member(member_id: str) -> Dict:
    """Get details about a specific member"""
    global client
    return await client.get(f"/members/{member_id}")

@mcp.resource("stories://shortcut/stories")
@mcp.tool("shortcut/stories")
async def list_stories() -> List[Dict]:
    """List all stories in the workspace"""
    global client
    return await client.get("/stories")

@mcp.resource("stories://shortcut/stories/{story_id}")
@mcp.tool("shortcut/stories/{story_id}")
async def get_story(story_id: int) -> Dict:
    """Get details about a specific story"""
    global client
    return await client.get(f"/stories/{story_id}")

@mcp.resource("epics://shortcut/epics")
@mcp.tool("shortcut/epics")
async def list_epics() -> List[Dict]:
    """List all epics in the workspace"""
    global client
    return await client.get("/epics")

@mcp.resource("epics://shortcut/epics/{epic_id}")
@mcp.tool("shortcut/epics/{epic_id}")
async def get_epic(epic_id: int) -> Dict:
    """Get details about a specific epic"""
    global client
    return await client.get(f"/epics/{epic_id}")

@mcp.resource("milestones://shortcut/milestones")
@mcp.tool("shortcut/milestones")
async def list_milestones() -> List[Dict]:
    """List all milestones in the workspace"""
    global client
    return await client.get("/milestones")

@mcp.resource("milestones://shortcut/milestones/{milestone_id}")
@mcp.tool("shortcut/milestones/{milestone_id}")
async def get_milestone(milestone_id: int) -> Dict:
    """Get details about a specific milestone"""
    global client
    return await client.get(f"/milestones/{milestone_id}")

@mcp.resource("projects://shortcut/projects")
@mcp.tool("shortcut/projects")
async def list_projects() -> List[Dict]:
    """List all projects in the workspace"""
    global client
    return await client.get("/projects")

@mcp.resource("projects://shortcut/projects/{project_id}")
@mcp.tool("shortcut/projects/{project_id}")
async def get_project(project_id: int) -> Dict:
    """Get details about a specific project"""
    global client
    return await client.get(f"/projects/{project_id}")

@mcp.resource("workflows://shortcut/workflows")
@mcp.tool("shortcut/workflows")
async def list_workflows() -> List[Dict]:
    """List all workflows in the workspace"""
    global client
    return await client.get("/workflows")

@mcp.resource("workflows://shortcut/workflows/{workflow_id}")
@mcp.tool("shortcut/workflows/{workflow_id}")
async def get_workflow(workflow_id: int) -> Dict:
    """Get details about a specific workflow"""
    global client
    return await client.get(f"/workflows/{workflow_id}")

@mcp.resource("iterations://shortcut/iterations")
@mcp.tool("shortcut/iterations")
async def list_iterations() -> List[Dict]:
    """List all iterations/sprints in the workspace"""
    global client
    return await client.get("/iterations")

@mcp.resource("iterations://shortcut/iterations/{iteration_id}")
@mcp.tool("shortcut/iterations/{iteration_id}")
async def get_iteration(iteration_id: int) -> Dict:
    """Get details about a specific iteration/sprint"""
    global client
    return await client.get(f"/iterations/{iteration_id}")

@mcp.resource("labels://shortcut/labels")
@mcp.tool("shortcut/labels")
async def list_labels() -> List[Dict]:
    """List all labels in the workspace"""
    global client
    return await client.get("/labels")

@mcp.resource("teams://shortcut/teams")
@mcp.tool("shortcut/teams")
async def list_teams() -> List[Dict]:
    """List all teams in the workspace"""
    global client
    return await client.get("/teams")

# Tools
@mcp.tool()
async def search_stories(query: str) -> List[Dict]:
    """Search for stories using Shortcut's search syntax"""
    global client
    try:
        # Shortcut API uses the /search endpoint for searching stories
        params = {"query": query, "page_size": 25}
        results = await client.get("/search", params)
        
        # Filter to only return stories from the search results
        stories = []
        if "data" in results and results["data"]:
            for item in results["data"]:
                if item["type"] == "story":
                    stories.append(item["data"])
        
        return stories
    except Exception as e:
        logger.error(f"Error searching stories: {str(e)}")
        return []

@mcp.tool()
async def create_story(
    name: str,
    description: Optional[str] = None,
    project_id: Optional[int] = None,
    workflow_state_id: Optional[int] = None,
    epic_id: Optional[int] = None,
    estimate: Optional[int] = None,
    labels: Optional[List[str]] = None,
    owner_ids: Optional[List[str]] = None
) -> str:
    """Create a new story in Shortcut"""
    global client
    try:
        data = {
            "name": name,
        }
        
        if description:
            data["description"] = description
        if project_id:
            data["project_id"] = project_id
        if workflow_state_id:
            data["workflow_state_id"] = workflow_state_id
        if epic_id:
            data["epic_id"] = epic_id
        if estimate:
            data["estimate"] = estimate
        if labels:
            data["labels"] = [{"name": label} for label in labels]
        if owner_ids:
            data["owner_ids"] = owner_ids
        
        story = await client.post("/stories", data)
        return f"Story created successfully with ID {story['id']} and URL {story['app_url']}"
    except Exception as e:
        return f"Error creating story: {str(e)}"

@mcp.tool()
async def update_story(
    story_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    project_id: Optional[int] = None,
    workflow_state_id: Optional[int] = None,
    epic_id: Optional[int] = None,
    estimate: Optional[int] = None,
    labels: Optional[List[str]] = None,
    owner_ids: Optional[List[str]] = None
) -> str:
    """Update an existing story in Shortcut"""
    global client
    try:
        data = {}
        
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if project_id:
            data["project_id"] = project_id
        if workflow_state_id:
            data["workflow_state_id"] = workflow_state_id
        if epic_id:
            data["epic_id"] = epic_id
        if estimate is not None:
            data["estimate"] = estimate
        if labels:
            data["labels"] = [{"name": label} for label in labels]
        if owner_ids:
            data["owner_ids"] = owner_ids
        
        story = await client.put(f"/stories/{story_id}", data)
        return f"Story {story_id} updated successfully. URL: {story['app_url']}"
    except Exception as e:
        return f"Error updating story: {str(e)}"

@mcp.tool()
async def create_epic(
    name: str,
    description: Optional[str] = None,
    milestone_id: Optional[int] = None,
    state: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Create a new epic in Shortcut"""
    global client
    try:
        data = {"name": name}
        
        if description:
            data["description"] = description
        if milestone_id:
            data["milestone_id"] = milestone_id
        if state:
            data["state"] = state
        if start_date:
            data["start_date"] = start_date
        if end_date:
            data["deadline"] = end_date
        
        epic = await client.post("/epics", data)
        return f"Epic created successfully with ID {epic['id']} and URL {epic['app_url']}"
    except Exception as e:
        return f"Error creating epic: {str(e)}"

@mcp.tool()
async def create_milestone(
    name: str,
    description: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Create a new milestone in Shortcut"""
    global client
    try:
        data = {"name": name}
        
        if description:
            data["description"] = description
        if start_date:
            data["started_at_override"] = start_date
        if end_date:
            data["completed_at_override"] = end_date
        
        milestone = await client.post("/milestones", data)
        return f"Milestone created successfully with ID {milestone['id']}"
    except Exception as e:
        return f"Error creating milestone: {str(e)}"

@mcp.tool()
async def create_iteration(
    name: str,
    description: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    group_ids: Optional[List[str]] = None
) -> str:
    """Create a new iteration/sprint in Shortcut"""
    global client
    try:
        data = {
            "name": name,
            "start_date": start_date,
            "end_date": end_date
        }
        
        if description:
            data["description"] = description
        if group_ids:
            data["group_ids"] = group_ids
        
        iteration = await client.post("/iterations", data)
        return f"Iteration created successfully with ID {iteration['id']}"
    except Exception as e:
        return f"Error creating iteration: {str(e)}"

@mcp.tool()
async def create_label(name: str, description: Optional[str] = None) -> str:
    """Create a new label in Shortcut"""
    global client
    try:
        data = {"name": name}
        if description:
            data["description"] = description
        
        label = await client.post("/labels", data)
        return f"Label '{name}' created successfully with ID {label['id']}"
    except Exception as e:
        return f"Error creating label: {str(e)}"

# Add prompt templates for key PM activities
@mcp.prompt()
def create_story_prompt() -> str:
    """Create a new story in Shortcut"""
    return """
    I need to create a new story in Shortcut. Please help me with the following details:
    
    1. What should be the name of the story?
    2. What's the description for the story?
    3. Do you know the project ID it should be added to?
    4. Do you know the workflow state ID it should start in?
    5. Should it be part of an epic? If yes, what's the epic ID?
    6. What's the estimate for this story?
    
    Once you have this information, you can use the create_story tool to create the story in Shortcut.
    """

@mcp.prompt()
def sprint_planning_prompt() -> str:
    """Help organize and plan upcoming sprints"""
    return """
    I'll help you plan your upcoming sprint in Shortcut. To get started, please tell me:
    
    1. When does your sprint start and end? (dates)
    2. What is your team's velocity? (story points per sprint)
    3. Are there any specific epics or themes you want to focus on?
    4. Do you have any carry-over stories from the previous sprint?
    
    After I have this information, I can:
    - Search for potential stories to include from your backlog
    - Recommend a balanced mix of story types
    - Help estimate stories if needed
    - Check for dependencies between stories
    - Organize the sprint backlog with a logical sequence
    
    If you have specific story IDs you'd like to include, please share those as well.
    """

@mcp.prompt()
def feature_specification_prompt() -> str:
    """Write detailed feature specifications"""
    return """
    I'll help you write a detailed feature specification for Shortcut. Please provide:
    
    1. What is the name of the feature?
    2. What problem does this feature solve? Who is it for?
    3. What are the high-level requirements?
    4. Are there any design mockups or references?
    5. Are there technical constraints or requirements to consider?
    6. How does this feature tie into your overall product strategy?
    
    I'll help you create a comprehensive specification that includes:
    - Feature overview and business justification
    - Success metrics: how will we know if this feature is successful?
    - User stories or job stories
    - Detailed functional requirements
    - Non-functional requirements (performance, security, etc.)
    - User experience flow with key screens and interactions
    - Technical implementation guidelines
    - Acceptance criteria for each component
    - Testing requirements and edge cases
    - Rollout and launch considerations
    - Future enhancements or iterations to consider
    
    Once we have this specification, I'll create an epic in Shortcut with appropriately linked stories.
    """

@mcp.prompt()
def roadmap_planning_prompt() -> str:
    """Plan strategic product roadmaps"""
    return """
    I'll help you plan a strategic product roadmap in Shortcut. Let's start with:
    
    1. What timeframe are you planning for? (Quarter, 6 months, year, etc.)
    2. What are your key business or product objectives for this period?
    3. Who are the key stakeholders or customers this roadmap addresses?
    4. What constraints do you need to consider? (resources, deadlines, market events, etc.)
    5. What are your current product pillars or strategic themes?
    
    I can help you:
    - Structure your roadmap into themes, epics, and milestones
    - Balance different types of work (new features, improvements, technical debt, research)
    - Set realistic timelines based on team capacity and priorities
    - Identify dependencies or sequence constraints
    - Create a roadmap that communicates clearly to different audiences
    - Incorporate feedback from stakeholders and customers
    - Establish key OKRs or success metrics for major initiatives
    - Plan discovery and validation activities alongside delivery
    
    Once we've outlined the roadmap, I'll implement it in Shortcut by creating epics, milestones, and associated stories with appropriate timeline indicators.
    """

@mcp.prompt()
def market_research_prompt() -> str:
    """Analyze competitive landscape and market opportunities"""
    return """
    I'll help you conduct a thorough market analysis and competitive research. Let's gather information about:

    1. Target Market Understanding:
       - Who are your primary and secondary target users/customers?
       - What are their key pain points and needs?
       - What market segments are you focusing on?

    2. Competitive Analysis:
       - Who are your direct competitors?
       - Who are your indirect competitors?
       - For each competitor, what are their:
         * Key features and differentiators
         * Strengths and weaknesses
         * Pricing strategies
         * Target audience
         * Market positioning

    3. Market Opportunities:
       - What are the unmet needs in the market?
       - What trends are emerging in your industry?
       - What technological advances could impact your product?
       - What regulatory changes might affect the market?

    4. Competitive Advantage:
       - What unique value proposition can you offer?
       - What features or capabilities set you apart?
       - What barriers to entry exist in your market?
       - How sustainable is your competitive advantage?

    Based on this analysis, I can help you:
    - Create epics for key opportunity areas
    - Define stories for competitive feature development
    - Set up tracking labels for competitor-related items
    - Prioritize features based on competitive positioning
    - Document market insights in story descriptions
    - Create a competitive monitoring framework
    - Plan regular competitive analysis updates

    I'll help organize this information in Shortcut by creating:
    - An epic for market research findings
    - Stories for each competitor analysis
    - Labels for tracking competitive features
    - Milestones for market opportunity initiatives
    """

@mcp.prompt()
def user_feedback_analysis_prompt() -> str:
    """Analyze user feedback to identify needs and prioritize features"""
    return """
    I'll help you analyze user feedback to identify key needs and prioritize your product backlog. Let's start by identifying:

    1. Feedback Sources:
       - What sources of user feedback do you have? (surveys, support tickets, reviews, user interviews, usage data)
       - How recent is this feedback?
       - Which user segments or personas does the feedback represent?
       - Are there any biases in your feedback collection methods?

    2. Feedback Analysis:
       - What are the most common pain points mentioned?
       - What feature requests appear most frequently?
       - What patterns emerge across different feedback channels?
       - What is the emotional tone of the feedback? (frustrated, satisfied, confused)
       - Which areas of your product receive the most positive/negative feedback?

    3. User Needs Identification:
       - What underlying needs do these feedback points reveal?
       - Are users asking for specific solutions or expressing problems?
       - What jobs-to-be-done are users struggling with?
       - Are there unstated needs that emerge from analyzing usage patterns?
       - What contextual factors affect user needs? (industry, company size, role)

    4. Prioritization Framework:
       - How does this feedback align with your product strategy?
       - Which needs impact the largest number of users?
       - Which needs represent the most critical user journeys?
       - What is the potential business impact of addressing each need?
       - How technically feasible is it to address each need?
       - What is the opportunity cost of not addressing certain needs?

    Based on this analysis, I can help you:
    - Categorize feedback into actionable themes
    - Create user stories that address underlying needs
    - Assign priority levels to backlog items
    - Design validation experiments for proposed solutions
    - Map user needs to your product roadmap
    - Set up metrics to measure improvement in problem areas

    I'll help organize this in Shortcut by creating:
    - Epics for major user need themes
    - Stories for specific feedback-driven improvements
    - Labels to track feedback sources and sentiment
    - Custom fields for priority levels and impact metrics
    - Links between related feedback items and development work
    """

if __name__ == "__main__":
    # Initialize client here
    api_token = os.getenv("SHORTCUT_API_TOKEN")
    api_url = os.getenv("SHORTCUT_API_URL")
    
    if not api_token:
        logger.error("SHORTCUT_API_TOKEN environment variable not set")
        raise ValueError("SHORTCUT_API_TOKEN environment variable not set")
    
    # Create global client that will be used by all handlers
    client = ShortcutClient(api_url, api_token)
    
    # Start the MCP server
    mcp.run()