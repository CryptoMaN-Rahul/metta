import os
import sys
import webbrowser
import subprocess
import time
import signal
import platform
from pathlib import Path

def start_server():
    """Start the FastAPI server"""
    print("Starting the server...")
    
    # Determine the Python executable to use
    python_cmd = sys.executable
    
    # Start the server as a subprocess
    server_process = subprocess.Popen(
        [python_cmd, "src/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for the server to start
    print("Waiting for server to start...")
    time.sleep(3)  # Give the server a few seconds to start
    
    return server_process

def open_demo():
    """Open the demo interface in a web browser"""
    # Get the absolute path to the demo.html file
    demo_path = os.path.abspath("demo.html")
    
    # Convert to file:// URL
    if platform.system() == 'Windows':
        demo_url = f"file:///{demo_path.replace(os.sep, '/')}"
    else:
        demo_url = f"file://{demo_path}"
    
    print(f"Opening demo interface: {demo_url}")
    webbrowser.open(demo_url)

def main():
    """Main function to start the demo"""
    print("Starting Domain-Specific FAQ Chatbot Demo")
    print("----------------------------------------")
    
    # Check if the server is already running
    try:
        import requests
        response = requests.get("http://localhost:9009/docs")
        if response.status_code == 200:
            print("Server is already running.")
            server_process = None
        else:
            server_process = start_server()
    except:
        server_process = start_server()
    
    # Open the demo interface
    open_demo()
    
    if server_process:
        print("\nServer is running. Press Ctrl+C to stop the demo.")
        try:
            # Keep the script running until interrupted
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping the server...")
            # Kill the server process
            if platform.system() == 'Windows':
                server_process.terminate()
            else:
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
            print("Server stopped.")
    else:
        print("\nDemo is running with an existing server instance.")
        print("Close your browser when done.")

if __name__ == "__main__":
    main() 