# ratios: loc_comments=100:46 imports_exports=9:7 calls_definitions=40:12
"""
FastAPI seed runner for PCNA. This file provides a minimal runnable seed
process that can act as compute/meta/global/sentinel. It is intentionally
lightweight and suitable for local testing.

Environment configuration:
  - SEED_ID: int (default 0)
  - ROLE: one of compute|meta|sentinel|global (default compute)

The networking layer here is a minimal placeholder using aiohttp. In a real
deployment you'd wire actual DNS/ports mapping per-seed.
"""

# === MODULE_BUILD ===
# id: pcna_core_main
#   module_name: main
#   module_kind: service
#   summary: Minimal FastAPI seed-runner process (compute/meta/sentinel/global) exposing health/topology/receive_delta routes with an aiohttp networking placeholder.
#   owner: Erin Spencer
#   public_surface: app, PCNASeed, health, topology, receive_delta, startup, shutdown, tick_loop
#   internal_surface: seed_instance
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: external
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: do not launch this process; use root-level main.py seed runner instead
#   requires: pcna_topology, pcna_tensor_engine
#   since: 2026-06-02
#   unresolved: BROKEN alt entry point — imports from non-existent src.core.* (do not use per CLAUDE.md)
# === END MODULE_BUILD ===

import os
import asyncio
from typing import Dict, Any, Optional
import logging

from fastapi import FastAPI, BackgroundTasks
import uvicorn
import aiohttp

from src.core.topology import PCNATopology, SeedRole
from src.core.tensor_engine import TensorState, MarkovRecursion

logger = logging.getLogger("pcna")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="PCNA Seed")

seed_instance: Optional["PCNASeed"] = None


class PCNASeed:
    def __init__(self, seed_id: int, role: SeedRole):
        self.seed_id = seed_id
        self.role = role
        self.topology = PCNATopology()
        self.state: Optional[TensorState] = None
        self.tick = 0
        self._client = aiohttp.ClientSession()

        if role == SeedRole.COMPUTE:
            # Create a small default tensor for local testing/demo.
            actor = [0]  # simple single-dim actor/time/context for demo
            time = [0]
            metric = (1.0 * (np := __import__("numpy"))).ones((1,))  # single-value metric
            context = [0]
            self.state = TensorState(actor=np.array(actor), time=np.array(time), metric=metric, context=np.array(context))
            self.tensor_engine = MarkovRecursion()
            logger.info(f"Initialized compute seed {seed_id} with trivial state")

    async def process_tick(self):
        self.tick += 1
        logger.debug(f"Seed {self.seed_id} processing tick {self.tick}")

        if self.role == SeedRole.COMPUTE:
            await self._compute_tick()
        # meta/sentinel/global roles could be handled here with specific logic

    async def _compute_tick(self):
        # Example compute operations: compute injected/resolved (dummy here)
        injected = self.state.metric * 0.01  # small injected
        resolved = self.state.metric * 0.009  # slightly different to demonstrate conservation
        new_state = self.tensor_engine.update(self.state, injected, resolved)
        self.state = new_state

        # send deltas to neighbors (using global neighbor ids, convert to URLs in your deployment)
        seed_info = self.topology.seeds.get(self.seed_id)
        if seed_info and seed_info.neighbors:
            for neighbor_id in seed_info.neighbors:
                # in local testing this will likely fail unless neighbor URL mapping is provided
                await self._send_to_neighbor(neighbor_id, {"from": self.seed_id, "tick": self.tick})

    async def _send_to_neighbor(self, neighbor_id: int, payload: Dict[str, Any]):
        """
        Simple async HTTP POST to a neighbor. This function assumes a mapping
        from neighbor_id -> host:port which is environment-specific.
        For local testing, you can set SEED_URL_<id> environment variables,
        e.g. SEED_URL_6=http://localhost:8001
        """
        env_var = f"SEED_URL_{neighbor_id}"
        url = os.getenv(env_var)
        if not url:
            # nothing configured for neighbor, skip
            logger.debug(f"No URL configured for neighbor {neighbor_id} (env {env_var}), skipping send")
            return

        try:
            async with self._client.post(f"{url}/receive_delta", json=payload, timeout=2) as resp:
                logger.debug(f"Sent delta to {neighbor_id} ({url}), status {resp.status}")
        except Exception as exc:
            logger.warning(f"Failed to send to neighbor {neighbor_id} at {url}: {exc}")

    async def close(self):
        await self._client.close()


async def tick_loop():
    while True:
        try:
            if seed_instance:
                await seed_instance.process_tick()
            await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.exception(f"tick loop error: {exc}")
            await asyncio.sleep(1.0)


@app.on_event("startup")
async def startup():
    global seed_instance
    seed_id = int(os.getenv("SEED_ID", "0"))
    role_raw = os.getenv("ROLE", "compute").lower()
    try:
        role = SeedRole(role_raw)
    except Exception:
        # fallback if value is 'compute', 'meta', etc.
        role = SeedRole.COMPUTE

    seed_instance = PCNASeed(seed_id=seed_id, role=role)

    # launch tick loop
    asyncio.create_task(tick_loop())
    logger.info(f"Seed {seed_id} (role={role.value}) started")


@app.on_event("shutdown")
async def shutdown():
    if seed_instance:
        await seed_instance.close()


@app.get("/health")
async def health():
    if not seed_instance:
        return {"status": "starting"}
    return {"status": "healthy", "seed_id": seed_instance.seed_id, "role": seed_instance.role.value}


@app.get("/topology")
async def topology():
    if not seed_instance:
        return {}
    return seed_instance.topology.to_dict()


@app.post("/receive_delta")
async def receive_delta(delta: Dict):
    # In a real system, we'd validate and apply the delta to a pending buffer.
    logger.info(f"Received delta at seed {seed_instance.seed_id if seed_instance else 'unknown'}: {delta}")
    return {"status": "received"}


if __name__ == "__main__":
    # Useful for local development: honor PORT env var and SEED_ID/ROLE
    port = int(os.getenv("PORT", os.getenv("PORT0", "8000")))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, log_level="info")
# ratios: loc_comments=100:46 imports_exports=9:7 calls_definitions=40:12
