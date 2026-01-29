import Icon from "@/components/atoms/Icon";

function Button({
    children,
    isOutline,
    btnColor,
    isBold,
    borderWeight,
    iconName,
    iconSize,
    textColor,
    isNoButton,
    onClick,
    className,
    disabled // 1. Recibimos la prop
}) {
    
    // 2. Saneamos el valor: undefined/null/false se convierten en FALSE puro.
    const isReallyDisabled = !!disabled; 

    return (
        <button 
            disabled={isReallyDisabled} // 3. Pasamos el valor saneado al HTML
            onClick={onClick} 
            className={`
                d-flex flex-row gap-2 align-items-center justify-content-center
                ${textColor ? `text-${textColor}` : ""}
                ${isBold ? "fw-bold" : ""}
                
                ${isNoButton 
                    ? "bg-transparent border-0 p-0 text-decoration-none"
                    : `btn btn${isOutline ? "-outline" : ""}-${btnColor ? btnColor : "primary"} ${borderWeight ? `border-${borderWeight}` : ""}`
                }
                ${className ? className : ""}
                
                /* 4. Aplicamos opacidad visual siempre que esté deshabilitado */
                ${isReallyDisabled ? "opacity-50" : ""}
            `}
            
            // 5. Cursor de prohibido usando la variable saneada
            style={{ cursor: isReallyDisabled ? 'not-allowed' : 'pointer' }}
        >
            {
                (iconName && iconSize) ?
                <Icon name={iconName} size={iconSize} /> :
                ""
            }
            {
                children
            }
        </button>
    );
}

export default Button;