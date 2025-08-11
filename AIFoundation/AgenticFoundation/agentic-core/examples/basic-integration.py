#!/usr/bin/env python3
"""
Basic Integration Example - Agentic Core

This example demonstrates how to integrate Agentic Core into an existing
Python application with minimal setup.
"""

import asyncio
import os
from typing import Dict, Any

# Import Agentic Core
from agentic_core import AgenticCore, create_agentic_core


async def basic_chat_example():
    """Basic chat functionality example."""
    print("🤖 Agentic Core - Basic Chat Example")
    print("=" * 50)
    
    # Initialize Agentic Core
    agentic = create_agentic_core(
        model_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///agentic.db")
    )
    
    try:
        # Simple chat
        response = await agentic.chat(
            message="Hello! Can you help me with a simple task?",
            user_id="user_123"
        )
        
        print(f"🤖 AI Response: {response.response}")
        print(f"📊 Task ID: {response.task_id}")
        print(f"⏱️  Status: {response.status}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await agentic.close()


async def task_processing_example():
    """Task processing example."""
    print("\n🔧 Agentic Core - Task Processing Example")
    print("=" * 50)
    
    agentic = create_agentic_core(
        model_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    try:
        # Process a specific task
        response = await agentic.process_task(
            task_type="analyze",
            user_id="user_123",
            task_description="Analyze the following data: Sales increased by 15% this quarter",
            context={"data_type": "sales", "timeframe": "quarterly"}
        )
        
        print(f"📋 Task Type: {response.task_type}")
        print(f"📊 Result: {response.result}")
        print(f"⏱️  Processing Time: {response.processing_time}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await agentic.close()


async def conversation_history_example():
    """Conversation history example."""
    print("\n📚 Agentic Core - Conversation History Example")
    print("=" * 50)
    
    agentic = create_agentic_core(
        model_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        database_url=os.getenv("DATABASE_URL")
    )
    
    try:
        # Send multiple messages
        messages = [
            "Hello! I'm working on a Python project.",
            "Can you help me with error handling?",
            "What are the best practices for async programming?"
        ]
        
        conversation_id = None
        
        for i, message in enumerate(messages, 1):
            print(f"\n💬 Message {i}: {message}")
            
            response = await agentic.chat(
                message=message,
                user_id="user_123",
                conversation_id=conversation_id
            )
            
            conversation_id = response.conversation_id
            print(f"🤖 Response: {response.response[:100]}...")
        
        # Get conversation history
        history = await agentic.get_conversation_history("user_123", limit=5)
        print(f"\n📚 Conversation History: {len(history)} conversations found")
        
        for conv in history:
            print(f"  - {conv.title} ({conv.created_at})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await agentic.close()


async def custom_tool_example():
    """Custom tool integration example."""
    print("\n🛠️  Agentic Core - Custom Tool Example")
    print("=" * 50)
    
    from agentic_core.tools import BaseTool
    
    # Define a custom tool
    class CalculatorTool(BaseTool):
        name = "calculator"
        description = "Perform mathematical calculations"
        
        async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
            expression = data.get("expression", "")
            try:
                # Safe evaluation (in production, use a proper math parser)
                result = eval(expression)
                return {
                    "status": "success",
                    "result": result,
                    "expression": expression
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e),
                    "expression": expression
                }
    
    # Initialize with custom tool
    agentic = create_agentic_core(
        model_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Register the custom tool
    calculator_tool = CalculatorTool()
    agentic.register_tool(calculator_tool)
    
    try:
        # Use the tool through chat
        response = await agentic.chat(
            message="Can you calculate 15 * 23 + 7?",
            user_id="user_123"
        )
        
        print(f"🧮 Calculation Request: {response.response}")
        
        # Get available tools
        tools = agentic.get_available_tools()
        print(f"\n🛠️  Available Tools: {len(tools)} tools")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await agentic.close()


async def health_monitoring_example():
    """Health monitoring example."""
    print("\n🏥 Agentic Core - Health Monitoring Example")
    print("=" * 50)
    
    agentic = create_agentic_core(
        model_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    try:
        # Check health status
        health = await agentic.get_health_status()
        
        print("🏥 System Health Status:")
        for key, value in health.items():
            print(f"  - {key}: {value}")
        
        # Get performance metrics
        metrics = await agentic.get_metrics(hours_back=24)
        
        print(f"\n📊 Performance Metrics (last 24h):")
        if metrics:
            for metric_name, metric_data in metrics.items():
                print(f"  - {metric_name}: {metric_data}")
        else:
            print("  No metrics available yet")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await agentic.close()


async def main():
    """Run all examples."""
    print("🚀 Agentic Core Integration Examples")
    print("=" * 60)
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Some examples may fail.")
        print("   Set it with: export OPENAI_API_KEY='your-api-key'")
        print()
    
    # Run examples
    await basic_chat_example()
    await task_processing_example()
    await conversation_history_example()
    await custom_tool_example()
    await health_monitoring_example()
    
    print("\n✅ All examples completed!")
    print("\n📚 Next Steps:")
    print("  1. Set up your environment variables")
    print("  2. Configure your database connection")
    print("  3. Customize the tools and models")
    print("  4. Integrate into your application")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 