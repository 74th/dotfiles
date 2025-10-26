#!/usr/local/bin/system-python

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable, List, Sequence


class CommandError(RuntimeError):
	"""Raised when an underlying CLI command fails."""


@dataclass
class ContainerInfo:
	container_id: str  # full length
	short_id: str
	name: str
	image: str
	started_at: dt.datetime
	age: dt.timedelta


def run_command(args: Sequence[str]) -> str:
	"""Run a CLI command and return its stdout as text."""

	try:
		result = subprocess.run(
			list(args),
			check=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
		)
	except FileNotFoundError as exc:
		raise CommandError(f"'{args[0]}' が見つかりません (PATH を確認してください)") from exc
	except subprocess.CalledProcessError as exc:
		raise CommandError(exc.stderr.strip() or str(exc)) from exc
	return result.stdout


def list_running_container_ids() -> List[str]:
	"""Return running container IDs (same set as `docker ps`)."""

	output = run_command(("docker", "ps", "--no-trunc", "--format", "{{.ID}}"))
	return [line.strip() for line in output.splitlines() if line.strip()]


def inspect_containers(container_ids: Sequence[str]) -> list[dict]:
	if not container_ids:
		return []
	output = run_command(("docker", "inspect", *container_ids))
	try:
		return json.loads(output)
	except json.JSONDecodeError as exc:
		raise CommandError("`docker inspect` の出力を JSON として解析できませんでした") from exc


def parse_docker_datetime(value: str | None) -> dt.datetime | None:
	if not value:
		return None

	value = value.strip()
	if not value:
		return None

	if value.endswith("Z"):
		value = value[:-1] + "+00:00"

	tz_pos = max(value.rfind("+"), value.rfind("-"))
	if tz_pos <= len("YYYY-MM-DDT"):
		tz_part = ""
		main = value
	else:
		tz_part = value[tz_pos:]
		main = value[:tz_pos]

	if "." in main:
		date_part, frac_part = main.split(".", 1)
		frac_digits = ''.join(ch for ch in frac_part if ch.isdigit())
		frac_part = (frac_digits + "000000")[:6]
		main = f"{date_part}.{frac_part}"

	iso_value = main + tz_part
	try:
		return dt.datetime.fromisoformat(iso_value)
	except ValueError:
		for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z"):
			try:
				return dt.datetime.strptime(iso_value, fmt)
			except ValueError:
				continue
	return None


def format_timedelta(delta: dt.timedelta) -> str:
	total_seconds = int(delta.total_seconds())
	sign = "-" if total_seconds < 0 else ""
	total_seconds = abs(total_seconds)
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	return f"{sign}{hours:d}h {minutes:02d}m {seconds:02d}s"


def collect_recent_containers(threshold: dt.timedelta) -> List[ContainerInfo]:
	container_ids = list_running_container_ids()
	if not container_ids:
		return []

	inspected = inspect_containers(container_ids)
	now = dt.datetime.now(dt.timezone.utc)
	recent: List[ContainerInfo] = []
	for entry in inspected:
		started_raw = entry.get("State", {}).get("StartedAt")
		started_at = parse_docker_datetime(started_raw)
		if started_at is None:
			continue
		if started_at.tzinfo is None:
			started_at = started_at.replace(tzinfo=dt.timezone.utc)
		age = now - started_at.astimezone(dt.timezone.utc)
		if age < dt.timedelta(0) or age > threshold:
			continue
		container_id = entry.get("Id", "")
		short_id = container_id[:12] if container_id else container_id
		name = entry.get("Name", "").lstrip("/") or short_id
		image = entry.get("Config", {}).get("Image", "")
		recent.append(ContainerInfo(container_id, short_id, name, image, started_at, age))
	return sorted(recent, key=lambda c: c.age)


def remove_containers(containers: Iterable[ContainerInfo]) -> str:
	ids = [c.container_id for c in containers]
	if not ids:
		return ""
	output = run_command(("docker", "rm", "-f", *ids))
	return output.strip()


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="docker ps で確認できるうち、指定時間以内に起動したコンテナを削除します",
	)
	parser.add_argument(
		"--within-minutes",
		type=float,
		default=60.0,
		help="何分以内に起動したコンテナを削除対象にするか (デフォルト: 60 分)",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="削除を実行せず対象コンテナだけ表示します",
	)
	return parser


def main(argv: Sequence[str] | None = None) -> int:
	parser = build_parser()
	args = parser.parse_args(argv)

	try:
		threshold = dt.timedelta(minutes=args.within_minutes)
	except OverflowError:
		print("指定した時間が大きすぎます", file=sys.stderr)
		return 1

	try:
		recent = collect_recent_containers(threshold)
	except CommandError as exc:
		print(exc, file=sys.stderr)
		return 1

	if not recent:
		print(f"{args.within_minutes:.1f} 分以内に起動したコンテナはありませんでした。")
		return 0

	print(f"{args.within_minutes:.1f} 分以内に起動したコンテナ:")
	for info in recent:
		started_display = info.started_at.astimezone(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
		age_display = format_timedelta(info.age)
		image_display = info.image
		if image_display and len(image_display) > 60:
			image_display = image_display[:57] + "..."
		image_part = f" ({image_display})" if image_display else ""
		print(f"  - {info.short_id} [{info.name}]{image_part} | started {started_display} | age {age_display}")

	if args.dry_run:
		print("\n--dry-run オプションが指定されたため削除しません。")
		return 0

	try:
		removal_output = remove_containers(recent)
	except CommandError as exc:
		print(exc, file=sys.stderr)
		return 1

	if removal_output:
		print("削除したコンテナ:")
		for line in removal_output.splitlines():
			print(f"  - {line.strip()}")
	else:
		print("docker rm -f の出力はありませんでした。")

	return 0


if __name__ == "__main__":
	sys.exit(main())
