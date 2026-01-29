import React from 'react';

function BackgroundContainer({ 
    src, 
    overlayColor = "#000000", 
    overlayOpacity = 0.5, 
    children, 
    className = "",
    style = {},
    childrenClassName = "",
    ...rest
}) {
    return (
        <div 
            className={`position-relative ${className}`}
            style={{ 
                minHeight: '50px', 
                ...style 
            }}
            {...rest}
        >
            <div 
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    backgroundImage: `url(${src})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    zIndex: 0
                }}
            />

            <div 
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    backgroundColor: overlayColor,
                    opacity: overlayOpacity,
                    zIndex: 1
                }}
            />
            <div 
                style={{ 
                    position: 'relative', 
                    zIndex: 2,
                    width: '100%',
                    height: '100%' 
                }}
                className={childrenClassName}
            >
                {children}
            </div>
        </div>
    );
}
export default BackgroundContainer;