import React, { useId } from 'react';

function Slider({ 
    children, 
    id,
    interval = 3000,
    controls = true,
    indicators = true,
    className = ""
}) {

    const generatedId = useId().replace(/:/g, "");
    const sliderId = id || `slider-${generatedId}`;

    const slides = React.Children.toArray(children);

    if (slides.length === 0) return null;

    return (
        <div 
            id={sliderId} 
            className={`carousel slide ${className}`} 
            data-bs-ride="carousel"
        >
            {indicators && (
                <div className="carousel-indicators">
                    {slides.map((_, index) => (
                        <button
                            key={index}
                            type="button"
                            data-bs-target={`#${sliderId}`}
                            data-bs-slide-to={index}
                            className={index === 0 ? "active" : ""}
                            aria-current={index === 0 ? "true" : "false"}
                            aria-label={`Slide ${index + 1}`}
                        ></button>
                    ))}
                </div>
            )}

            <div className="carousel-inner">
                {slides.map((child, index) => (
                    <div 
                        key={index} 
                        className={`carousel-item ${index === 0 ? "active" : ""}`}
                        data-bs-interval={interval}
                    >
                        <div className="d-flex justify-content-center">
                            {child}
                        </div>
                    </div>
                ))}
            </div>

            {controls && (
                <>
                    <button 
                        className="carousel-control-prev" 
                        type="button" 
                        data-bs-target={`#${sliderId}`} 
                        data-bs-slide="prev"
                    >
                        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span className="visually-hidden">Previous</span>
                    </button>
                    <button 
                        className="carousel-control-next" 
                        type="button" 
                        data-bs-target={`#${sliderId}`} 
                        data-bs-slide="next"
                    >
                        <span className="carousel-control-next-icon" aria-hidden="true"></span>
                        <span className="visually-hidden">Next</span>
                    </button>
                </>
            )}
        </div>
    );
}

export default Slider;