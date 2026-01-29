import { numberDots } from "@/utils/numberDots";
import Button from "@/components/atoms/Button";
import Title from "@/components/atoms/Title";


function ProductCard({
    height = "400px",
    width = "200px",
    title,
    description,
    src,
    onClick,
    price = "0",
}) {

    const priceDots = "$ " + numberDots(price);
    const resumeDescription = description.substring(0, 40) + "..."

    return (
        <div style={{ width: width, height: height }}>
            <div
                style={{
                    height: parseInt(height) / 2,
                    overflow: 'hidden'
                }}
                className="d-flex align-items-center justify-content-center"
            >
                <img
                    src={src}
                    style={{
                        width: "100%",
                        height: "auto",
                        display: "block",
                        objectFit: "cover"
                    }}
                    alt="Imagen centrada"
                />
            </div>
            <div className="bg-white">
                <div className="d-flex justify-content-between align-items-center">
                    <Title heading="5" color="dark" align="start">
                        {title}
                    </Title>
                    <span>
                        {priceDots}
                    </span>
                </div>
                <div>
                    <p>
                        { resumeDescription }
                    </p>
                </div>
                <div>
                    <Button
                        btnColor="primary"
                        textColor="white"
                        iconName="cart"
                        iconSize="24"
                    >Agregar al carro</Button>
                </div>
            </div>
        </div>
    );

}

export default ProductCard;