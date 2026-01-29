import React from 'react';
import Icon from '@/components/atoms/Icon';

function TextField({
    width = "100%",
    fontSize = 3,
    icon,
    placeholder,
    color = "white",
    className,
    ...rest
}) {

    const iconSizeMap = {
        1: 32, 2: 28, 3: 24, 4: 20, 5: 18, 6: 16
    };
    const currentIconSize = iconSizeMap[fontSize] || 24;

    return (
        <div 
            className={`d-flex align-items-center border-bottom border-${color} ${className || ''}`}
            style={{ 
                width: width,
                paddingBottom: '8px'
            }}
        >
            {icon && (
                <div className="me-3">
                    <Icon name={icon} size={currentIconSize} color={color} />
                </div>
            )}

            <input 
                type="text" 
                className={`bg-transparent border-0 text-${color} w-100 fs-${fontSize}`}
                placeholder={placeholder}
                style={{ 
                    outline: 'none',
                    boxShadow: 'none'
                }}
                {...rest}
            />
        </div>
    );
}

export default TextField;