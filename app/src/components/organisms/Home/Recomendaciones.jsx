import Title from "@/components/atoms/Title";
import Card from "@/components/molecules/Card";

export default function Recomendaciones() {
    return (
        <div className="bg-dark">
            <div className="container-md py-5">
                <Title color="white">Nuestras recomendaciones</Title>
            </div>
            <div className="container-md d-flex flex-row align-items-center justify-content-between gap-3 pb-5">
                <Card width="250px" height="450px" titlePosition="center" src="/images/recom1.webp" heading="2" className="shadow-white">Ajedrez Clásico</Card>
                <Card width="250px" height="450px" titlePosition="center" src="/images/recom2.webp" heading="2" className="shadow-white">Jardinera Vertical</Card>
                <Card width="250px" height="450px" titlePosition="center" src="/images/recom3.webp" heading="2" className="shadow-white">Pesebre Rústico</Card>
                <Card width="250px" height="450px" titlePosition="center" src="/images/recom4.webp" heading="2" className="shadow-white">Ajedrez Cuatro Jugadores</Card>
            </div>
        </div>
    );
}