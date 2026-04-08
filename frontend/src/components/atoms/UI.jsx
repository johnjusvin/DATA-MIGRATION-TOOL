import React from 'react';

export const Button = ({ onClick, children, variant = 'primary', disabled = false }) => {
  const styles = {
    primary: { background: '#2563eb', color: 'white', padding: '10px 20px', borderRadius: '6px', border: 'none', cursor: 'pointer', fontWeight: 600 },
    danger: { background: '#dc2626', color: 'white', padding: '10px 20px', borderRadius: '6px', border: 'none', cursor: 'pointer', fontWeight: 600 }
  };
  
  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      style={{ ...styles[variant], opacity: disabled ? 0.5 : 1 }}
    >
      {children}
    </button>
  );
};

export const Card = ({ children, style }) => (
  <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', ...style }}>
    {children}
  </div>
);

export const Text = ({ children, variant = 'body' }) => {
  const size = variant === 'h1' ? '24px' : variant === 'h2' ? '18px' : variant === 'small' ? '12px' : '14px';
  const weight = variant.startsWith('h') ? 600 : 400;
  return <span style={{ fontSize: size, fontWeight: weight, display: 'block', margin: '4px 0' }}>{children}</span>;
};