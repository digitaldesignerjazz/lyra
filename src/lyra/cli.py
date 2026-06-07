"""Lyra CLI - Command line interface for running agents and swarms.

Now with real inter-agent messaging support.
"""

import argparse
import asyncio
import random
from typing import List, Dict

from lyra.core.agent import LyraAgent


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lyra",
        description="Lyra - Self-improving emotional AI agent framework with messaging",
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
        help="Enable more detailed output and message logging",
    )
    return parser


async def run_single_agent(name: str, steps: int, verbose: bool = False) -> None:
    """Run a single LyraAgent."""
    agent = LyraAgent(name=name)
    if verbose:
        print(f"[CLI] Running single agent: {name} for {steps} steps")
    await agent.run(steps=steps)


async def run_swarm(num_agents: int, steps: int, base_name: str = "Lyra", verbose: bool = False) -> None:
    """Run a swarm of LyraAgents with real inter-agent messaging.

    Agents can now send messages to each other (status, encouragement, questions).
    Receiving messages influences emotional state.
    """
    print(f"\n🌐 Starting Lyra Swarm with {num_agents} agents + inter-agent messaging\n")

    agents: List[LyraAgent] = [
        LyraAgent(name=f"{base_name}-{i+1}") for i in range(num_agents)
    ]
    name_to_agent: Dict[str, LyraAgent] = {agent.name: agent for agent in agents}

    async def agent_task(agent: LyraAgent) -> None:
        for step in range(steps):
            # 1. Process any messages received since last step
            summaries = await agent.process_inbox()
            if summaries and verbose:
                for s in summaries:
                    print(f"  [{agent.name}] Inbox: {s}")

            # 2. Occasionally perceive swarm context
            if step % 2 == 0:
                await agent.perceive({
                    "type": "swarm_event",
                    "step": step,
                })

            # 3. Occasionally send a message to another agent
            if step > 0 and random.random() < 0.45:  # ~45% chance per step after first
                other_agents = [a for a in agents if a.name != agent.name]
                if other_agents:
                    target = random.choice(other_agents)

                    if random.random() < 0.5:
                        msg_type = "status"
                        content = f"Step {step}: All good here. Curiosity at {agent.emotional_state.curiosity:.2f}"
                    else:
                        msg_type = "encouragement"
                        content = "You're doing great — keep exploring!"

                    message = await agent.send_message(
                        to=target,
                        content=content,
                        msg_type=msg_type,
                    )
                    # Deliver the message
                    await target.receive_message(message)

                    if verbose:
                        print(f"  [{agent.name}] → [{target.name}] ({msg_type}): {content}")

            # 4. Act + self-improve
            action = await agent.act()
            if verbose:
                print(f"  [{agent.name}] Step {step+1}: {action.get('action')}")

            if step % 3 == 0:
                improvement = await agent.self_improve()
                if verbose:
                    print(f"  [{agent.name}] {improvement}")

            await asyncio.sleep(0.35)

    # Run all agents concurrently
    tasks = [agent_task(agent) for agent in agents]
    await asyncio.gather(*tasks)

    print(f"\n✅ Swarm run complete. {num_agents} agents finished {steps} steps each.\n")
    print("Final emotional states:")
    for agent in agents:
        print(f"  {agent.name}: dominant={agent.emotional_state.dominant_emotion}, "
              f"curiosity={agent.emotional_state.curiosity:.2f}, joy={agent.emotional_state.joy:.2f}")

    # Show total messages exchanged
    total_messages = sum(len(a.memory.short_term) for a in agents)
    print(f"\nTotal memory events across swarm: {total_messages}")


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
