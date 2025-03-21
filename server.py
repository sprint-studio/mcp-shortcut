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
    - Search for prioritization_workshop_prompt stories to include from your backlog
    - Recommend a balanced mix of story types
    - Help estimate stories if needed
    - Check for dependencies between stories
    - Organize the sprint backlog with a logical sequence
    
    If you have specific story IDs you'd like to include, please share those as well.
    """

@mcp.prompt()
def feature_impact_analysis_prompt() -> str:
    """Evaluate potential solutions and their expected impact"""
    return """
    I'll help you evaluate potential features and solutions to determine which will have the greatest impact. Let's analyze:

    1. Solution Effectiveness:
       - How well does each solution address the identified user needs?
       - What evidence do we have that this solution will work?
       - Are there alternative approaches we should consider?
       - What are the limitations of each proposed solution?
       - Are there any edge cases or user scenarios not covered?

    2. Business Impact Assessment:
       - How does each solution align with business objectives?
       - What key metrics will this solution impact? (revenue, retention, engagement)
       - What is the estimated ROI for each solution?
       - How does this solution affect different business stakeholders?
       - Does this solution create new business opportunities?

    3. User Impact Evaluation:
       - Which user segments will benefit most from each solution?
       - How will the solution change user behavior or workflows?
       - What is the learning curve for users adopting this solution?
       - How might users respond negatively to this change?
       - What is the accessibility impact of this solution?

    4. Technical and Resource Considerations:
       - What is the development complexity of each solution?
       - What dependencies exist with other features or systems?
       - What ongoing maintenance will be required?
       - What are the performance implications?
       - What resources (time, people, infrastructure) are needed?

    5. Risk Assessment:
       - What could go wrong with each solution?
       - What security or privacy concerns exist?
       - How might competitors respond?
       - What regulatory considerations apply?
       - What is our mitigation plan for identified risks?

    6. Success Criteria and Measurement:
       - How will we know if this solution is successful?
       - What specific metrics should we track?
       - What is our testing and validation approach?
       - What are our thresholds for success vs. failure?
       - How will we gather feedback on the implementation?

    Based on this analysis, I can help you:
    - Create a decision matrix for feature evaluation
    - Document impact assessments in Shortcut stories
    - Define success metrics and tracking plan
    - Identify dependencies and risks to monitor
    - Prioritize features based on expected impact
    - Design smaller experiments to validate assumptions

    I'll help organize this in Shortcut by creating:
    - Epic descriptions with detailed impact analysis
    - Success criteria in story acceptance criteria
    - Custom fields for impact and risk scores
    - Labels for tracking metrics and outcomes
    - Stories for monitoring and measuring results
    """

@mcp.prompt()
def feature_specification_prompt() -> str:
    """Write detailed feature specifications"""
    return """
    I'll help you create a comprehensive feature specification document. Let's cover all the essential aspects:

    1. Feature Overview:
       - What is the name and brief description of the feature?
       - What is the primary purpose and value proposition?
       - Who are the target users or personas?
       - How does this feature align with product strategy and goals?
       - What is the expected business impact?

    2. Problem Statement and User Needs:
       - What specific user problems or needs does this feature address?
       - What use cases or scenarios will this feature support?
       - What jobs-to-be-done is the user trying to accomplish?
       - What evidence do we have about these needs? (user research, feedback, data)
       - How critical is this problem for our users?

    3. Success Metrics:
       - How will we measure the success of this feature?
       - What specific KPIs or metrics will be impacted?
       - What are our targets or thresholds for these metrics?
       - How will we collect the necessary data?
       - When will we evaluate performance?

    4. Functional Requirements:
       - What are the core capabilities the feature must provide?
       - What actions can users take with this feature?
       - What are the required inputs and expected outputs?
       - What are the different states or modes of the feature?
       - What validation rules or constraints apply?

    5. User Experience and Design:
       - What is the user flow or journey for this feature?
       - What are the key screens, components, or interactions?
       - How will the feature handle edge cases and errors?
       - What accessibility requirements must be met?
       - How will this feature integrate with existing UI patterns?

    6. Technical Requirements:
       - What backend systems or APIs will be affected?
       - What data structures or models are needed?
       - What performance requirements must be met?
       - What security or privacy considerations exist?
       - How will the feature scale with increased usage?

    7. Dependencies and Constraints:
       - What other features or systems does this depend on?
       - What technical limitations might affect implementation?
       - Are there any third-party integrations required?
       - What are the regulatory or compliance requirements?
       - What resource constraints must be considered?

    8. Implementation Plan:
       - What is the proposed implementation approach?
       - Can this be broken down into smaller increments?
       - What is the estimated level of effort?
       - What are the key milestones or phases?
       - What resources (people, tools, etc.) are needed?

    9. Testing Requirements:
       - What test cases should be covered?
       - What edge cases or error conditions need testing?
       - What performance or load testing is needed?
       - What user acceptance testing is required?
       - How will we gather feedback during testing?

    10. Rollout Strategy:
       - Will this be released gradually or all at once?
       - Is feature flagging or A/B testing needed?
       - What user communications are required?
       - What training or documentation is needed?
       - What monitoring will be in place during rollout?

    Based on this specification, I can help you:
    - Create a well-structured epic in Shortcut
    - Break down the work into individual stories
    - Define clear acceptance criteria for each story
    - Document technical requirements and dependencies
    - Create a trackable implementation plan

    I'll help organize this in Shortcut by:
    - A detailed epic with the complete specification
    - Individual stories for each component or requirement
    - Labels for tracking progress and components
    - Custom fields for priorities and dependencies
    - Attachments or links to relevant designs or research
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

    I'll help organize this in Shortcut by:
    - Epics for major user need themes
    - Stories for specific feedback-driven improvements
    - Labels to track feedback sources and sentiment
    - Custom fields for priority levels and impact metrics
    - Links between related feedback items and development work
    """

@mcp.prompt()
def acceptance_criteria_prompt() -> str:
    """Break down work into stories and set clear acceptance criteria"""
    return """
    I'll help you break down work into well-defined stories with clear acceptance criteria. Let's work through:

    1. Epic or Feature Breakdown:
       - What is the overall feature or epic we're breaking down?
       - What are the key user workflows or journeys involved?
       - What are the logical components or modules of this feature?
       - Are there distinct phases of implementation to consider?
       - What dependencies exist between different components?

    2. Story Creation Framework:
       - Who is the user or stakeholder for each story?
       - What specific action or capability does each story enable?
       - What is the business value or user benefit for each story?
       - How can we slice stories to be small but valuable?
       - Are these stories independent enough to be worked on separately?
       - Can each story be completed within a single iteration?

    3. Acceptance Criteria Structure:
       - What format works best for your team? (Given-When-Then, checklist, etc.)
       - What specific behaviors must be implemented?
       - What edge cases or error conditions need handling?
       - What performance or non-functional requirements apply?
       - What existing patterns or standards need to be followed?
       - What specific inputs and outputs should be validated?

    4. Testability Considerations:
       - How will each criteria be verified?
       - Are automated tests possible for these criteria?
       - What manual testing scenarios are required?
       - What test data or environments are needed?
       - Are there specific states or conditions to test?

    5. Definition of Done Elements:
       - What quality standards must be met?
       - What documentation is required?
       - What accessibility requirements apply?
       - What security checks are needed?
       - What performance thresholds must be achieved?
       - What approvals or sign-offs are required?

    6. Story Relationships and Sequence:
       - What is the optimal order for implementing these stories?
       - Which stories have technical dependencies on others?
       - Are there stories that can be developed in parallel?
       - Which stories should be prioritized for early feedback?
       - Are there stories that carry higher risk and should be addressed early?

    Based on this breakdown, I can help you:
    - Create right-sized stories in Shortcut with clear titles and descriptions
    - Draft comprehensive acceptance criteria for each story
    - Set appropriate estimates and priorities
    - Identify and document dependencies between stories
    - Create a logical implementation sequence
    - Define shared Definition of Done criteria across stories

    I'll help organize this in Shortcut by:
    - Creating well-structured stories under the parent epic
    - Adding clear acceptance criteria to each story description
    - Setting up story relationships and dependencies
    - Adding appropriate labels for tracking
    - Establishing workflow states based on implementation sequence
    - Documenting technical requirements and constraints
    """

@mcp.prompt()
def status_update_prompt() -> str:
    """Generate comprehensive status updates and track progress"""
    return """
    I'll help you create detailed status updates and track progress on your projects in Shortcut. Let's gather information about:

    1. Scope Definition:
       - Which specific epic, milestone, iteration, or set of stories do you want to report on?
       - What time period are you covering in this status update? (sprint, week, month)
       - Which teams or individuals are involved in this work?
       - Who are the stakeholders for this status update?
       - What level of detail is appropriate for your audience?

    2. Progress Assessment:
       - What stories have been completed since the last update?
       - What stories are currently in progress and what is their status?
       - What is the overall completion percentage for the epic/milestone?
       - How does the current progress compare to the original plan or timeline?
       - Are there any completed items awaiting verification or deployment?
       - What metrics or KPIs are available to quantify progress?

    3. Blockers and Challenges:
       - What current blockers or impediments exist?
       - How long have these blockers been in place?
       - What steps are being taken to resolve each blocker?
       - Are there any resource constraints affecting progress?
       - What dependencies on other teams or systems are impacting work?
       - Are there any quality or technical issues that have emerged?

    4. Risk Analysis:
       - What new risks have been identified since the last update?
       - Have any previously identified risks materialized?
       - Have risk mitigation strategies been effective?
       - Are there timeline, scope, or quality risks on the horizon?
       - Has the priority of any risks changed?
       - What contingency plans should be considered?

    5. Timeline and Forecast:
       - Is the work still on track to meet the expected completion date?
       - What is the revised forecast if the timeline has changed?
       - What factors are influencing any timeline changes?
       - Are there any upcoming milestones or deadlines to highlight?
       - What is the team's velocity and how is it trending?
       - What is the confidence level in meeting upcoming deadlines?

    6. Accomplishments and Wins:
       - What key accomplishments should be highlighted?
       - What value has been delivered to users/customers?
       - Are there any efficiency or process improvements to note?
       - Have any significant technical challenges been overcome?
       - Are there any positive metrics or feedback to share?
       - What team or individual contributions deserve recognition?

    7. Next Steps:
       - What are the priorities for the next period?
       - What specific stories will be tackled next?
       - What decisions or input is needed from stakeholders?
       - What upcoming meetings or reviews are scheduled?
       - What dependencies need to be coordinated?
       - What preparation work is needed for upcoming phases?

    Based on this information, I can help you:
    - Draft a comprehensive status update with appropriate detail level
    - Create visual progress indicators for dashboards
    - Update story statuses and comments in Shortcut
    - Document and assign action items for blockers
    - Adjust timeline forecasts based on current progress
    - Prepare briefing materials for different stakeholder groups

    I'll help organize this in Shortcut by:
    - Adding status comments to epics, milestones, or iterations
    - Updating workflow states to reflect current status
    - Creating or updating blockers with action plans
    - Tagging relevant stakeholders on important updates
    - Generating summary reports for overall health assessment
    - Creating or updating timeline indicators
    """

@mcp.prompt()
def retrospective_prompt() -> str:
    """Facilitate retrospectives to review outcomes and capture learnings"""
    return """
    I'll help you conduct an effective retrospective to review outcomes and capture valuable learnings. Let's explore:

    1. Scope and Context:
       - What specific work are we reviewing? (sprint, project, feature, milestone)
       - What timeframe are we examining?
       - Which teams or individuals contributed to this work?
       - What were the original goals, requirements, and success criteria?
       - What metrics or outcomes were we targeting?

    2. Accomplishments Review:
       - What did we successfully deliver?
       - How do the deliverables compare to the original requirements?
       - What metrics or KPIs show our impact?
       - What customer or user feedback have we received?
       - What technical achievements should we highlight?
       - What challenges did we overcome?

    3. Process Evaluation:
       - How effectively did we follow our planned process?
       - Were our estimations and timelines accurate?
       - How was our velocity compared to expectations?
       - How effective was our collaboration and communication?
       - Did we have the right skills and resources available?
       - How well did our tools and infrastructure support our needs?

    4. What Went Well:
       - Which practices or approaches proved particularly effective?
       - Where did we exceed expectations?
       - What positive team dynamics emerged?
       - What decisions turned out to be good ones?
       - What should we continue doing in future work?
       - What strengths did team members demonstrate?

    5. Challenges and Obstacles:
       - What difficulties or roadblocks did we encounter?
       - What caused delays or quality issues?
       - Where did we have communication breakdowns?
       - What technical debts were created or encountered?
       - What assumptions proved incorrect?
       - What external factors impacted our work negatively?

    6. Learning and Insights:
       - What have we learned about our users or customers?
       - What have we learned about our product?
       - What have we learned about our technical approach?
       - What have we learned about our team and how we work?
       - What have we learned about our planning and estimation?
       - What surprised us during this work?

    7. Actions and Improvements:
       - What specific changes should we make going forward?
       - What experiments should we try in our next iteration?
       - What processes need refinement?
       - What skills or knowledge gaps should we address?
       - What tools or automation could help us improve?
       - How should we adjust our planning or estimation?

    Based on this retrospective, I can help you:
    - Document key learnings and insights
    - Create actionable improvement items
    - Update team working agreements or best practices
    - Adapt estimation or planning methods for future work
    - Identify skills development needs
    - Recognize and celebrate team achievements

    I'll help organize this in Shortcut by:
    - Creating stories for action items with clear ownership
    - Documenting learnings in epics or milestone descriptions
    - Adding notes to relevant stories about process improvements
    - Creating labels for tracking recurring issues
    - Setting up metrics to monitor improvements over time
    - Establishing reminders to check on improvement progress
    """

@mcp.prompt()
def product_metrics_prompt() -> str:
    """Define and track key product metrics to measure success"""
    return """
    I'll help you define, implement, and track meaningful product metrics that measure success. Let's work through:

    1. Strategic Alignment:
       - What are your overall product and business goals?
       - What specific problems are you trying to solve for users?
       - What are your product's key value propositions?
       - What user behaviors indicate successful product adoption?
       - How does your monetization strategy relate to metrics?
       - What timeframes are most relevant for your metrics?

    2. Framework Selection:
       - Which metric framework makes sense for your product? (AARRR, HEART, North Star + supporting metrics)
       - Do you need different metrics for different user segments?
       - What leading vs. lagging indicators should you track?
       - What are your vanity metrics to avoid over-emphasizing?
       - What qualitative signals should complement your quantitative metrics?
       - How frequently should different metrics be reviewed?

    3. Core Product Metrics:
       - What is your North Star or primary success metric?
       - What acquisition metrics matter most? (new users, acquisition channels, conversion rates)
       - What activation/onboarding metrics indicate initial success? (time to value, setup completion)
       - What engagement metrics show ongoing value? (active usage, retention, feature adoption)
       - What retention metrics demonstrate stickiness? (cohort retention, churn rate)
       - What revenue metrics track business performance? (ARPU, LTV, conversion to paid)

    4. Feature-Specific Metrics:
       - What metrics should track success for specific features?
       - How do feature-level metrics roll up to product-level metrics?
       - What usage patterns indicate feature effectiveness?
       - What negative signals might indicate feature problems?
       - What A/B test metrics should evaluate feature variations?
       - How will you determine if a feature should be evolved or deprecated?

    5. User Experience Metrics:
       - What metrics capture user satisfaction? (NPS, CSAT, CES)
       - How will you measure usability? (completion rates, time-on-task)
       - What metrics indicate user friction? (error rates, support tickets)
       - How will you track performance experience? (load times, responsiveness)
       - What accessibility metrics should you monitor?
       - How will you measure user sentiment over time?

    6. Implementation Plan:
       - What data collection mechanisms are needed?
       - How will you ensure data accuracy and consistency?
       - What dashboards or reporting tools will visualize metrics?
       - Who needs access to which metrics and reports?
       - What baselines need to be established?
       - What targets or goals should be set for key metrics?

    7. Metrics Governance:
       - How often will you review and update your metrics?
       - Who is responsible for maintaining each metric?
       - How will you validate that metrics are driving right behaviors?
       - What process exists for adding or retiring metrics?
       - How will you prevent metric manipulation or gaming?
       - How will you handle conflicting metric signals?

    Based on this framework, I can help you:
    - Define a balanced metrics scorecard
    - Create implementation stories for tracking mechanisms
    - Establish baseline measurements and targets
    - Design actionable dashboards and reports
    - Set up regular metrics review cadences
    - Link metrics to specific product initiatives

    I'll help organize this in Shortcut by:
    - Creating an epic for metrics implementation
    - Defining stories for each metric tracking component
    - Setting up custom fields for metric targets and actuals
    - Adding metric success criteria to feature stories
    - Creating labels for tracking metric-driven initiatives
    - Developing templates for reporting and analysis
    """

@mcp.prompt()
def release_planning_prompt() -> str:
    """Plan releases with proper scope and timing"""
    return """
    I'll help you plan a well-structured release with the right scope and timing. Let's work through:

    1. Release Objectives:
       - What are the primary goals for this release?
       - What user problems will this release solve?
       - What business outcomes should this release drive?
       - How does this release align with product strategy?
       - What is the theme or narrative for this release?
       - What success metrics will measure the impact of this release?

    2. Scope Definition:
       - What features or enhancements are candidates for this release?
       - What are the must-have vs. nice-to-have items?
       - What critical bugs or technical debt should be addressed?
       - What dependencies exist between different scope items?
       - What can be deferred to future releases?
       - How much buffer should we include for unexpected work?

    3. Timeline Planning:
       - What is the target release date?
       - What are the key milestones leading to release?
       - What development capacity is available for this release?
       - How much time is needed for testing and stabilization?
       - What external deadlines or events should we consider?
       - What is the critical path for this release?

    4. Resource Allocation:
       - Which teams or individuals need to contribute?
       - What specialized skills are required for specific components?
       - Are there any resource constraints or competing priorities?
       - What external dependencies or partners are involved?
       - What tools or environments need to be available?
       - Do we need any additional resources for this release?

    5. Risk Assessment:
       - What are the highest risk components of this release?
       - What technical challenges might cause delays?
       - What testing challenges should we anticipate?
       - What market or competitive risks should we consider?
       - What stakeholder or user adoption risks exist?
       - What contingency plans should we have ready?

    6. Quality Assurance Planning:
       - What testing approach is appropriate for this release?
       - What test environments will be needed?
       - What types of testing should be conducted? (functional, performance, security, etc.)
       - What test data will be required?
       - What automation can accelerate testing?
       - What acceptance criteria must be met before release?

    7. Release Process:
       - What deployment approach will be used? (big bang, phased, canary, etc.)
       - What approvals are needed before release?
       - What documentation needs to be prepared?
       - What communication plans should be in place?
       - What post-release monitoring is needed?
       - What rollback procedures should be defined?

    8. Stakeholder Communication:
       - Who needs to be informed about this release?
       - What training or enablement is required?
       - What marketing or promotional activities are planned?
       - How will user feedback be collected post-release?
       - What customer support preparation is needed?
       - How will release notes be communicated?

    Based on this planning, I can help you:
    - Create a structured release plan with clear milestones
    - Prioritize the backlog for this release
    - Identify critical dependencies and risks
    - Define quality gates and acceptance criteria
    - Create a communication plan for stakeholders
    - Set up monitoring for post-release success

    I'll help organize this in Shortcut by:
    - Creating a release milestone with target date
    - Linking relevant epics and stories to the release
    - Setting up iteration planning for the release timeline
    - Adding release criteria to stories and epics
    - Creating labels for tracking release readiness
    - Setting up custom fields for release status tracking
    - Establishing a release dashboard for monitoring progress
    """

@mcp.prompt()
def prioritization_workshop_prompt() -> str:
    """Facilitate structured prioritization decisions"""
    return """
    I'll help you facilitate a structured prioritization workshop to make more effective decisions about what to build next. Let's work through:

    1. Preparation and Context:
       - What items need to be prioritized? (features, epics, stories, bugs, tech debt)
       - Who are the key stakeholders that should participate in prioritization?
       - What time horizon are we prioritizing for? (next sprint, quarter, year)
       - What context do participants need before the workshop? (market data, customer feedback, technical constraints)
       - What are the current strategic priorities or themes?
       - What resource constraints do we need to consider?

    2. Prioritization Framework Selection:
       - Which prioritization framework best fits your needs? Options include:
         * Value vs. Effort (2x2 matrix)
         * RICE (Reach, Impact, Confidence, Effort)
         * Kano Model (Basic, Performance, Excitement features)
         * MoSCoW (Must, Should, Could, Won't)
         * Weighted Scoring
         * Buy a Feature
         * ICE (Impact, Confidence, Ease)
       - What custom criteria or scoring system makes sense for your product?
       - How will you weight different factors in your decision-making?

    3. Data and Evidence Collection:
       - What user data should inform these decisions?
       - What business metrics are relevant to prioritization?
       - What user feedback supports various options?
       - What competitive intelligence should be considered?
       - What technical constraints or dependencies exist?
       - What level of estimation is needed for each item?

    4. Stakeholder Input Gathering:
       - How will different perspectives be represented?
       - How will you ensure voices from different functions are heard? (engineering, design, marketing, sales, support)
       - What structured format will you use to gather input?
       - How will you quantify subjective assessments? (anonymous voting, dot voting, linear scales)
       - How will you handle disagreements or conflicting priorities?
       - What biases might affect the process and how will you mitigate them?

    5. Evaluation Process:
       - How will each item be presented and discussed?
       - What specific questions should be answered for each item?
       - What scoring or voting mechanism will you use?
       - How will you ensure consistent evaluation across items?
       - How will you handle items with dependencies or interrelationships?
       - What time boxing will keep the process efficient?

    6. Decision Making Mechanism:
       - How will final decisions be made after evaluation?
       - Who has decision-making authority for final prioritization?
       - How will you handle conflicts or close calls?
       - What veto rights or escalation paths exist?
       - How will you document the rationale behind decisions?
       - What happens with items that aren't prioritized now?

    7. Communication and Follow-through:
       - How will you communicate priorities to the wider team?
       - How will you track if higher priority items achieve better outcomes?
       - When will the next prioritization review occur?
       - What would trigger a reprioritization before the scheduled review?
       - How will you capture learning from previous prioritization decisions?
       - How will you communicate changes to stakeholders?

    Based on this workshop, I can help you:
    - Create a structured prioritization framework
    - Document decision criteria and evaluation methodology
    - Capture stakeholder inputs systematically
    - Facilitate consensus building
    - Create visualizations of priority order
    - Document rationale for future reference
    - Establish a regular cadence for re-evaluation

    I'll help organize this in Shortcut by:
    - Creating labeled priority tiers for stories
    - Setting up custom fields for priority scores
    - Documenting prioritization rationale in descriptions
    - Creating a prioritization epic with associated stories
    - Setting up iteration planning based on priorities
    - Adding priority labels to the backlog
    - Creating dashboard views filtered by priority
    """

@mcp.prompt()
def estimation_prompt() -> str:
    """Help with story point estimation"""
    return """
    I'll help you implement effective story point estimation for your team. Let's work through:

    1. Estimation System Setup:
       - What estimation scale will you use? (Fibonacci, T-shirt sizes, Powers of 2, etc.)
       - What does each point value represent in your system?
       - Do you want to establish reference stories for each point value?
       - Will you estimate absolute size/complexity or relative to other stories?
       - What is your team's current velocity (if known)?
       - Are there certain types of work you'll estimate differently? (bugs, tech debt, research)

    2. Complexity Factors Assessment:
       - What technical complexity factors should be considered?
       - What uncertainty factors influence complexity?
       - What cross-team dependencies affect estimates?
       - What external systems integration affects estimates?
       - How does testing complexity factor in?
       - What deployment or rollout complexity should be considered?

    3. Estimation Workshop Structure:
       - Who should participate in estimation sessions?
       - What preparation is needed before estimation?
       - How frequently will you hold estimation sessions?
       - What format works best? (Planning Poker, Team Estimation Game, Affinity Mapping)
       - How much time will be allocated for discussion per story?
       - What information must be available for each story being estimated?

    4. Consensus Building Process:
       - How will you handle estimation disagreements?
       - What discussion format helps resolve estimate differences?
       - When will you split stories that are too large?
       - How will you document assumptions that influenced estimates?
       - What threshold of difference requires deeper discussion?
       - How will you prevent anchoring bias or dominant voices?

    5. Confidence and Risk Assessment:
       - How will you indicate confidence levels in estimates?
       - When should stories be flagged for re-estimation?
       - How will you handle items with significant unknowns?
       - What spikes or research tasks should precede uncertain estimates?
       - How will you track estimate accuracy over time?
       - What threshold constitutes a significant estimation miss?

    6. Velocity Calculation:
       - How will you calculate and track team velocity?
       - What time period will you use for velocity calculations? (sprint, moving average)
       - How will you handle outliers in velocity data?
       - What factors might temporarily affect velocity?
       - How will you use velocity for capacity planning?
       - When will you recalibrate velocity assumptions?

    7. Estimation Refinement:
       - How often will you review estimation accuracy?
       - What metrics indicate your estimation system needs adjustment?
       - How will you incorporate learning from past estimations?
       - When should the team recalibrate its understanding of point values?
       - What ceremonies will include estimation review?
       - How will you improve estimation consistency over time?

    Based on these discussions, I can help you:
    - Set up a consistent estimation framework
    - Facilitate estimation sessions
    - Document estimation guidelines
    - Track velocity and estimation accuracy
    - Identify stories needing more refinement
    - Build consensus on complex estimates
    - Improve estimation precision over time

    I'll help organize this in Shortcut by:
    - Setting up custom fields for estimates
    - Adding estimation notes to story descriptions
    - Creating template checklists for estimation factors
    - Tracking velocity with labels and iterations
    - Documenting reference stories for each point value
    - Creating dashboards for estimation accuracy
    - Setting up workflows for stories needing re-estimation
    """

@mcp.prompt()
def dependency_mapping_prompt() -> str:
    """Identify and manage dependencies"""
    return """
    I'll help you identify, document, and manage dependencies across your product work. Let's explore:

    1. Dependency Identification:
       - What types of work items need dependency mapping? (epics, stories, features)
       - What internal team dependencies exist across the work?
       - What cross-team dependencies should be tracked?
       - What external or third-party dependencies impact your timelines?
       - What system or infrastructure dependencies are relevant?
       - What data or API dependencies influence your development?
       - What design or UX dependencies need coordination?

    2. Dependency Classification:
       - Which dependencies are hard blockers vs. soft dependencies?
       - Which dependencies are one-way vs. bidirectional?
       - Which dependencies are technical vs. business/stakeholder-related?
       - Which dependencies are within your control vs. external factors?
       - How would you rank dependencies by risk level?
       - Which dependencies have fixed dates vs. flexible timing?
       - Which dependencies are sequential vs. those that can be worked in parallel?

    3. Dependency Documentation:
       - What level of detail is needed for each dependency?
       - How will you document the nature and conditions of each dependency?
       - How will you track the status of each dependency?
       - Who are the key contacts or owners for each dependency?
       - What expected resolution dates should be recorded?
       - What assumptions underlie each dependency?
       - How will you visualize the dependency network?

    4. Timeline and Sequencing:
       - What is the critical path through your dependency network?
       - What is the optimal sequence for resolving dependencies?
       - How do dependencies affect overall project timelines?
       - What buffer should be built in for dependency resolution?
       - What dependencies create the highest risk of delays?
       - How will schedule changes affect the dependency chain?
       - What parallel work streams can progress independently?

    5. Dependency Management:
       - How frequently will you review dependency status?
       - What escalation process exists for at-risk dependencies?
       - How will you communicate dependency updates to stakeholders?
       - What contingency plans exist for broken dependencies?
       - Who has authority to reprioritize work based on dependencies?
       - How will you handle conflicting dependencies across teams?
       - What metrics will track dependency health?

    6. Risk Mitigation Strategies:
       - How can you reduce the number of critical dependencies?
       - What alternatives exist if key dependencies aren't resolved on time?
       - How can you build modularity to isolate dependency impacts?
       - What early warning indicators will flag dependency risks?
       - How can you structure work to resolve high-risk dependencies early?
       - What technical approaches can decouple tightly coupled components?
       - What process improvements would reduce dependency-related delays?

    7. Governance and Review:
       - Who should participate in dependency planning sessions?
       - What regular forums will address dependency management?
       - How will lessons learned be incorporated into future dependency planning?
       - What role do different stakeholders play in managing dependencies?
       - What dependency patterns should inform architectural decisions?
       - How will dependency management effectiveness be evaluated?

    Based on this mapping, I can help you:
    - Create a comprehensive dependency map
    - Establish dependency tracking systems
    - Identify critical path dependencies
    - Develop risk mitigation strategies
    - Schedule work to optimize for dependencies
    - Create communication plans for dependency management
    - Design escalation processes for dependency issues

    I'll help organize this in Shortcut by:
    - Setting up dependency relationships between stories
    - Creating custom fields for dependency types and status
    - Establishing blockers with clear ownership
    - Adding dependency information to story descriptions
    - Creating dependency-focused iterations or milestones
    - Setting up dashboard views filtered by dependency status
    - Creating labels for different dependency categories
    - Documenting dependency resolution criteria
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