export default function Alert({className = "", color = "dark", children}) {
    return (
        <div className={`alert alert-${color} ${className}`} role="alert">
            {children}
        </div>
    );
}