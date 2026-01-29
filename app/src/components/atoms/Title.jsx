function Title({
    children,
    heading,
    color,
    align,
    className
}) {

    const Tag = heading ? `h${heading}` : "h1";
    const classes = [
    color ? `text-${color}` : '',
    align ? `text-${align}` : '',
    className
    ].filter(Boolean).join(' ');

    return (
        <Tag
        className={classes}>
                {children}
        </Tag>
    );
}

export default Title;