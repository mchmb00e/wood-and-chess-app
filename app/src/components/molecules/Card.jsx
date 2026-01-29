import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Title from '@/components/atoms/Title'; 

function Card({ 
    width = "100%",
    height = "400px",
    withOverlay = true,
    overlayColor = "#000000",
    overlayOpacity = 0.5,
    heading = 1,
    classNameHeading,
    className,
    titlePosition = "left",
    src,
    alt,
    children,
    href
}) {

    const [isHovered, setIsHovered] = useState(false);

    const navigate = useNavigate();

    const handleClick = (link) => {
        if (link) {
            navigate(link);
        }
    }

    const alignmentMap = {
        left: 'text-start',
        center: 'text-center',
        right: 'text-end'
    };
    const alignClass = alignmentMap[titlePosition] || 'text-center';

    return (
        <div 
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            
            onClick={() => handleClick(href)}

            className={`card border-0 rounded-0 overflow-hidden ${className || ''}`}
            style={{ 
                width: width, 
                height: height, 
                position: 'relative',
                cursor: 'pointer'
            }}
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
                    zIndex: 0,
                    
                    transform: isHovered ? 'scale(1.05)' : 'scale(1)',
                    transition: 'transform 0.3s ease-in-out'
                }}
                role="img"
                aria-label={alt}
            />

            {withOverlay && (
                <div 
                    style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        backgroundColor: overlayColor,
                        opacity: overlayOpacity,
                        zIndex: 1,
                        pointerEvents: 'none',
                        transition: 'opacity 0.3s'
                    }}
                />
            )}

            <div 
                className={`d-flex flex-column justify-content-end p-4 h-100 w-100 ${alignClass}`}
                style={{ 
                    position: 'relative', 
                    zIndex: 2,
                    pointerEvents: 'none'
                }}
            >
                <Title 
                    heading={heading} 
                    className={`text-white mb-0 ${classNameHeading || ''}`} 
                >
                    {children}
                </Title>
            </div>
        </div>
    );
}

export default Card;