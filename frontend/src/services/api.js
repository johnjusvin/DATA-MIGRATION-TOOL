const b64Auth = btoa('admin:migrate123!');
const headers = { 'Authorization': `Basic ${b64Auth}` };

export const fetchStatus = async () => {
    const res = await fetch('/api/status', { headers });
    return await res.json();
};

export const fetchDlqStats = async () => {
    const res = await fetch('/api/dlq/stats', { headers });
    return await res.json();
};

export const triggerStart = async () => {
    const res = await fetch('/api/start', { method: 'POST', headers });
    return await res.json();
};
