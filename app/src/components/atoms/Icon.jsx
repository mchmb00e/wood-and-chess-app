const Icon = ({ name, size, color }) => {
  const colorClass = color ? `text-${color}` : '';

  return (
    <i 
      className={`bi bi-${name} ${colorClass}`}
      
      style={{ 
        fontSize: `${size}px`,
        lineHeight: 1,
        display: 'inline-flex',
        verticalAlign: 'middle'
      }}
      
      role="img" 
      aria-label={name}
    />
  );
};

Icon.defaultProps = {
  size: 16,
  color: undefined
};

export default Icon;