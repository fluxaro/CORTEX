import React from 'react';
import { Background, Controls, ReactFlow } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes = [
  { id: '1', position: { x: 50, y: 120 }, data: { label: 'API Layer (/api/v1)' }, style: { background: '#1e293b', color: '#60a5fa', border: '1px solid #3b82f6', borderRadius: '10px', padding: '10px' } },
  { id: '2', position: { x: 300, y: 50 }, data: { label: 'Service Layer (Services)' }, style: { background: '#1e293b', color: '#34d399', border: '1px solid #10b981', borderRadius: '10px', padding: '10px' } },
  { id: '3', position: { x: 300, y: 190 }, data: { label: 'Engine Layer (Analyzers)' }, style: { background: '#1e293b', color: '#c084fc', border: '1px solid #8b5cf6', borderRadius: '10px', padding: '10px' } },
  { id: '4', position: { x: 550, y: 120 }, data: { label: 'Database ORM (Models)' }, style: { background: '#1e293b', color: '#fbbf24', border: '1px solid #f59e0b', borderRadius: '10px', padding: '10px' } },
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#3b82f6' } },
  { id: 'e1-3', source: '1', target: '3', animated: true, style: { stroke: '#3b82f6' } },
  { id: 'e2-4', source: '2', target: '4', style: { stroke: '#10b981' } },
  { id: 'e3-4', source: '3', target: '4', style: { stroke: '#8b5cf6' } },
];

export const DependencyGraphVisualizer: React.FC = () => {
  return (
    <div className="w-full h-80 rounded-xl overflow-hidden border border-border/80 glass-panel">
      <ReactFlow nodes={initialNodes} edges={initialEdges} fitView>
        <Background color="#1f293d" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  );
};
