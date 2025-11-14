#!/usr/bin/env python3
"""
Main application entry point for the Agent Framework
This file serves as a backup/alternative way to run the application
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def setup_environment():
    """Setup environment variables from template if .env doesn't exist"""
    env_file = Path(".env")
    env_template = Path("env.template")
    
    if not env_file.exists() and env_template.exists():
        print("Creating .env file from template...")
        with open(env_template, 'r') as template:
            content = template.read()
        
        with open(env_file, 'w') as env:
            env.write(content)
        
        print("Please edit .env file with your actual configuration values")
        return False
    
    return True

def check_agents_directory():
    """Ensure agents directory exists with sample agents"""
    agents_dir = Path("agents")
    
    if not agents_dir.exists():
        print("Agents directory not found. Creating sample structure...")
        agents_dir.mkdir(exist_ok=True)
        return False
    
    # Check if we have any agents
    agent_configs = list(agents_dir.glob("*/config.yaml"))
    if not agent_configs:
        print("No agent configurations found in agents directory")
        return False
    
    print(f"Found {len(agent_configs)} agent configurations:")
    for config in agent_configs:
        print(f"  - {config.parent.name}")
    
    return True

def run_devui(args):
    """Run the devui command with specified arguments"""
    # Default values
    entities_dir = args.entities_dir or os.getenv('ENTITIES_DIR', './agents')
    host = args.host or os.getenv('HOST', '0.0.0.0')
    port = args.port or os.getenv('PORT', '8080')
    mode = args.mode or os.getenv('MODE', 'user')
    
    # Build command
    cmd = [
        'devui',
        entities_dir,
        '--host', host,
        '--port', str(port),
        '--mode', mode
    ]
    
    if args.auth or os.getenv('AUTH_ENABLED', 'true').lower() == 'true':
        cmd.append('--auth')
    
    print(f"Starting Agent Framework DevUI...")
    print(f"Command: {' '.join(cmd)}")
    print(f"Access URL: http://{host}:{port}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running devui: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Agent Framework Application')
    parser.add_argument('--entities-dir', help='Path to agents directory')
    parser.add_argument('--host', help='Host to bind to')
    parser.add_argument('--port', type=int, help='Port to bind to')
    parser.add_argument('--mode', choices=['user', 'admin'], help='Application mode')
    parser.add_argument('--auth', action='store_true', help='Enable authentication')
    parser.add_argument('--setup-only', action='store_true', help='Only setup environment, don\'t run')
    
    args = parser.parse_args()
    
    print("=== Agent Framework Startup ===")
    
    # Setup environment
    if not setup_environment() and not args.setup_only:
        print("Environment setup required. Run with --setup-only to create .env file only.")
        sys.exit(1)
    
    if args.setup_only:
        print("Environment setup complete.")
        return
    
    # Check agents directory
    if not check_agents_directory():
        print("Agents directory setup required.")
        sys.exit(1)
    
    # Run the application
    run_devui(args)

if __name__ == "__main__":
    main()
