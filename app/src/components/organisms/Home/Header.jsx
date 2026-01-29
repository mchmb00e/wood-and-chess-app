import Nav from "@/components/molecules/Nav";
import BackgroundContainer from "@/components/atoms/BackgroundContainer";
import Card from "@/components/molecules/Card";
import Title from "@/components/atoms/Title";
import ChessKingViewer from "@/components/molecules/ChessKingViewer";

export default function Header({pageTitle, isLogged}) {

    const posCard = 450;
    return (
        <header>
            <div className="bg-dark">
                <BackgroundContainer 
                    src="/images/bg_header1.png" 
                    overlayOpacity={0.7}
                    className="pb-5"
                    style={{ paddingBottom: '8rem' }}
                >
                    <Nav pageTitle={pageTitle} isLogged={isLogged} />

                    <div className="mt-5 container" style={{marginBottom: `${posCard / 2}px`}}>
                        <Title color="white" align="center">Herencia de mi Abuelo</Title>
                        <p className="text-white text-center">Artesanía en madera, tableros personalizados y decoración para el hogar.</p>
                    </div>
                </BackgroundContainer>

                <div 
                    className="d-flex flex-row align-items-center justify-content-center gap-3 flex-wrap"
                    style={{ 
                        marginTop: `${-1 * (posCard / 2)}px`,
                        position: 'relative',
                        zIndex: 10,
                        paddingBottom: '3rem'
                    }}
                >
                    <Card
                        width="250px"
                        height={`${posCard}px`}
                        src="/images/pesebre.webp"
                        heading="2"
                        className="shadow-white"
                    >Pesebre</Card>
                    <Card
                        width="250px"
                        height={`${posCard}px`}
                        src="/images/chess_white.webp"
                        heading="2"
                        className="shadow-white"
                    >Ajedrez</Card>
                    <Card
                        width="250px"
                        height={`${posCard}px`}
                        src="/images/jardinera.webp"
                        heading="2"
                        className="shadow-white"
                    >Jardinera</Card>
                </div>

                <section className="d-flex flex-row justify-content-center align-items-center container-md mt-3">
                    <div className="col-6">
                        <Title color="white" className="mb-5">Un ajedrez a medida</Title>
                        <p className="text-white fst-italic">¿Sabías que nuestros ajedreces están construidos de forma artesanal?</p>
                        <p className="text-white">
                            Nuestros tableros combinan la calidez de la carpintería tradicional con la tecnología  moderna.
                            No necesitas imaginar cómo quedará: usa nuestro personalizador 3D para probar diferentes maderas,
                            acabados y estilos en tiempo real. <span className="fw-bold">Tú te encargas del diseño</span>, nosotros lo hacemos realidad a mano.
                        </p>
                    </div>
                    <div className="col-6 d-flex align-items-start justify-content-center">
                        <ChessKingViewer height="400px"></ChessKingViewer>
                    </div>
                </section>
            </div>
        </header>
    );
}