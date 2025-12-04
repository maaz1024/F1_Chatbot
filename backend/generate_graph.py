import os
import sys
    
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agent.graph import agent_runner
except ImportError:
    print("Could not import agent_runner. Make sure your graph variable in agent/graph.py is named 'agent_runner'.")
    sys.exit(1)

def generate_png():
    print("Generating graph.png...")
    try:
        # Generate the mermaid PNG binary data
        png_data = agent_runner.get_graph().draw_mermaid_png()
        
        # Save to file
        output_path = "graph.png"
        with open(output_path, "wb") as f:
            f.write(png_data)
        
        print(f"Successfully saved graph to {os.path.abspath(output_path)}")
        print("You can now move this file to your root directory or assets folder for the README.")
        
    except Exception as e:
        print(f"Error generating graph: {e}")
        print("Ensure you have 'langgraph' installed.")

if __name__ == "__main__":
    generate_png()