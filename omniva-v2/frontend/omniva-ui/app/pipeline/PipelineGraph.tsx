"use client";

import ReactFlow, { Background, Controls, Node, Edge } from "react-flow-renderer";

const nodes: Node[] = [
  { id: "scrape", data: { label: "Scrape" }, position: { x: 0, y: 0 } },
  { id: "download", data: { label: "Download" }, position: { x: 180, y: 0 } },
  { id: "transcribe", data: { label: "Transcribe" }, position: { x: 360, y: 0 } },
  { id: "analyze", data: { label: "Analyze" }, position: { x: 540, y: 0 } },
  { id: "edit", data: { label: "Edit" }, position: { x: 720, y: 0 } },
  { id: "upload", data: { label: "Upload" }, position: { x: 900, y: 0 } }
];

const edges: Edge[] = [
  { id: "e1", source: "scrape", target: "download" },
  { id: "e2", source: "download", target: "transcribe" },
  { id: "e3", source: "transcribe", target: "analyze" },
  { id: "e4", source: "analyze", target: "edit" },
  { id: "e5", source: "edit", target: "upload" }
];

export default function PipelineGraph() {
  return (
    <div style={{ height: 320, background: "#1a1a1a", borderRadius: 8 }}>
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
