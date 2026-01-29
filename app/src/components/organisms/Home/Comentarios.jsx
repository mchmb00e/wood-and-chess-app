import BackgroundContainer from "@/components/atoms/BackgroundContainer";
import Title from "@/components/atoms/Title";
import Comment from "@/components/molecules/Comment";
import Slider from "@/components/molecules/Slider";

function Comentarios() {

    return (
        <BackgroundContainer src="/images/chess_oscuro.webp" overlayOpacity={0.7} className="py-5">
            <Title align="center" color="white">Ellos han confiado en nosotros</Title>
            <div className="container-md">
            <Slider className="mt-5 pb-5">
                <Comment width="50%" rate={5} author={"Nuve Bustamante"}>
                    “Al principio dudaba si el color de la madera se vería igual que en la pantalla, pero al recibirlo quedé impresionado. Usar el personalizador 3D fue súper fácil y el tablero llegó exactamente como lo diseñé. Se nota el cariño en el lijado y los detalles. 100% recomendado.”
                </Comment>
            </Slider>
            </div>
        </BackgroundContainer>
    );
}

export default Comentarios;