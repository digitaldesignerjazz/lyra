"""Lyra CLI - Command line interface for running agents and swarms.

Usage examples:
    lyra --name "Lyra-Prime" --mode single
    lyra --name "Lyra-Prime" --mode swarm --agents 5 --steps 8
    python -m lyra.core.agent --name "MyAgent" --mode swarm
"""

import argparse
import asyncio
from typing import List

from lyra.core.agent import LyraAgent


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lyra",
        description="Lyra - Self-improving emotional AI agent framework",
        epilog="Run agents and swarms. See https://github.com/digitaldesignerjazz/lyra",
    )
    parser.add_argument(
        "--name", "-n",
        type=str,
        default="Lyra-Prime",
        help="Name / persona for the primary agent (default: Lyra-Prime)",
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["single", "swarm"],
        default="single",
        help="Run mode: 'single' (one agent) or 'swarm' (multiple coordinated agents)",
    )
    parser.add_argument(
        "--agents", "-a",
        type=int,
        default=3,
        help="Number of agents in swarm mode (default: 3)",
    )
    parser.add_argument(
        "--steps", "-s",
        type=int,
        default=6,
        help="Number of steps each agent runs (default: 6)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable more detailed output",
    )
    return parser


async def run_single_agent(name: str, steps: int, verbose: bool = False) -> None:
    """Run a single LyraAgent."""
    agent = LyraAgent(name=name)
    if verbose:
        print(f"[CLI] Running single agent: {name} for {steps} steps")
    await agent.run(steps=steps)


async def run_swarm(num_agents: int, steps: int, base_name: str = "Lyra", verbose: bool = False) -> None:
    """Run a simple swarm of LyraAgents concurrently.

    In this initial implementation, agents run in parallel and occasionally
    'perceive' a shared swarm event. This demonstrates coordination scaffolding.
    """
    print(f"\n🌐 Starting Lyra Swarm with {num_agents} agents (mode: swarm)\n")

    agents: List[LyraAgent] = [
        LyraAgent(name=f"{base_name}-{i+1}") for i in range(num_agents)
    ]

    async def agent_task(agent: LyraAgent, agent_idx: int) -> None:
        for step in range(steps):
            # Each agent perceives a 'swarm context' occasionally
            if step % 2 == 0:
                await agent.perceive({
                    "type": "swarm_event",
                    "from": "swarm_coordinator",
                    "message": f"Swarm step {step} - agent {agent_idx + 1} checking in",
                })
            action = await agent.act()
            if verbose:
                print(f"  [{agent.name}] Step {step+1}: {action.get('action')}")

            if step % 3 == 0:
                improvement = await agent.self_improve()
                if verbose:
                    print(f"  [{agent.name}] {improvement}")

            await asyncio.sleep(0.3)

    # Run all agents concurrently
    tasks = [agent_task(agent, idx) for idx, agent in enumerate(agents)]
    await asyncio.gather(*tasks)

    print(f"\n✅ Swarm run complete. {num_agents} agents finished {steps} steps each.\n")
    print("Emotional states at end:")
    for agent in agents:
        print(f"  {agent.name}: dominant={agent.emotional_state.dominant_emotion}, "
              f"curiosity={agent.emotional_state.curiosity:.2f}")


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    print(f"Lyra v{LyraAgent.model_fields['version'].default} — {args.mode.upper()} mode")

    if args.mode == "single":
        asyncio.run(run_single_agent(args.name, args.steps, args.verbose))
    elif args.mode == "swarm":
        asyncio.run(run_swarm(args.agents, args.steps, base_name=args.name.split("-")[0], verbose=args.verbose))
    else:
        parser.error(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    main()
