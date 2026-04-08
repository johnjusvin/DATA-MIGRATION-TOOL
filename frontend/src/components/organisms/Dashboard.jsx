import React, { useState, useEffect } from 'react';
import { Card, Text, Button } from '../atoms/UI.jsx';
import { StatCard } from '../molecules/StatCard.jsx';
import { fetchStatus, fetchDlqStats, triggerStart } from '../../services/api';

export const Dashboard = () => {
  const [data, setData] = useState({ status: 'Pending', total_rows_migrated: 0, table_stats: {} });
  const [dlq, setDlq] = useState({ total_failed: 0, breakdown: {} });
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    try {
      const st = await fetchStatus();
      const dq = await fetchDlqStats();
      setData(st);
      setDlq(dq);
    } catch(err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    setLoading(true);
    await triggerStart();
    setTimeout(() => {
        setLoading(false);
        loadData();
    }, 1000);
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <Text variant="h1">Data Migration Studio</Text>
          <Text variant="small">Legacy to Modern DB Transformation & Reporting</Text>
        </div>
        <Button onClick={handleStart} disabled={loading || data.status === 'Running'}>
            {data.status === 'Running' ? 'Migration In Progress...' : 'Start Migration'}
        </Button>
      </div>

      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
        <StatCard title="System Status" value={data.status} icon="activity" subtext="Polls every 3s" />
        <StatCard title="Rows Migrated" value={data.total_rows_migrated.toLocaleString()} icon="db" subtext="Across all tables" />
        <StatCard title="DLQ Failures" value={dlq.total_failed} icon="error" subtext="Rows rejected/failed" />
      </div>

      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
        
        {/* Table Stats block */}
        <Card style={{ flex: 2 }}>
            <Text variant="h2">Table Progress</Text>
            {Object.keys(data.table_stats).length === 0 ? (
                <Text style={{color: '#6b7280', marginTop:'20px'}}>No tables processed yet.</Text>
            ) : (
                <table style={{ width: '100%', marginTop: '20px', borderCollapse: 'collapse', textAlign: 'left' }}>
                    <thead>
                        <tr style={{ borderBottom: '1px solid #e5e7eb' }}>
                            <th style={{ padding: '8px' }}>Table Name</th>
                            <th style={{ padding: '8px' }}>Rows Done</th>
                            <th style={{ padding: '8px' }}>Batches</th>
                            <th style={{ padding: '8px' }}>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(data.table_stats).map(([table, stat]) => (
                            <tr key={table} style={{ borderBottom: '1px solid #f3f4f6' }}>
                                <td style={{ padding: '8px' }}>{table}</td>
                                <td style={{ padding: '8px' }}>{stat.rows_done.toLocaleString()}</td>
                                <td style={{ padding: '8px' }}>{stat.last_batch}</td>
                                <td style={{ padding: '8px', color: stat.status === 'completed' ? '#10b981' : '#2563eb' }}>{stat.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </Card>
        
        {/* DLQ Breakdown Block */}
        <Card style={{ flex: 1, borderLeft: '4px solid #ef4444' }}>
            <Text variant="h2">Dead Letter Queue Reports</Text>
            <ul style={{ paddingLeft: '20px', marginTop: '20px' }}>
                {Object.keys(dlq.breakdown).length === 0 ? (
                    <Text variant="small">No errors logged.</Text>
                ) : (
                    Object.entries(dlq.breakdown).map(([tbl, count]) => (
                        <li key={tbl} style={{marginBottom:'8px'}}>
                            <Text>{tbl}: <strong style={{color:'#ef4444'}}>{count}</strong> rows failed</Text>
                        </li>
                    ))
                )}
            </ul>
        </Card>
      </div>

    </div>
  );
};
