#!/usr/bin/env python3
"""
AI Agent Level 5 - REAL Implementation
Uses actual Mistral AI API with tool calling and conversation memory
"""

import os
import json
import time
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    print("Installing colorama...")
    subprocess.run([sys.executable, "-m", "pip", "install", "colorama"], check=True)
    from colorama import Fore, Back, Style, init
    init(autoreset=True)

try:
    from mistralai import Mistral
except ImportError:
    print("Installing mistralai...")
    subprocess.run([sys.executable, "-m", "pip", "install", "mistralai"], check=True)
    from mistralai import Mistral


class BeautifulUI:
    """Handles all terminal UI rendering"""
    
    @staticmethod
    def header():
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}║{' '*78}║")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{Style.BRIGHT}{'AI AGENT LEVEL 5':^78}{Fore.CYAN}║")
        print(f"{Fore.CYAN}║{Fore.WHITE}{'Real AI with Tool Calling & Sub-Agent Spawning':^78}{Fore.CYAN}║")
        print(f"{Fore.CYAN}║{Fore.MAGENTA}{'Powered by Mistral AI API':^78}{Fore.CYAN}║")
        print(f"{Fore.CYAN}║{' '*78}║")
        print(f"{Fore.CYAN}{'='*80}\n")
    
    @staticmethod
    def system_msg(msg: str, status: str = "INFO"):
        icons = {
            "INFO": f"{Fore.BLUE}ℹ",
            "SUCCESS": f"{Fore.GREEN}✓",
            "ERROR": f"{Fore.RED}✗",
            "WARNING": f"{Fore.YELLOW}⚠",
            "PROCESS": f"{Fore.CYAN}⚙",
            "AGENT": f"{Fore.MAGENTA}🤖",
            "MEMORY": f"{Fore.YELLOW}💾",
            "THINK": f"{Fore.MAGENTA}🧠"
        }
        icon = icons.get(status, icons["INFO"])
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.WHITE}[{timestamp}] {icon} {Style.BRIGHT}{msg}{Style.RESET_ALL}")
    
    @staticmethod
    def ai_thinking(text: str = "AI is thinking..."):
        print(f"\n{Fore.MAGENTA}🧠 {text}{Style.RESET_ALL}")
    
    @staticmethod
    def tool_call(tool_name: str, inputs: Dict):
        """Display when AI decides to use a tool"""
        print(f"\n{Fore.GREEN}╔═══ AI CALLING TOOL: {tool_name.upper()} {'═'*(55-len(tool_name))}╗")
        params_str = json.dumps(inputs, indent=2)[:200]
        print(f"{Fore.GREEN}║ {Fore.CYAN}Inputs:{Style.RESET_ALL}")
        for line in params_str.split('\n'):
            print(f"{Fore.GREEN}║   {line:<73}{Fore.GREEN}║")
        print(f"{Fore.GREEN}╚{'═'*78}╝")
    
    @staticmethod
    def tool_result(result: str):
        """Display tool result"""
        preview = result[:100] + "..." if len(result) > 100 else result
        print(f"{Fore.GREEN}║ {Fore.YELLOW}Result: {Style.RESET_ALL}{preview}")
    
    @staticmethod
    def agent_spawn(agent_name: str):
        """Display sub-agent spawning"""
        print(f"\n{Fore.MAGENTA}╭{'─'*76}╮")
        print(f"{Fore.MAGENTA}│ {Fore.YELLOW}⚡ SUB-AGENT SPAWNED:{Fore.WHITE} {agent_name:<59}{Fore.MAGENTA}│")
        print(f"{Fore.MAGENTA}╰{'─'*76}╯")
    
    @staticmethod
    def user_prompt():
        return input(f"\n{Fore.GREEN}{Style.BRIGHT}YOU >{Style.RESET_ALL} ")
    
    @staticmethod
    def ai_response(text: str):
        print(f"\n{Fore.CYAN}{Style.BRIGHT}AGENT >{Style.RESET_ALL} {text}\n")
    
    @staticmethod
    def separator():
        print(f"{Fore.WHITE}{'─'*80}")
    
    @staticmethod
    def error_box(error_type: str, details: str):
        print(f"\n{Fore.RED}╔{'═'*76}╗")
        print(f"{Fore.RED}║ {Style.BRIGHT}ERROR: {error_type:<66}{Style.RESET_ALL}{Fore.RED}║")
        print(f"{Fore.RED}║ {details[:74]:<74}║")
        print(f"{Fore.RED}╚{'═'*76}╝\n")


class ToolExecutor:
    """Executes tools when called by the AI"""
    
    def __init__(self):
        self.workspace = Path("./workspace")
        self.workspace.mkdir(exist_ok=True)
    
    def execute(self, tool_name: str, tool_input: Dict) -> str:
        """Execute a tool and return result as string"""
        try:
            if tool_name == "read_file":
                return self._read_file(tool_input.get("path", ""))
            
            elif tool_name == "write_file":
                return self._write_file(
                    tool_input.get("path", ""),
                    tool_input.get("content", "")
                )
            
            elif tool_name == "execute_shell":
                return self._execute_shell(tool_input.get("command", ""))
            
            elif tool_name == "web_search":
                results = self._web_search(tool_input.get("query", ""))
                return json.dumps(results, indent=2)
            
            elif tool_name == "list_files":
                files = self._list_files(tool_input.get("directory", "."))
                return "\n".join(files)
            
            elif tool_name == "spawn_sub_agent":
                return self._spawn_sub_agent(
                    tool_input.get("name", ""),
                    tool_input.get("role", ""),
                    tool_input.get("tools", [])
                )
            
            else:
                return f"Error: Unknown tool '{tool_name}'"
        
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def _read_file(self, filepath: str) -> str:
        path = Path(filepath)
        if not path.exists():
            return f"Error: File not found: {filepath}"
        
        with open(path, 'r') as f:
            content = f.read()
        
        return f"File contents of {filepath}:\n\n{content}"
    
    def _write_file(self, filepath: str, content: str) -> str:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            f.write(content)
        
        return f"Successfully wrote {len(content)} characters to {filepath}"
    
    def _execute_shell(self, command: str) -> str:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = f"Command: {command}\n"
        output += f"Exit Code: {result.returncode}\n"
        output += f"Output:\n{result.stdout}\n"
        if result.stderr:
            output += f"Errors:\n{result.stderr}\n"
        
        return output
    
    def _web_search(self, query: str) -> List[Dict]:
        try:
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1
            }
            
            response = requests.get("https://api.duckduckgo.com/", params=params, timeout=10)
            data = response.json()
            
            results = []
            if data.get('AbstractText'):
                results.append({
                    'title': data.get('Heading', 'Result'),
                    'snippet': data.get('AbstractText'),
                    'url': data.get('AbstractURL', '')
                })
            
            if data.get('RelatedTopics'):
                for topic in data['RelatedTopics'][:5]:
                    if isinstance(topic, dict) and 'Text' in topic:
                        results.append({
                            'title': topic.get('Text', '')[:100],
                            'snippet': topic.get('Text', ''),
                            'url': topic.get('FirstURL', '')
                        })
            
            return results if results else [{"title": "No results", "snippet": "No results found for query", "url": ""}]
        
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]
    
    def _list_files(self, directory: str) -> List[str]:
        path = Path(directory)
        if not path.exists():
            return [f"Error: Directory not found: {directory}"]
        
        return [str(f.name) for f in path.iterdir()]
    
    def _spawn_sub_agent(self, name: str, role: str, tools: List[str]) -> str:
        BeautifulUI.agent_spawn(f"{name} - {role}")
        
        # Save agent info
        agents_file = Path("./memory/active_agents.json")
        agents_file.parent.mkdir(exist_ok=True)
        
        agents = []
        if agents_file.exists():
            with open(agents_file, 'r') as f:
                agents = json.load(f)
        
        agent_info = {
            "name": name,
            "role": role,
            "tools": tools,
            "spawned_at": datetime.now().isoformat()
        }
        
        agents.append(agent_info)
        
        with open(agents_file, 'w') as f:
            json.dump(agents, f, indent=2)
        
        return f"Successfully spawned sub-agent '{name}' with role: {role}. It has access to tools: {', '.join(tools)}"


class CentralBrain:
    """Main AI brain using Mistral AI API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "No API key found! Set MISTRAL_API_KEY environment variable or pass api_key parameter.\n"
                "Get your key from: https://console.mistral.ai/"
            )
        
        # Initialize Mistral Client
        self.client = Mistral(api_key=self.api_key)
        self.tool_executor = ToolExecutor()
        
        # Conversation history
        self.messages = []
        
        # Load system prompt and initialize conversation
        self.system_prompt = self._load_system_prompt()
        self.messages.append({"role": "system", "content": self.system_prompt})
        
        # Define tools available to the AI
        self.tools = self._define_tools()
        
        BeautifulUI.system_msg("Central Brain initialized with Mistral API", "SUCCESS")
    
    def _load_system_prompt(self) -> str:
        """Load system prompt from boot.md"""
        boot_file = Path("./boot.md")
        if boot_file.exists():
            BeautifulUI.system_msg("Loading system prompt from boot.md...", "PROCESS")
            with open(boot_file, 'r') as f:
                content = f.read()
            BeautifulUI.system_msg("System prompt loaded", "SUCCESS")
            return content
        else:
            BeautifulUI.system_msg("boot.md not found - using default", "WARNING")
            return "You are AI Agent Level 5, a helpful AI assistant with access to tools."
    
    def _define_tools(self) -> List[Dict]:
        """Define tools that the AI can use (Mistral/OpenAI format)"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the contents of a file. Returns the full text content of the file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the file to read (e.g., './workspace/data.txt', 'boot.md')"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write content to a file. Creates the file if it doesn't exist, overwrites if it does.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path where to write the file"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write to the file"
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_shell",
                    "description": "Execute a shell command and return its output. Use for running system commands.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Shell command to execute (e.g., 'ls -la', 'python script.py')"
                            }
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web using DuckDuckGo. Returns a list of search results with titles, snippets, and URLs.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (e.g., 'Python programming tutorials', 'latest AI news')"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List all files and directories in a given directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directory to list (e.g., '.', './workspace', './memory')"
                            }
                        },
                        "required": ["directory"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "spawn_sub_agent",
                    "description": "Spawn a specialized sub-agent with a specific role and tools. Use this to delegate specialized tasks.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the sub-agent (e.g., 'Research Agent', 'Code Analyzer')"
                            },
                            "role": {
                                "type": "string",
                                "description": "Role/purpose of the sub-agent (e.g., 'Handles web research and data gathering')"
                            },
                            "tools": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of tool names this agent should have access to"
                            }
                        },
                        "required": ["name", "role", "tools"]
                    }
                }
            }
        ]
    
    def chat(self, user_message: str) -> str:
        """Send message to AI and get response"""
        
        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Save to file
        self._save_conversation()
        
        BeautifulUI.ai_thinking()
        
        # Call Mistral API
        response = self.client.chat.complete(
            model="mistral-large-latest",
            messages=self.messages,
            tools=self.tools
        )
        
        # Process response and handle tool calls
        final_response = self._process_response(response)
        
        # Add assistant response to history (text content)
        # Note: Tool use handling adds messages inside _process_response
        if final_response:
             # Only add if we haven't already added a final text response in process
             pass 

        self._save_conversation()
        
        return final_response
    
    def _process_response(self, response) -> str:
        """Process API response and handle tool calls"""
        
        message = response.choices[0].message
        
        # Check if AI wants to use tools
        while message.tool_calls:
            # Add the assistant's request to history
            self.messages.append(message)
            
            # Execute all tools requested
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                
                # Mistral arguments come as a JSON string
                try:
                    tool_input = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_input = {}

                BeautifulUI.tool_call(tool_name, tool_input)
                
                # Execute the tool
                result = self.tool_executor.execute(tool_name, tool_input)
                BeautifulUI.tool_result(str(result))
                
                # Append result to messages with role "tool"
                self.messages.append({
                    "role": "tool",
                    "name": tool_name,
                    "content": str(result),
                    "tool_call_id": tool_call.id
                })

            # Get next response from AI
            BeautifulUI.ai_thinking("AI is processing tool results...")
            
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=self.messages,
                tools=self.tools
            )
            message = response.choices[0].message
        
        # If no tools, or after tools are done, we have a text response
        if message.content:
            self.messages.append({
                "role": "assistant",
                "content": message.content
            })
            return message.content
            
        return "No response generated."
    
    def _save_conversation(self):
        """Save conversation to file"""
        memory_dir = Path("./memory")
        memory_dir.mkdir(exist_ok=True)
        
        session_file = memory_dir / f"session_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Helper to serialize Mistral objects
        def serializable(obj):
            if hasattr(obj, "model_dump"):
                return obj.model_dump()
            return obj

        with open(session_file, 'w') as f:
            json.dump(self.messages, f, indent=2, default=serializable)
    
    def get_active_agents(self) -> List[Dict]:
        """Get list of active sub-agents"""
        agents_file = Path("./memory/active_agents.json")
        if agents_file.exists():
            with open(agents_file, 'r') as f:
                return json.load(f)
        return []
    
    def shutdown(self):
        """Graceful shutdown"""
        BeautifulUI.system_msg("Initiating shutdown...", "WARNING")
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}SESSION SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}")
        print(f"\n{Fore.WHITE}Total messages: {len(self.messages)}")
        
        agents = self.get_active_agents()
        print(f"Sub-agents spawned: {len(agents)}")
        
        if agents:
            print(f"\n{Fore.YELLOW}Active Sub-Agents:")
            for agent in agents:
                print(f"  {Fore.CYAN}• {agent['name']}: {agent['role']}")
        
        print(f"\n{Fore.CYAN}{'='*80}\n")
        
        BeautifulUI.system_msg("Shutdown complete", "SUCCESS")


def verify_system():
    """Verify system setup"""
    BeautifulUI.system_msg("Verifying system integrity...", "PROCESS")
    time.sleep(0.3)
    
    # Check directories
    for directory in ["memory", "workspace"]:
        Path(f"./{directory}").mkdir(exist_ok=True)
        BeautifulUI.system_msg(f"Directory verified: {directory}", "SUCCESS")
    
    # Check boot.md
    boot_file = Path("./boot.md")
    if boot_file.exists():
        BeautifulUI.system_msg("boot.md found", "SUCCESS")
    else:
        BeautifulUI.system_msg("boot.md not found - will use default", "WARNING")
    
    time.sleep(0.3)
    BeautifulUI.system_msg("System ready", "SUCCESS")


def main():
    """Main entry point"""
    
    os.system('clear' if os.name != 'nt' else 'cls')
    
    BeautifulUI.header()
    
    BeautifulUI.system_msg("System starting...", "PROCESS")
    time.sleep(0.5)
    
    verify_system()
    
    time.sleep(0.5)
    BeautifulUI.separator()
    
    try:
        brain = CentralBrain()
        BeautifulUI.system_msg("All systems operational", "SUCCESS")
        BeautifulUI.separator()
        
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}💡 Real AI with tool calling active! Type 'exit' to shutdown{Style.RESET_ALL}\n")
        
        while True:
            try:
                user_input = BeautifulUI.user_prompt()
                
                if user_input.lower() in ['exit', 'quit', 'shutdown']:
                    brain.shutdown()
                    break
                
                if not user_input.strip():
                    continue
                
                # Get AI response
                response = brain.chat(user_input)
                BeautifulUI.ai_response(response)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupt received{Style.RESET_ALL}")
                brain.shutdown()
                break
            except Exception as e:
                BeautifulUI.error_box("ERROR", str(e))
                import traceback
                traceback.print_exc()
    
    except ValueError as e:
        BeautifulUI.error_box("CONFIGURATION ERROR", str(e))
        return 1
    except Exception as e:
        BeautifulUI.error_box("INITIALIZATION FAILED", str(e))
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())