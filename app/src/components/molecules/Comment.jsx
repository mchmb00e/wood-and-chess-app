import Title from '@/components/atoms/Title';
import Rate from '@/components/atoms/Rate';

function Comment({
    width = "500px",
    rate,
    title,
    author,
    rateColor = "primary", textColor = "white",
    children = "No se dió una descripción.",
    className = ""
}) {

    return (
        <div className={`d-flex flex-column gap-2 ${className}`} style={{
            width: width
        }}>
            <Rate number={rate} color={rateColor}></Rate>
            {
                (title) ? <Title heading="3" color={textColor}>{title}</Title> : ""
            }
            <p className={
                `text-${textColor}`
            }>
                {children}
                <br></br>
                <br></br>
                <b>
                - {author}
                </b>
            </p>
        </div>
    );
}

export default Comment;