#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="pryma-tech-website"
HOST_PORT="${1:-8080}"
RULE_NAME="omniva-dashboard-allow"
NETWORK_TAG="omniva-dashboard"

echo "Detecting public IP for trusted CIDR..."
MY_IP="$(curl -s https://ifconfig.me)"
if [[ -z "$MY_IP" ]]; then
  echo "ERROR: Could not determine public IP."
  exit 1
fi
TRUSTED_CIDR="${MY_IP}/32"
echo "Using trusted CIDR: $TRUSTED_CIDR"

echo "Querying VM metadata..."
VM_NAME="$(curl -s -H 'Metadata-Flavor: Google' \
  http://metadata.google.internal/computeMetadata/v1/instance/name)"
ZONE="$(curl -s -H 'Metadata-Flavor: Google' \
  http://metadata.google.internal/computeMetadata/v1/instance/zone | awk -F/ '{print $NF}')"

if [[ -z "$VM_NAME" || -z "$ZONE" ]]; then
  echo "ERROR: Could not determine VM metadata."
  exit 1
fi
echo "VM: $VM_NAME (zone: $ZONE)"

echo "Creating firewall rule $RULE_NAME (tcp:$HOST_PORT)..."
gcloud compute firewall-rules create "$RULE_NAME" \
  --project="$PROJECT_ID" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules="tcp:${HOST_PORT}" \
  --source-ranges="$TRUSTED_CIDR" \
  --target-tags="$NETWORK_TAG"

echo "Tagging VM with $NETWORK_TAG..."
gcloud compute instances add-tags "$VM_NAME" \
  --tags="$NETWORK_TAG" \
  --zone="$ZONE"

echo "Done. Traffic from $TRUSTED_CIDR can now reach tcp:$HOST_PORT."
