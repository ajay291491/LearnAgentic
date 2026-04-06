### What is AI Agents ?
Basic building block of agentic is; 
- its ability to use LLM to augment the retrival from input, 
- process them using a tool and them store the state using memory 
- and finally provide the output based on the input.

![img.png](Images/What_is_agentic.png)

AI Agents are programs where LLM outputs control the workflow

1. Multiple LLM calls
2. LLM with ability to use tools
3. An environment where LLMs interact 
4. A Planner to coordinate activities
5. Autonomy 

Reference - Anthropic Guide for Agentic - https://www.anthropic.com/engineering/building-effective-agents

### Key Agentic Concepts

- Agents
- Workflows 
- MCP 

### What are Different workflows 
#### Chaining Workflow
  - Here each input goes through a LLM call then we will have a backend check to validate its on track and direct it to next step
  - This can be used when task can be easily decomposed into fixed sub-tasks, more like if then conditions  
![img.png](Images/Chaining_workflow.png)

#### Routing Workflow - 
- Routing classifies an input and direct it to a specialized followup task
- This workflow allows more seperation of concerns and building more specialized prompts.
- Without optimizing this routing input for one workflow can hurt others 
![img.png](Images/routingWorkflow.png)

#### Workflow Parallelization 
- Here it can execute multple workflows in parallel and aggregates their input into one.
- This comes with two main sub strem process 
  - sectioning - Breaking down one single task into multiple sub-tasks
  - voting - Running same tasks multiple times to get diverse outputs 
- Parallelization is effective when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher confidence results.
  ![img.png](Images/WorkflowParallelization.png)

#### Workflow Orchestrator
- In this concept a central LLL dynamically breakdown tasks into multiple and then delegates into multiple LLMs
- Then these multiple LLMs process the individual workflows assigned to them 
- Finally all output will be synchorized by another LLM 
![img.png](Images/Orchestrator.png)

#### Evaluator and Optimizer 
- In this architecture one LLM creates responses 
- Another one repeatedly evaluates the response being created 

![img.png](Images/evaluator_Optimizer.png)





