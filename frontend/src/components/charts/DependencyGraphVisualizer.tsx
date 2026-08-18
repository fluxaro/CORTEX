import React from 'react';
import { Background, Controls, ReactFlow } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes = [
  {
    id: '1',
    position: { x: 40, y: 110 },
    data: { label: 'API Layer (/api/v1)' },
    style: {
      background: '#eff6ff',
      color: '#1e40af',
      border: '2px solid #93c5fd',
      borderRadius: '16px',
      padding: '12px 18px',
      fontSize: '12px',
      fontWeight: '800',
      boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
    },
  },
  {
    id: '2',
    position: { x: 300, y: 40 },
    data: { label: 'Service Layer (Services)' },
    style: {
      background: '#ecfdf5',
      color: '#065f46',
      border: '2px solid #a7f3d0',
      borderRadius: '16px',
      padding: '12px 18px',
      fontSize: '12px',
      fontWeight: '800',
      boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
    },
  },
  {
    id: '3',
    position: { x: 300, y: 180 },
    data: { label: 'Engine Layer (Analyzers)' },
    style: {
      background: '#faf5ff',
      color: '#6b21a8',
      border: '2px solid #e9d5ff',
      borderRadius: '16px',
      padding: '12px 18px',
      fontSize: '12px',
      fontWeight: '800',
      boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
    },
  },
  {
    id: '4',
    position: { x: 560, y: 110 },
    data: { label: 'Database ORM (Models)' },
    style: {
      background: '#fffbeb',
      color: '#92400e',
      border: '2px solid #fde68a',
      borderRadius: '16px',
      padding: '12px 18px',
      fontSize: '12px',
      fontWeight: '800',
      boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
    },
  },
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#2563eb', strokeWidth: 2 } },
  { id: 'e1-3', source: '1', target: '3', animated: true, style: { stroke: '#2563eb', strokeWidth: 2 } },
  { id: 'e2-4', source: '2', target: '4', style: { stroke: '#10b981', strokeWidth: 2 } },
  { id: 'e3-4', source: '3', target: '4', style: { stroke: '#9333ea', strokeWidth: 2 } },
];

export const DependencyGraphVisualizer: React.FC = () => {
  return (
    <div className="w-full h-80 rounded-2xl overflow-hidden border border-slate-200 bg-slate-50/50">
      <ReactFlow nodes={initialNodes} edges={initialEdges} fitView>
        <Background color="#cbd5e1" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  );
};
