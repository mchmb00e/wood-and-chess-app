import React, { useMemo } from 'react';
import Icon from '@/components/atoms/Icon';

function TextField({
    width = "100%",
    fontSize = 3,
    placeholderSize,
    label, // 1. Nueva prop para el texto superior
    icon,
    placeholder,
    color = "white",
    className,
    isHidden,
    onChange,
    ...rest
}) {

    // Generamos un ID único para vincular el label con el input
    const inputId = useMemo(() => `input-${Math.random().toString(36).substr(2, 9)}`, []);

    const iconSizeMap = {
        1: 32, 2: 28, 3: 24, 4: 20, 5: 18, 6: 16
    };
    const currentIconSize = iconSizeMap[fontSize] || 24;

    return (
        <div className={`${className || ''}`} style={{ width: width }}>
            {/* 2. Estilos dinámicos para el placeholder */}
            {placeholderSize && (
                <style>
                    {`
                        #${inputId}::placeholder {
                            font-size: ${placeholderSize}px !important;
                        }
                    `}
                </style>
            )}

            {/* 3. Renderizado condicional del Label */}
            {label && (
                <label 
                    htmlFor={inputId} 
                    className={`d-block text-${color} fs-5`} // fs-5 para un tamaño legible estándar
                >
                    {label}
                </label>
            )}

            {/* 4. Contenedor del Input (La línea inferior) */}
            <div 
                className={`d-flex align-items-center border-bottom border-${color}`}
                style={{ paddingBottom: '8px' }}
            >
                {icon && (
                    <div className="me-3">
                        <Icon name={icon} size={currentIconSize} color={color} />
                    </div>
                )}

                <input 
                    id={inputId}
                    type={`${isHidden ? "password" : "text"}`} 
                    className={`bg-transparent border-0 text-${color} w-100 fs-${fontSize}`}
                    placeholder={placeholder}
                    style={{ 
                        outline: 'none',
                        boxShadow: 'none'
                    }}
                    onChange={onChange}
                    {...rest}
                />
            </div>
        </div>
    );
}

export default TextField;