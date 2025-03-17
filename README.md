# Shortcut Product Manager MCP

A Model Context Protocol (MCP) server that acts as a virtual Product Manager using the Shortcut API, enabling AI assistants to help manage your entire product development lifecycle.

## Overview

The Shortcut Product Manager MCP enables AI assistants like Claude to perform comprehensive product management functions through the [Shortcut API](https://shortcut.com/api/). This integration effectively replaces or augments a human Product Manager by:

- Creating and managing product backlogs with proper prioritization
- Planning sprints and releases based on team capacity and business priorities
- Writing detailed feature specifications and acceptance criteria
- Analyzing user feedback and market research to inform product decisions
- Tracking product metrics and measuring feature impact
- Creating tailored stakeholder updates and status reports
- Facilitating team ceremonies like backlog refinement and retrospectives
- Managing dependencies and team workloads
- Organizing product roadmaps and strategic planning

## Installation

### Prerequisites

- Python 3.8 or higher
- `pip` package manager
- A Shortcut account with API access

### Setup

1. Clone the repository or download the source code:

   ```bash
   git clone https://github.com/yourusername/mcp-shortcut.git
   cd mcp-shortcut
   ```

2. Install dependencies:

   ```bash
   pip install mcp httpx
   ```

3. Set up your Shortcut API token:

   ```bash
   export SHORTCUT_API_TOKEN=your_api_token_here
   ```

   You can find your API token in Shortcut under Settings > API Tokens.

4. Run the server:
   ```bash
   python server-v2.py
   ```

### MCP CLI Integration

For enhanced functionality with the MCP CLI:

1. Install the MCP CLI:

   ```bash
   pip install "mcp[cli]"
   ```

2. Run in development mode to test with the MCP Inspector:

   ```bash
   mcp dev server-v2.py
   ```

3. Install in Claude Desktop:
   ```bash
   mcp install server-v2.py
   ```

## Product Management Features

### Strategic Planning & Roadmapping

- **Feature Specification**: Create comprehensive specifications for new features
- **Roadmap Planning**: Develop strategic roadmaps with themes, epics, and milestones
- **Market Research**: Organize competitive analysis and market trends
- **Feature Impact Analysis**: Evaluate potential impact before committing to build
- **Product Metrics**: Define and track key performance indicators

### Sprint & Release Management

- **Sprint Planning**: Create balanced sprint plans based on velocity and priorities
- **Release Planning**: Plan releases with proper scope and timeline
- **Dependency Mapping**: Identify and manage dependencies between work items
- **Team Workload Analysis**: Balance work across team members
- **Status Updates**: Generate stakeholder-specific updates on progress

### Backlog Management

- **Story Creation**: Create well-structured user stories
- **Backlog Refinement**: Organize and prioritize the product backlog
- **Prioritization Workshops**: Facilitate structured prioritization sessions
- **Bug Reporting**: Create detailed, actionable bug reports
- **Acceptance Criteria**: Define clear, testable acceptance criteria

### Team Facilitation

- **Retrospectives**: Guide data-driven sprint or project retrospectives
- **Estimation**: Assist with story point estimation
- **Ticket Triage**: Prioritize and categorize incoming work
- **User Feedback Analysis**: Analyze and categorize user feedback

## Using the Product Manager MCP

### Product Strategy & Vision

Ask the MCP to help with strategic planning:

```
I need to create a 6-month product roadmap focused on improving user retention. Can you help me organize this in Shortcut?
```

The MCP will guide you through creating a structured roadmap with proper epics and milestones.

### Feature Planning

Get help creating detailed feature specifications:

```
I need to write a specification for our new "Team Collaboration" feature. Can you help me create this and break it down into stories?
```

### Sprint Management

Plan and track sprints:

```
We're planning our next two-week sprint starting Monday. Our velocity is about 30 points per sprint, and we want to focus on the Payment Processing epic. Help me create a balanced sprint plan.
```

### Prioritization

Facilitate prioritization decisions:

```
I need to prioritize the 20 items in our backlog for next quarter. Can you help me run a RICE prioritization workshop?
```

### User Feedback & Market Analysis

Process user input:

```
We've received 50 feedback items from our recent user survey about the checkout process. Can you help categorize them and identify key themes?
```

### Status Reporting

Generate appropriate stakeholder updates:

```
I need to create an executive summary of our product progress for the last month, focusing on our three main initiatives: user onboarding, payment processing, and analytics dashboards.
```

## Prompt Templates

The MCP includes specialized prompt templates for common Product Management activities:

### Strategic Activities

- `feature_specification_prompt`: Write detailed feature specifications
- `roadmap_planning_prompt`: Plan strategic product roadmaps
- `feature_impact_analysis_prompt`: Analyze potential impact of new features
- `market_research_prompt`: Organize competitive and market research
- `product_metrics_prompt`: Define and track key product metrics

### Planning Activities

- `sprint_planning_prompt`: Plan upcoming sprints with balanced work
- `release_planning_prompt`: Plan releases with proper scope and timing
- `prioritization_workshop_prompt`: Facilitate structured prioritization decisions
- `estimation_prompt`: Help with story point estimation
- `dependency_mapping_prompt`: Identify and manage dependencies

### Team & Process Activities

- `retrospective_prompt`: Guide data-driven retrospectives
- `backlog_refinement_prompt`: Organize and prioritize the backlog
- `team_workload_prompt`: Analyze and balance team workloads
- `ticket_triage_prompt`: Prioritize and categorize incoming work

### User-Focused Activities

- `user_feedback_analysis_prompt`: Analyze and categorize user feedback
- `acceptance_criteria_prompt`: Write clear, testable acceptance criteria
- `bug_report_prompt`: Create detailed bug reports

### Communication Activities

- `status_update_prompt`: Generate comprehensive status updates
- `stakeholder_update_prompt`: Create tailored stakeholder communications

## API Reference

### Resource Parameters

- `story_id` - ID of a Shortcut story
- `epic_id` - ID of a Shortcut epic
- `milestone_id` - ID of a Shortcut milestone
- `project_id` - ID of a Shortcut project
- `member_id` - ID of a Shortcut member

### Key Tool Parameters

#### Create Story

- `name` - The name of the story (required)
- `description` - The description of the story (markdown supported)
- `project_id` - The ID of the project to add the story to
- `workflow_state_id` - The ID of the workflow state
- `epic_id` - The ID of the epic to add the story to
- `estimate` - The estimate value for the story

#### Update Story

- `story_id` - The ID of the story to update (required)
- `name` - The new name of the story
- `description` - The new description of the story
- `project_id` - The ID of the project to move the story to
- `workflow_state_id` - The ID of the workflow state to move the story to
- `epic_id` - The ID of the epic to add the story to
- `estimate` - The estimate value for the story

#### Create Epic

- `name` - The name of the epic (required)
- `description` - The description of the epic (markdown supported)
- `milestone_id` - The ID of the milestone to add the epic to

#### Create Task

- `story_id` - The ID of the story to add the task to (required)
- `description` - The description of the task (required)
- `complete` - Whether the task is complete
- `owner_ids` - List of member UUIDs to assign as owners

#### Search Stories

- `query` - The search query using Shortcut's search syntax

## Product Management Workflows

The MCP supports common product management workflows:

### Product Discovery to Delivery

1. Start with `market_research_prompt` to understand the competitive landscape
2. Use `user_feedback_analysis_prompt` to identify user needs
3. Apply `feature_impact_analysis_prompt` to evaluate potential solutions
4. Create specifications with `feature_specification_prompt`
5. Break down work into stories and set criteria with `acceptance_criteria_prompt`
6. Plan implementation with `sprint_planning_prompt`
7. Track progress with `status_update_prompt`
8. Review outcomes with `retrospective_prompt`

### Quarterly Planning

1. Begin with `roadmap_planning_prompt` to set direction
2. Use `prioritization_workshop_prompt` to rank initiatives
3. Create epics and milestones for key initiatives
4. Break down near-term work with `backlog_refinement_prompt`
5. Establish metrics with `product_metrics_prompt`
6. Create a reporting cadence with `stakeholder_update_prompt`

## Error Handling

The server handles common errors including:

- Authentication failures due to invalid API tokens
- Resource not found errors (404)
- Permission issues
- Rate limiting
- Validation errors when creating or updating items

If you encounter errors, check that:

1. Your API token is valid and has the necessary permissions
2. The IDs you're using for stories, epics, etc. exist in your workspace
3. Your request data follows Shortcut's required format

## Security Considerations

The Shortcut API token provides complete access to your Shortcut workspace. To maintain security:

1. Never commit your API token to version control
2. Use environment variables to store your token
3. Grant access only to trusted users
4. Regularly rotate your API tokens

## License

This MCP server is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
