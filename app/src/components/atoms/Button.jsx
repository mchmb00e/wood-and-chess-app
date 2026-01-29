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
    isNoButton
}) {
    
    return (
        <button className={`
            d-flex flex-row gap-2 align-items-center justify-content-center
            ${textColor ? `text-${textColor}` : ""}
            ${isBold ? "fw-bold" : ""}
            
            ${isNoButton 
                ? "bg-transparent border-0 p-0 text-decoration-none"
                : `btn btn${isOutline ? "-outline" : ""}-${btnColor ? btnColor : "primary"} ${borderWeight ? `border-${borderWeight}` : ""}`
            }
        `}>
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