import Icon from '@/components/atoms/Icon';

export default function Rate({ number, color = "primary", size = "24" }) {

    const iterations = Array.from({ length: parseInt(number) || 0 }, (v, i) => i);

    return (
        <div className="d-flex flex-row align-items-center gap-2 pb-2">
            {
                iterations.map((index) => {
                    return <Icon name="star-fill" color={color} size={size} key={index} />
                })
            }
        </div>
    );
}