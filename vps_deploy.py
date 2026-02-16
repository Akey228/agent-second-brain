"""Full automated VPS deployment for Agent Second Brain."""

import paramiko
import time
import sys

# VPS connection
HOST = "144.31.226.94"
USER = "root"
PASSWORD = "M9w2tnchqn0b"

# Tokens
TELEGRAM_BOT_TOKEN = "8363344885:AAF0I08ErFhwBdJqbNxANoMipl98SohTCTE"
TELEGRAM_USER_ID = "1887929462"
DEEPGRAM_API_KEY = "1c8a62344965df13c933da0dd88ab1a2910714d6"
TODOIST_API_KEY = "74a57d3cf0f9b42b964dd21c23eeed174bc272c8"

# Deploy user
DEPLOY_USER = "nikita"
DEPLOY_PASS = "agent2brain"


def run_cmd(ssh, cmd, timeout=300):
    """Run command via SSH and print output in real-time."""
    print(f"\n>>> {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)

    output = stdout.read().decode("utf-8", errors="replace")
    errors = stderr.read().decode("utf-8", errors="replace")
    exit_code = stdout.channel.recv_exit_status()

    if output.strip():
        # Truncate long outputs
        lines = output.strip().split("\n")
        if len(lines) > 30:
            print("\n".join(lines[:5]))
            print(f"  ... ({len(lines) - 10} lines skipped) ...")
            print("\n".join(lines[-5:]))
        else:
            print(output.strip())

    if errors.strip() and exit_code != 0:
        print(f"STDERR: {errors.strip()[:500]}")

    if exit_code != 0:
        print(f"[EXIT CODE: {exit_code}]")

    return output, errors, exit_code


def main():
    print("=" * 60)
    print("  AGENT SECOND BRAIN - FULL VPS DEPLOYMENT")
    print("=" * 60)
    print(f"\nConnecting to {HOST}...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    print("Connected!\n")

    # =========================================================================
    # Step 1: Create deploy user
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 1: Creating user")
    print("=" * 60)

    run_cmd(ssh, f'id {DEPLOY_USER} 2>/dev/null || adduser --disabled-password --gecos "" {DEPLOY_USER}')
    run_cmd(ssh, f'echo "{DEPLOY_USER}:{DEPLOY_PASS}" | chpasswd')
    run_cmd(ssh, f'usermod -aG sudo {DEPLOY_USER}')
    # Allow sudo without password for setup
    run_cmd(ssh, f'echo "{DEPLOY_USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/{DEPLOY_USER}')

    print(f"\nUser '{DEPLOY_USER}' created with sudo access")

    # =========================================================================
    # Step 2: System dependencies
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 2: Installing system dependencies")
    print("=" * 60)

    run_cmd(ssh, 'apt-get update -qq', timeout=120)
    run_cmd(ssh, 'apt-get install -y -qq git curl wget build-essential software-properties-common', timeout=120)

    # =========================================================================
    # Step 3: Python 3.12
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 3: Installing Python 3.12")
    print("=" * 60)

    out, _, _ = run_cmd(ssh, 'python3.12 --version 2>/dev/null || echo "NOT_FOUND"')
    if "NOT_FOUND" in out:
        run_cmd(ssh, 'add-apt-repository -y ppa:deadsnakes/ppa', timeout=60)
        run_cmd(ssh, 'apt-get update -qq', timeout=60)
        run_cmd(ssh, 'apt-get install -y -qq python3.12 python3.12-venv python3.12-dev', timeout=120)

    run_cmd(ssh, 'python3.12 --version')

    # =========================================================================
    # Step 4: uv (as deploy user)
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 4: Installing uv")
    print("=" * 60)

    out, _, _ = run_cmd(ssh, f'su - {DEPLOY_USER} -c "command -v uv 2>/dev/null || echo NOT_FOUND"')
    if "NOT_FOUND" in out:
        run_cmd(ssh, f'su - {DEPLOY_USER} -c "curl -LsSf https://astral.sh/uv/install.sh | sh"', timeout=120)

    run_cmd(ssh, f'su - {DEPLOY_USER} -c "$HOME/.local/bin/uv --version"')

    # =========================================================================
    # Step 5: Node.js 20
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 5: Installing Node.js 20")
    print("=" * 60)

    out, _, _ = run_cmd(ssh, 'node --version 2>/dev/null || echo "NOT_FOUND"')
    if "NOT_FOUND" in out:
        run_cmd(ssh, 'curl -fsSL https://deb.nodesource.com/setup_20.x | bash -', timeout=60)
        run_cmd(ssh, 'apt-get install -y -qq nodejs', timeout=120)

    run_cmd(ssh, 'node --version')
    run_cmd(ssh, 'npm --version')

    # =========================================================================
    # Step 6: Claude CLI
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 6: Installing Claude CLI")
    print("=" * 60)

    out, _, _ = run_cmd(ssh, 'command -v claude 2>/dev/null || echo "NOT_FOUND"')
    if "NOT_FOUND" in out:
        run_cmd(ssh, 'npm install -g @anthropic-ai/claude-code', timeout=180)

    run_cmd(ssh, 'claude --version 2>/dev/null || echo "Claude CLI installed (version check may need login)"')

    # =========================================================================
    # Step 7: Clone repository
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 7: Cloning repository")
    print("=" * 60)

    PROJECT_DIR = f"/home/{DEPLOY_USER}/projects/agent-second-brain"

    run_cmd(ssh, f'su - {DEPLOY_USER} -c "mkdir -p /home/{DEPLOY_USER}/projects"')

    out, _, _ = run_cmd(ssh, f'test -d {PROJECT_DIR} && echo "EXISTS" || echo "NOT_FOUND"')
    if "EXISTS" in out:
        print("Project directory already exists, pulling latest...")
        run_cmd(ssh, f'su - {DEPLOY_USER} -c "cd {PROJECT_DIR} && git pull"', timeout=60)
    else:
        run_cmd(ssh, f'su - {DEPLOY_USER} -c "git clone https://github.com/smixs/agent-second-brain.git {PROJECT_DIR}"', timeout=60)

    # =========================================================================
    # Step 8: Create .env file
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 8: Creating .env file")
    print("=" * 60)

    env_content = f"""# Telegram Bot API token from @BotFather
TELEGRAM_BOT_TOKEN={TELEGRAM_BOT_TOKEN}

# Deepgram API key for voice transcription
DEEPGRAM_API_KEY={DEEPGRAM_API_KEY}

# Todoist API key for task management
TODOIST_API_KEY={TODOIST_API_KEY}

# Path to Obsidian vault directory
VAULT_PATH=./vault

# JSON array of Telegram user IDs allowed to use the bot
ALLOWED_USER_IDS=[{TELEGRAM_USER_ID}]"""

    run_cmd(ssh, f'cat > {PROJECT_DIR}/.env << \'ENVEOF\'\n{env_content}\nENVEOF')
    run_cmd(ssh, f'chmod 600 {PROJECT_DIR}/.env')
    run_cmd(ssh, f'chown {DEPLOY_USER}:{DEPLOY_USER} {PROJECT_DIR}/.env')

    print(".env file created")

    # =========================================================================
    # Step 9: Configure MCP (Todoist for Claude)
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 9: Configuring MCP (Todoist integration)")
    print("=" * 60)

    mcp_content = f"""{{
  "mcpServers": {{
    "todoist": {{
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@doist/todoist-ai"],
      "env": {{
        "TODOIST_API_KEY": "{TODOIST_API_KEY}"
      }}
    }}
  }}
}}"""

    run_cmd(ssh, f'cat > {PROJECT_DIR}/mcp-config.json << \'MCPEOF\'\n{mcp_content}\nMCPEOF')
    run_cmd(ssh, f'chown {DEPLOY_USER}:{DEPLOY_USER} {PROJECT_DIR}/mcp-config.json')

    print("MCP config created with Todoist API key")

    # =========================================================================
    # Step 10: Install Python dependencies
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 10: Installing Python dependencies")
    print("=" * 60)

    run_cmd(ssh, f'su - {DEPLOY_USER} -c "cd {PROJECT_DIR} && $HOME/.local/bin/uv sync"', timeout=180)

    # =========================================================================
    # Step 11: Fix script paths
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 11: Fixing script paths")
    print("=" * 60)

    # Fix process.sh - replace hardcoded shima paths
    run_cmd(ssh, f'sed -i \'s|export HOME="/home/shima"|export HOME="/home/{DEPLOY_USER}"|\' {PROJECT_DIR}/scripts/process.sh 2>/dev/null || true')
    run_cmd(ssh, f'sed -i \'s|/home/shima/projects/agent-second-brain|{PROJECT_DIR}|\' {PROJECT_DIR}/scripts/process.sh 2>/dev/null || true')
    # Also handle the new template format
    run_cmd(ssh, f'sed -i \'s|export HOME="${{HOME:-/home/$(whoami)}}"|export HOME="/home/{DEPLOY_USER}"|\' {PROJECT_DIR}/scripts/process.sh 2>/dev/null || true')
    run_cmd(ssh, f'chmod +x {PROJECT_DIR}/scripts/process.sh')

    print("Script paths fixed")

    # =========================================================================
    # Step 12: Clean vault example data
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 12: Cleaning vault examples")
    print("=" * 60)

    run_cmd(ssh, f"""
rm -rf {PROJECT_DIR}/vault/daily/* 2>/dev/null
rm -rf {PROJECT_DIR}/vault/thoughts/ideas/* 2>/dev/null
rm -rf {PROJECT_DIR}/vault/thoughts/projects/* 2>/dev/null
rm -rf {PROJECT_DIR}/vault/thoughts/learnings/* 2>/dev/null
rm -rf {PROJECT_DIR}/vault/thoughts/reflections/* 2>/dev/null
rm -rf {PROJECT_DIR}/vault/summaries/* 2>/dev/null
rm -rf {PROJECT_DIR}/vault/attachments/* 2>/dev/null
echo "Vault cleaned"
""")

    # =========================================================================
    # Step 13: Systemd services and timers
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 13: Setting up systemd services and timers")
    print("=" * 60)

    # Bot service (24/7)
    bot_service = f"""[Unit]
Description=d-brain Telegram Bot
After=network.target

[Service]
Type=simple
User={DEPLOY_USER}
WorkingDirectory={PROJECT_DIR}
ExecStart=/home/{DEPLOY_USER}/.local/bin/uv run python -m d_brain
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target"""

    run_cmd(ssh, f'cat > /etc/systemd/system/d-brain-bot.service << \'SVCEOF\'\n{bot_service}\nSVCEOF')

    # Daily processing service
    process_service = f"""[Unit]
Description=d-brain Daily Processing

[Service]
Type=oneshot
User={DEPLOY_USER}
WorkingDirectory={PROJECT_DIR}
ExecStart={PROJECT_DIR}/scripts/process.sh
Environment=PYTHONUNBUFFERED=1"""

    run_cmd(ssh, f'cat > /etc/systemd/system/d-brain-process.service << \'SVCEOF\'\n{process_service}\nSVCEOF')

    # Daily processing timer
    process_timer = """[Unit]
Description=Run d-brain processing daily at 21:00

[Timer]
OnCalendar=*-*-* 21:00:00
Persistent=true

[Install]
WantedBy=timers.target"""

    run_cmd(ssh, f'cat > /etc/systemd/system/d-brain-process.timer << \'SVCEOF\'\n{process_timer}\nSVCEOF')

    # Weekly digest service
    weekly_service = f"""[Unit]
Description=d-brain Weekly Digest
After=network.target

[Service]
Type=oneshot
User={DEPLOY_USER}
WorkingDirectory={PROJECT_DIR}
ExecStart=/home/{DEPLOY_USER}/.local/bin/uv run python scripts/weekly.py
EnvironmentFile={PROJECT_DIR}/.env
StandardOutput=journal
StandardError=journal"""

    run_cmd(ssh, f'cat > /etc/systemd/system/d-brain-weekly.service << \'SVCEOF\'\n{weekly_service}\nSVCEOF')

    # Weekly digest timer
    weekly_timer = """[Unit]
Description=Run d-brain weekly digest Friday morning

[Timer]
OnCalendar=Fri 06:00
Persistent=true

[Install]
WantedBy=timers.target"""

    run_cmd(ssh, f'cat > /etc/systemd/system/d-brain-weekly.timer << \'SVCEOF\'\n{weekly_timer}\nSVCEOF')

    # Enable and start all
    print("\nEnabling and starting services...")
    run_cmd(ssh, 'systemctl daemon-reload')
    run_cmd(ssh, 'systemctl enable d-brain-bot && systemctl start d-brain-bot')
    run_cmd(ssh, 'systemctl enable d-brain-process.timer && systemctl start d-brain-process.timer')
    run_cmd(ssh, 'systemctl enable d-brain-weekly.timer && systemctl start d-brain-weekly.timer')

    # =========================================================================
    # Step 14: Configure Git
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 14: Configuring Git")
    print("=" * 60)

    run_cmd(ssh, f'su - {DEPLOY_USER} -c "cd {PROJECT_DIR} && git config user.name \'Agent Second Brain Bot\'"')
    run_cmd(ssh, f'su - {DEPLOY_USER} -c "cd {PROJECT_DIR} && git config user.email \'bot@localhost\'"')

    # =========================================================================
    # Step 15: Fix ownership
    # =========================================================================
    print("\n" + "=" * 60)
    print("  STEP 15: Fixing file ownership")
    print("=" * 60)

    run_cmd(ssh, f'chown -R {DEPLOY_USER}:{DEPLOY_USER} {PROJECT_DIR}')

    # =========================================================================
    # FINAL STATUS CHECK
    # =========================================================================
    print("\n" + "=" * 60)
    print("  FINAL STATUS CHECK")
    print("=" * 60)

    print("\n--- Services ---")
    run_cmd(ssh, 'systemctl is-active d-brain-bot && echo "Bot: RUNNING" || echo "Bot: NOT RUNNING"')
    run_cmd(ssh, 'systemctl is-active d-brain-process.timer && echo "Daily timer: ACTIVE" || echo "Daily timer: INACTIVE"')
    run_cmd(ssh, 'systemctl is-active d-brain-weekly.timer && echo "Weekly timer: ACTIVE" || echo "Weekly timer: INACTIVE"')

    print("\n--- Versions ---")
    run_cmd(ssh, 'python3.12 --version')
    run_cmd(ssh, 'node --version')
    run_cmd(ssh, f'su - {DEPLOY_USER} -c "$HOME/.local/bin/uv --version"')

    print("\n--- Files ---")
    run_cmd(ssh, f'test -f {PROJECT_DIR}/.env && echo ".env: EXISTS" || echo ".env: MISSING"')
    run_cmd(ssh, f'test -f {PROJECT_DIR}/mcp-config.json && echo "mcp-config.json: EXISTS" || echo "mcp-config.json: MISSING"')

    print("\n--- Timers ---")
    run_cmd(ssh, 'systemctl list-timers --no-pager | grep d-brain || echo "No timers found"')

    print("\n--- Bot logs (last 5 lines) ---")
    time.sleep(3)
    run_cmd(ssh, 'journalctl -u d-brain-bot -n 5 --no-pager 2>/dev/null || echo "No logs yet"')

    # =========================================================================
    # DONE
    # =========================================================================
    print("\n" + "=" * 60)
    print("  DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print(f"""
  VPS: {HOST}
  User: {DEPLOY_USER} (password: {DEPLOY_PASS})
  Project: {PROJECT_DIR}

  What's running:
    - Bot:        24/7 (listens to Telegram)
    - Processing: daily at 21:00
    - Digest:     Friday at 06:00

  Services connected:
    - Telegram Bot
    - Deepgram (voice transcription)
    - Todoist (task management via MCP)

  Next steps:
    1. SSH into VPS: ssh {DEPLOY_USER}@{HOST}
    2. Authenticate Claude: claude auth login
    3. Open Telegram and test your bot!

  Useful commands:
    sudo journalctl -u d-brain-bot -f        # live logs
    sudo systemctl restart d-brain-bot        # restart bot
    sudo systemctl list-timers | grep d-brain # check timers
""")

    ssh.close()


if __name__ == "__main__":
    main()
