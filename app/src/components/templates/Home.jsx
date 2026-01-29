import { useTitle } from '@/hooks/useTitle';
import Header from '@/components/organisms/Home/Header';
import Comentarios from '@/components/organisms/Home/Comentarios';
import Recomendaciones from '@/components/organisms/Home/Recomendaciones';
import Footer from '@/components/molecules/Footer';

function Home() {
    const pageTitle = 'Home';
    useTitle(pageTitle);

    return (
        <>
        <Header pageTitle={pageTitle} />
        <Comentarios />
        <Recomendaciones></Recomendaciones>
        <Footer></Footer>
        </>
    );
}

export default Home;