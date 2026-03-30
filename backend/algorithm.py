import json
from collections import deque
from datetime import datetime


class RoutePlanner:
    def __init__(self, data_path="../data/graph.json"):
        try:
            with open(data_path, "r") as f:
                raw = json.load(f)
                self.graph = {k.upper(): v for k, v in raw.items()}
        except:
            self.graph = {}

    def find_routes(self, source, destination, max_transfers=5, max_routes=5):
        src, dest = source.upper(), destination.upper()
        if src not in self.graph or dest not in self.graph:
            return []

        # BFS layers by transfer count
        all_paths = []
        for xfers in range(0, max_transfers + 1):
            paths = self._bfs(src, dest, xfers)
            all_paths.extend(paths)
            if all_paths:  # Optional: stop early if you want least‑transfers only
                break

        # Process each path into summary + segments
        processed = []
        for legs in all_paths:
            segments = self._compress(legs)

            # Use first departure as the sort key (no duration / days)
            first_dep = legs[0]["dep"]      # departure from source station

            processed.append({
                "summary": f"{src} → {dest}",
                "transfer_count": len(segments) - 1,
                "segments": segments,
                "first_dep": first_dep,      # to sort by dep time
            })

        # Sort by first departure time, then by transfers (optional)
        processed.sort(key=lambda x: (x["first_dep"], x["transfer_count"]))

        return processed[:max_routes]

    def _bfs(self, src, dst, max_transfers):
        """BFS that stops at exactly max_transfers steps."""
        # State: (station, last_train, transfers, path_edges)
        queue = deque()
        seen = set()  # (station, last_train) to avoid cycles

        # From source, start a new train on each edge
        for edge in self.graph.get(src, []):
            state = (
                edge["to"],
                edge["train_name"],
                0,
                [
                    {
                        "from": src,
                        "to": edge["to"],
                        "train": edge["train_name"],
                        "train_no": edge.get("train_no", ""),
                        "dep": edge["departure"],
                        "arr": edge["arrival"],
                    }
                ],
            )
            key = (edge["to"], edge["train_name"])
            if key not in seen:
                seen.add(key)
                queue.append(state)

        paths = []

        while queue:
            station, last_train, transfers, legs = queue.popleft()

            if station == dst:
                paths.append(legs)
                continue

            if transfers > max_transfers:
                continue

            for edge in self.graph.get(station, []):
                next_train = edge["train_name"]
                next_transfers = transfers
                next_legs = legs[:]

                if next_train != last_train:
                    next_transfers += 1

                if next_transfers > max_transfers:
                    continue

                next_legs.append({
                    "from": station,
                    "to": edge["to"],
                    "train": next_train,
                    "train_no": edge.get("train_no"),
                    "dep": edge["departure"],
                    "arr": edge["arrival"],
                })

                state_key = (edge["to"], next_train)
                if state_key not in seen:
                    seen.add(state_key)
                    queue.append((edge["to"], next_train, next_transfers, next_legs))

        return paths

    def _compress(self, legs):
        if not legs:
            return []

        res = []
        curr = legs[0].copy()
        start_station = curr["from"]

        for i in range(1, len(legs)):
            leg = legs[i]
            if leg["train"] == curr["train"]:
                # Extend current segment
                curr["to"] = leg["to"]
                curr["arr"] = leg["arr"]
            else:
                # Flush current and start new
                res.append({
                    "line": f"{start_station} → {curr['to']}",
                    "train": curr["train"],
                    "train_no": curr.get("train_no", ""),
                    "dep": curr["dep"],
                    "arr": curr["arr"],
                })
                curr = leg.copy()
                start_station = curr["from"]

        res.append({
            "line": f"{start_station} → {curr['to']}",
            "train": curr["train"],
            "train_no": curr.get("train_no", ""),
            "dep": curr["dep"],
            "arr": curr["arr"],
        })
        return res

    # ========== Removed: duration and days ==========

    # Everything related to _duration_minutes, _duration_days, _format_duration is gone.

    # Optional later: if you want to show “time text” in UI, you can keep _format_duration,
    # but if you want to remove it, just delete those methods.

    # For now, this class is output‑only: transfers and dep/arr times.

planner = RoutePlanner()
