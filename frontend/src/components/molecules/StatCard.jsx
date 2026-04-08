import React from 'react';
import { Card, Text } from '../atoms/UI.jsx';
import { Activity, Database, AlertTriangle } from 'lucide-react';

export const StatCard = ({ title, value, icon, subtext }) => {
  const icons = {
    activity: <Activity size={24} color="#2563eb" />,
    db: <Database size={24} color="#10b981" />,
    error: <AlertTriangle size={24} color="#ef4444" />
  };

  return (
    <Card style={{ display: 'flex', flexDirection: 'column', minWidth: '220px', flex: 1 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
        <Text variant="small" style={{ color: '#6b7280' }}>{title}</Text>
        {icons[icon]}
      </div>
      <Text variant="h1">{value}</Text>
      {subtext && <Text variant="small">{subtext}</Text>}
    </Card>
  );
};
