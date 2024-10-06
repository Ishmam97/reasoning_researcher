import os

def save_output_to_markdown(content, agent_name, output_dir):
    """Save the agent's output to a markdown file."""
    # Create a markdown filename based on agent name
    file_path = os.path.join(output_dir, f"{agent_name}_output.md")
    
    # Write the content to the markdown file
    with open(file_path, "w") as file:
        file.write(f"# {agent_name} Output\n\n")
        file.write(content)