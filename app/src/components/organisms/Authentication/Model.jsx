import BackgroundContainer from "@/components/atoms/BackgroundContainer";
import ChessKingViewer from "@/components/molecules/ChessKingViewer";

export default function Model({className = ""}) {
    return <BackgroundContainer
        src="/images/horses1.webp"
        overlayOpacity="0.7"
        className={className}
        childrenClassName="d-flex flex-row justify-content-center align-items-center">
        <ChessKingViewer className="w-25 vh-100" />
    </BackgroundContainer>
}